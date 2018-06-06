# KMD Scaling Test

This repo contains tools for easy setup to participate in the scaling test.

Please sign up here: [Signup Sheet for Scaling Test](http://pad.supernet.org/Stress_Test_Signups)

## Install Steps
These steps are for installing on an empty server/vps. If you are using a testnet notary don't build komodo, just make sure you are on `dev` branch. The scripts will be compatible with komodo in `~/komodo`. There is also a docker folder, from PatchKez that will generate all these assetchains into docker containers. If you want to do it this way wait for more information, I haven't tested these yet.

**The script called buildkomodo.sh builds komodo from libscotts branch called momo if you need to install manually plese check the contents of that script**

```shell
sudo apt-get install git libcurl3
git clone https://github.com/blackjok3rtt/scaletest.git -b momo
cd scaletest
./buildkomodo.sh
```

### For All Nodes
```shell
./setchains 0 63
./sync_assets
```

The first command sets the range of the chains you are using, we are notarizing only 64.

## assets-cli

This file lets you interact with all the chains.

Examples:
```shell
./assets-cli importprivkey

./assets-cli stop
```

## TXSCL-cli

Interacts with just the first of the test chains only.

Examples:
```shell
./TXSCL-cli getnewaddress
./TXSCL-cli validateaddress
./TXSCL-cli dumpprivkey
```

## Notary Nodes
For notary nodes, you need to do the usual things but a few steps are diffrent.
You need to install komodo from libscott branch momo. The buildkomodo.sh script will do this for you if using momo branch of this repo.

Install SuperNET form jl777 branch

`git clone https://github.com/jl777/SuperNET.git -b jl777`

You need the usual wp_7776 file, there is one in this repo that will source your passphrase from `passphrase.txt`

`cp wp_7776 ~/SuperNET/iguana`

`nano ~/SuperNET/iguana/passphrase.txt`

copy your pubkey.txt to SuperNET dir

`cp ~/komodo/src/pubkey.txt ~/SuperNET/iguana/`

You will also need to: `cp m_notary_scale ~/SuperNET/iguana/`

Once you have all 64 TXSCL chains running and synced. Import your private key:

`assets-cli importprivkey "private key"`

To call dPoW for all 64 chains do:

`./startdpow`
