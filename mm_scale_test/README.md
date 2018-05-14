### Dependancies
Have all the chains running, `./sync_assets`

create the `passphrase` file in scripts sub directory

`passphrase="your passphrase in quotes"`

from mm_scale_test directory run `./client`

it will show `userpass` in console after started `marketmaker`

use that and save it in `userpass` file

`userpass=<user pass from marketmaker console output>`

Run `./calcaddfirstrun` Get the Raddress from here and get someone to fund you to this address. 

You also need to `./assets-cli importprivkey "wif"` for the shown wif key. 

### Instructions

Once marketmaker is running check you have balance on all chains with `./assets-cli getbalance`

From `mm_scale_test` dir run `./generateUTXO`

One this is finished a heap of files will be generated that get used in the next steps, these files are overwritten each time you run `./generateUTXO` so be careful what you are doing or you will lose funds.

Now run `pkill -15 marketmaker` a few times, to make sure marketmaker is not running.

Launch the marketmakers from the `mm_scale_test` dir using `./launchMM`

Wait until all the marketmakers have loaded, this takes a little while. :) 

Then launch `./TXblastMM100.sh`

Watch and wait until the loops have finished.

To start another set of loops just run `./generateUTXO` again then run `TXblastMM100.sh`
