# KMD Scaling Test 

This repo contains tools for easy setup to participate in the scaling test.

Please sign up here: [Signup Sheet for Scaling Test](http://pad.supernet.org/Stress_Test_Signups)

## Install Steps
These steps are for installing on an empty server/vps. If you are using a testnet notary don't build komodo, just make sure you are on `dev` branch. The scripts will be compatible with komodo in `~/komodo`. There is also a docker folder, from PatchKez that will generate all these assetchains into docker containers. If you want to do it this way wait for more information, I haven't tested these yet. 

**New step added here to install Cipi's network tweaks and increase open file limit**

```shell
sudo apt-get install git libcurl3
git clone https://github.com/blackjok3rtt/scaletest.git
cd scaletest
./applytweaks.sh
sudo reboot
./applytweaks.sh
sudo reboot
./buildkomodo.sh
```

### For All Nodes
```shell
./setchains x y
./sync_assets
```

The first command sets the range of the chains you are using. Everything else will be generated from this. The default value is 4096, but we have only made 0 - 1023 chains for this test. The second command starts the chains and syncs them.


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

# TX Blasters

[**See README.md in mm_scale_test folder**](https://github.com/blackjok3rtt/scaletest/blob/4096/mm_scale_test/README.md)

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
