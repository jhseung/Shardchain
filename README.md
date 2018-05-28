# Shardchain

## Abstract

A proposed solution to address the scalability limitations of the Ethereum network by sharding network transactions. The paper can be found [here](https://drive.google.com/open?id=1wGog0stvkCzDgvs8qIz9-GdCEaHOHB37)

The Shardchain attempts to increase transaction throughput by designating each transaction into one of _N_ shards, each with its own consensus mechanism. The network, instead of it being one blockchain containing the information to all previous information, will be sharded into multiple _shardchains_ and a single _mainchain_.

The _mainchain_ is responsible for maintaining the integrity of the network, and performs a similar role to the single blockchain in any other blockchain network –– Bitcoin, Ethereum, etc. It contains the canonical headers of each _shardchain_. The _shardchains_ are responsible for validating the transactions, after they have been designated a specific shard via the hash of the transaction sender address.

## Code

This codebase attempts to replicate the affects that sharding can have on the throughput of the Ethereum network. We aim to discover the tradeoff between the security to settle transactions and the total transaction throughput of a Proof of Work based blockchain network with sharding implemented.

The latest version provides the most basic functionalities of a cryptocurrency –– sending & receiving balances, validating transactions & mining blocks via the Proof of Work consensus mechanism, and propagating & receiving mined blocks. It contains the base logic for a Proof of Work based sharded blockchain, and the numbers are set to replicate the activity of the actual Ethereum network.
