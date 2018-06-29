# KMD Scaling Test 

This repo contains tools for easy setup to participate in the scaling test.

Please sign up here: [Signup Sheet for Scaling Test](http://pad.supernet.org/Stress_Test_Signups)

## Install Steps
These steps are for installing on an empty server/vps. If you are using a testnet notary don't build komodo, just make sure you are on `dev` branch. The scripts will be compatible with komodo in `~/komodo`. There is also a docker folder, from PatchKez that will generate all these assetchains into docker containers. If you want to do it this way wait for more information, I haven't tested these yet. 

**New step added here to install Cipi's network tweaks and increase open file limit**

```shell
sudo apt-get install git
git clone https://github.com/blackjok3rtt/scaletest.git
cd scaletest
./applytweaks.sh
sudo reboot
./buildkomodo.sh
```

When this is complete please refer to the section below for the role you are filling.

### FOR ALL NODES

You will need to create a pubkey.txt file and place it in the **scaletest** directory in the format.

```shell
pubkey=<yourpubkey>
```

To get a pubkey run `validateaddress` on an Raddress you have the private key for. (see [txtest-cli](#txtest-cli)) section below for an example of how to get a new address if you don't already have one you want to use.

Then you will specify the range of chains you wish to work with

```shell
./setchains <startnum> <endnum>
```

Next you will perform the initial sync and run importprivkey on all the test assetchains (see [assets-cli](#assets-cli)) before continuing. 

```shell
./sync_assets
./assets-cli importprivkey <your private key>
```

After importing the private key, you will need to restart your chains.

You will need funds sent to the address from the seed node operator to the R address of pubkey.txt in this folder.

**Make sure your Raddress is posted in the Signups Page so the operator can send funds.**

## For Transaction Blasters

### For Large Powerful Systems 

To blast transactions, this script will send 100 loops of 5 transactions on each chain. 50,000 Transactions each with 100 outputs. 5M payments per call.

```shell
./sync_assets
sh blastloop.sh
```
### For Smaller Systems 1-4 Core VPS

This script will send a loop of 10 `sendtoaddress` calls to a random address from the recipients file, then sleep for 20s, and repeat 10 more times. To send a total of 1000 TX. If the CPU is not being maxed out you can decrease sleep time. You might have to fine tune for your particualr system.

```shell
./sync_assets
sh slowloop.sh
```

### For CPU Miners

```shell
./mineassets
```

### For Regular Nodes (Stats, Mining Pool etc)
```shell
./sync_assets
```

## assets-cli 

This file lets you interact with all the chains.

Examples:
```shell
./assets-cli importprivkey

./assets-cli stop
```

### TXTEST-cli 

Interacts with just the first of the test chains only.

Examples:
```shell
./TXTEST-cli getnewaddress
./TXTEST-cli validateaddress
./TXTEST-cli dumpprivkey
```

# Generating Chains

**FOR THE FIRST ROUND OF TESTS THESE ARE NOT REQUIRED OF TESTERS**

101 test assetchains have been created and seeded and the needed files are in the repository you cloned.  Do not run these scripts or you might overwrite files needed in the first round of testing.

The **genac** script creates the initial parameters new test chains. 

Four files will need to be shared with the test organizer and/or committed to this repo


```shell
./genacs <numchains> <chainname> <supply>
```

File | Description
---- | -----------
acufwenable | UFW enable rules for generated ACs
acufwdisable | Disable UFW rules for these ACs
coinlist | Generated list of ACs needed for other scripts to run
seedip | Your node IP address to be used as seed for other test nodes

# Mining Pool Setup - ZNOMP

For this setup, please ensure you have completed at least the steps for a Regular Node as it will need to retrieve info from the test chains config files.

```shell
cd ~/scaletest/znomp/
nano generate
```

Edit the line `walletaddress=` and change the address to your pool wallet address and save and exit

```shell
./generate
```

Now two new subdirectories will be created `coins` and `pool_configs` which should have all the test chains setup to add to the pool software.

Stratum ports are set to start at 20777 and increment by 1 for each additional test chain.

.
