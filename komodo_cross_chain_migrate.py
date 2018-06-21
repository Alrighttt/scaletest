import sys
import subprocess
import json


# create an output with some funds to send across chain
# komodo-cli -ac_name=TXSCL sendtoaddress $inputaddress 2

inputaddress = sys.argv[1]
amount = sys.argv[4]
source_chain = sys.argv[2]
target_chain = sys.argv[3]


def cmd(*args):
    print >>sys.stderr, ('\033[90m> %s\033[0m' % ' '.join(args))
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    assert not p.wait()
    return p.stdout.read()


privkey = cmd('komodo-cli', '-ac_name=' + source_chain, 'dumpprivkey', inputaddress).strip()

tx = {"inputs":[{
        "txid":sys.argv[5],
        "idx":sys.argv[6],
        "script":{"address":inputaddress}}
    ],
    "outputs":[{
        "script":{"address":inputaddress},
        "amount": int(amount * 1e8)
    }]
}

print >>sys.stderr, "sign and encode tx"

# Tx needs to be signed so it can be encoded
txsigned = cmd('hoek', 'signTxBitcoin', json.dumps({"tx":tx, "privateKeys":[privkey]}))
# Get tx as hex
txraw = json.loads(cmd('hoek', 'encodeTx', txsigned))['hex']

print >>sys.stderr, "convert tx to export and re-sign"

# Convert tx to an export, this encodes the transaction's outputs in an OP_RETURN, as well as
# a merkle tree leading to the MoM
exportData = json.loads(cmd('komodo-cli', '-ac_name=' + source_chain, 'migrate_converttoexport', txraw, target_chain, str(amount)))

# Now need to re-sign the burn tx, so copy the OP_RETURN output into our unsigned tx, sign and encode
exportTx = tx.copy()
exportTx['outputs'] = json.loads(cmd('hoek', 'decodeTx', json.dumps({"hex":exportData['exportTx']})))['outputs']
exportTxSigned = cmd('hoek', 'signTxBitcoin', json.dumps({"tx":exportTx, "privateKeys":[privkey]}))
exportTxRawData = json.loads(cmd('hoek', 'encodeTx', exportTxSigned))

print >>sys.stderr, "broadcasting burn"

try:
    burnTxid = cmd("komodo-cli", '-ac_name=' + source_chain, 'sendrawtransaction', exportTxRawData['hex'])
except AssertionError as e:
    burnTxid = exportTxRawData['txid']

print >>sys.stderr, "burn txid:", burnTxid

print >>sys.stderr, "createimporttransaction"
importTxPart = cmd("komodo-cli", '-ac_name=' + source_chain, "migrate_createimporttransaction", exportTxRawData['hex'], exportData['payouts']).strip()

print >>sys.stderr, "completeimporttransaction, this requires two notarisations after the tx in order to succeed"
importTx = cmd("komodo-cli", "migrate_completeimporttransaction", importTxPart)
print importTx
print >>sys.stderr, "broadcast the above on target chain using sendrawtransaction"
