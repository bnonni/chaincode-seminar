# Scripts and Wallets

## Reading

| Content | Time \(min\) |
| :--- | :--- |
| [Bitcoin Script: Past and Future](https://btctranscripts.com/chaincode-labs/2020-04-08-john-newbery-contracts-in-bitcoin/) | 35 |
| [Script: A Mini Programming Language](https://learnmeabitcoin.com/technical/script) | 15 |
| [Scripts \(general & simple\)](https://btctranscripts.com/scalingbitcoin/tokyo-2018/edgedevplusplus/scripts-general-and-simple/) | 40 |
| [Miniscript: Streamlined Bitcoin Scripting](https://medium.com/blockstream/miniscript-bitcoin-scripting-3aeff3853620) | 15 |
| \(_optional_\) [Using the Chain for What Chains are Good For](https://btctranscripts.com/scalingbitcoin/stanford-2017/using-the-chain-for-what-chains-are-good-for/) | 30 |
| [The Battle for P2SH](https://bitcoinmagazine.com/technical/the-battle-for-p2sh-the-untold-story-of-the-first-bitcoin-war) | 40 |
| [HD Wallets](https://learnmeabitcoin.com/technical/hd-wallets) | 15 |
| [Mnemonic Code Converter](https://iancoleman.io/bip39/) | x |
| [Coin Selection](https://btctranscripts.com/scalingbitcoin/tokyo-2018/edgedevplusplus/coin-selection/) | 25 |
| [An Introduction to Bitcoin Core Fee Estimation](https://bitcointechtalk.com/an-introduction-to-bitcoin-core-fee-estimation-27920880ad0) | 15 |
| [Fee Bumping and RBF](https://github.com/bitcoinops/scaling-book/blob/add_rbf/1.fee_bumping/fee_bumping.md) | 25 |
| \(_optional_\) [PSBT with Andrew Chow](https://btctranscripts.com/sf-bitcoin-meetup/2019-03-15-partially-signed-bitcoin-transactions) | 25 |
| \(_optional_\) Native Descriptor Wallets - [gist](https://gist.github.com/achow101/94d889715afd49181f8efdca1f9faa25) or [presentation](https://btctranscripts.com/advancing-bitcoin/2020/2020-02-06-andrew-chow-descriptor-wallets/) | 15 or 20 |
| [Schnorr Signatures & The Inevitability of Privacy in Bitcoin](https://medium.com/digitalassetresearch/schnorr-signatures-the-inevitability-of-privacy-in-bitcoin-b2f45a1f7287) | 20 |
| \(_optional_\) [MuSig-DN: Schnorr Multisignatures with Verifiably Deterministic Nonces](https://medium.com/blockstream/musig-dn-schnorr-multisignatures-with-verifiably-deterministic-nonces-27424b5df9d6) | 15 |
| [Taproot Explained \(_video_\)](https://www.youtube.com/watch?v=d82-MPwpiYs) | 15 |
| [Overview of the Taproot & Tapscript BIPs](https://bitcoinops.org/en/newsletters/2019/05/14/#overview-of-the-taproot--tapscript-proposed-bips) | 25 |
| [Scriptless Scripts](https://bitcoinmagazine.com/articles/scriptless-scripts-how-bitcoin-can-support-smart-contracts-without-smart-contracts) | 15 |
| \(_optional_\) [Optech Series: Preparing for Taproot](https://bitcoinops.org/en/preparing-for-taproot/) | 70 |
| \(_optional_\) [On Building Consensus and Speedy Trial](http://r6.ca/blog/20210615T191422Z.html) | 25 |

## Optional Practical Exercise

* [Taproot, sighash, timelock transaction exercises (chapters 3-5)](https://github.com/chaincodelabs/bitcoin-tx-tutorial)
* [Taproot workshop by Bitcoin Optech Group](https://bitcoinops.org/en/schorr-taproot-workshop/) \(3+ hours\)

## Discussion Questions

Answers: https://docs.google.com/document/d/1mMIF0WxJXkEckZBq23UC_j1EiQqQoCOrZedgj7_2p0Q/edit?usp=sharing

### SCRIPT

1. John Newbery talks about [verification vs. computation](https://youtu.be/np-SCwkqVy4?t=934), and he bring it up as a big reason why he thinks bitcoin can scale but is skeptical about ethereum. Is there a qualitative difference between verification and computation? And is it the fact that ethereum is capable of performing arbitrary computation that makes the whole thing difficult to scale, or is it that specifically smart contracts that require arbitrary computation won’t be able to scale \(as in those contracts would be very expensive to run\)?

#### Answer
1. Yes, there is a qualitative difference between verification and computation.
   - Verification is an action taken to compare the contents of something to some “source of truth” to determine the truthiness (including authenticity, accuracy, and integrity) of the data. To verify is to care about what is in the data.
   - Computation, on the other hand, does not necessitate or imply any of the properties of verification. The term “Garbage In, Garbage Out (GIGO)” is descriptive here. If a user writes bad code, the computer won’t verify that the code won’t fail at execution if there are runtime errors or logical errors. The only “verification” that is done by a computer is actually done by applications that run on the computer, e.g. parsers, lexers, etc. (IDEs, linters). These tools are used when writing code to ensure that the code syntax is accurate and can be parsed into lexums for compilation or interpretation (depending on the language).
   - The lack of scaling in Ethereum is focused more on the turning completeness of the smart contracting language and the complexity involved with executing arbitrary, turing complete scripts on a public blockchain. In blockchain networks, all validation nodes must run the scripts submitted to the chain by other nodes, so if the script is arbitrary, non-deterministic and turning complete, how do you prevent that script from executing infinitely? Enter the Ethereum “gas limit.”
   - Performing arbitrary computation does scale if designed properly -- bitcoin is an example of this fact. Bitcoin Script scales because of its limited feature set and deterministic execution of arbitrary scripts.


#### Notes
- Bitcoin Script
  - description: smart contract programming language for bitcoin that uses data to validate arbitrary OP code scripts on-chain
  - attributes: non-turning complete (deterministic), forth-like, reverse-polish, stack-based language
  - predicate: answers a True or False question
  - question: Does the scriptSig data satisfy the scriptPubkey conditions? i.e. Does the user spending the ouptput own that output?
  - answer: True (1) or False (0)

#### P2PKH: Practical Structure & Example
- Structure
  - scriptPubkey
    ```script
    OP_DUP OP_HASH160 <Hash160(owner_pubkey)> OP_EQUALVERIFY OP_CHECKSIG
    ```
  - scriptsig
    ```script
    <OwnerSignature> <OwnerPubkey>
    ```
- Example
  - scriptPubkey
    ```script
    OP_DUP OP_HASH160 ab68025513c3dbd2f7b92a94e0581f5d50f654e7 OP_EQUALVERIFY OP_CHECKSIG
    ```
  - scriptsig
    ```script
    3045022100884d142d86652a3f47ba4746ec719bbfbd040a570b1deccbb6498c75c4ae24cb02204b9f039ff08df09cbe9f6addac960298cad530a863ea8f53982c09db8f6e3813 0484ecc0d46f1918b30928fa0e4ed99f16a0fb4fde0735e7ade8416ab9fe423cc5412336376789d172787ec3457eee41c04f4938de5cc17b4a10fa336a8d752adf
    ```
- Stack
```
  |                     |
  |     OP_CHECKSIG     |
  |    OP_EQUALVERIFY   |
  |    ab6802551...e7   |
  |      OP_HASH160     |
  |        OP_DUP       |
  |    0484ecc0d...13   |
  |    304502210...df   |
  |_____________________|
```
- Execution
```
  |                     |
  |        OP_DUP       | <-- take this action
  |    0484ecc0d...13   | <-- on this data
  |    304502210...df   |
  |_____________________|

  |                     |
  |    0484ecc0d...13   | <-- push result of prior step onto stack
  |    0484ecc0d...13   |
  |    304502210...df   |
  |_____________________|

  |                     |
  |      OP_HASH160     | <-- take this action
  |    0484ecc0d...13   | <-- on this data
  |    0484ecc0d...13   |
  |    304502210...df   |
  |_____________________|

  |                     |
  |    ab6802551...e7   | <-- push result of prior step onto stack
  |    0484ecc0d...13   |
  |    304502210...df   |
  |_____________________|

  |                     |
  |    ab6802551...e7   | <-- push next item on stack; since it is data, take no action, continue
  |    ab6802551...e7   |
  |    0484ecc0d...13   |
  |    304502210...df   |
  |_____________________|

  |                     |
  |    OP_EQUALVERIFY   | <-- take this action
  |    ab6802551...e7   | <-- on this data
  |    ab6802551...e7   | <-- and this data; if it passes, continue; else, fail
  |    0484ecc0d...13   |
  |    304502210...df   |
  |_____________________|

  |                     |
  |     OP_CHECKSIG     | <-- take this action
  |    0484ecc0d...13   | <-- on this data
  |    304502210...df   | <-- and this data; if it passes, the script is valid; else, the script is invalid
  |_____________________|

  |                     |
  |         1           | <-- Answer to the question: Is this script valid? 1 = True = Valid!
  |_____________________|
```
### Output Descriptors

1. What is the benefit of using output descriptors?
2. Are there any use cases for p2sh-wsh-p2pkh descriptors?
3. What's about miniscript? Interactions with descriptors?

### HD Wallets

1. What is the difference between child and hardened child addresses?
2. Why is the internal chain not visible outside of the wallet if it uses public derivation?

### Coin Selection

1. Is coin age ever a consideration for coin selection?
2. Coin selection can expose a wallet by observing how the wallet selects its inputs, are there any efforts to standardize coin selection into a library of sorts so there's a standard?

### Fee Bumping and RBF

1. Is there way to ensure that a transaction will be processed? What tools are available to ensure a stuck transaction \(due to low fees\) gets processed?
2. While inconvenient, could a stuck transaction lead to a loss of funds?

### Schnorr signatures

1. How are schnorr signatures reducing a transaction's data footprint?
2. How can validation of schnorr signatures be sped up?
3. Why may schnorr signatures incentivize multi-spender transactions?
4. What makes Schnorr signatures shorter?
5. Why do schnorr signatures need a nonce?
6. What is the risk of nonce-generation on a limited-entropy device like a hardware wallet? How can that risk be overcome with deterministic nonce generation?

### Taproot

1. What makes Pay to Taproot more private than previous output formats?
2. What are the difficulties and benefits of switching to Pay to Taproot addresses?
3. Why does tapscript not support OP\_CHECKMULTISIG?
4. What is the purpose of TaggedHashes?

### \(_optional_\) The softfork bundle

1. Would it be possible to implement Taproot without schnorr signatures or schnorr outputs without Taproot?
2. How did the Bitcoin network settle on using Speedy Trial to activate Taproot?

### \(_optional_\) Native segwit output and bech32 addresses

1. What's the difference between "native segwit" and "bech32\(m\)"?
2. Should wallets allow sending to bech32m addresses?

