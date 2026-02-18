# Blockchain and Web3 Integration Guide

## Purpose

This guide covers integrating blockchain technologies, smart contracts, NFTs, DeFi protocols, and wallet interactions with n8n workflows for enterprise automation.

## Overview

Blockchain integration enables automation of decentralized transactions, smart contract interactions, and Web3 operations. n8n can connect to blockchain networks via RPC endpoints, integrate with wallet services, and automate DeFi workflows.

## Blockchain Fundamentals

### Key Concepts

- **Blockchain** — Distributed ledger of immutable transactions
- **Smart Contracts** — Self-executing code on blockchain
- **RPC Endpoint** — HTTP/WebSocket interface to interact with blockchain
- **Wallet** — Address holding cryptocurrency or NFTs
- **Gas** — Fee required to execute transactions
- **Mainnet vs Testnet** — Production vs testing environments

### Major Blockchains for Business

- **Ethereum** — Smart contracts, DeFi, largest ecosystem
- **Polygon** — Ethereum sidechain, lower fees
- **Binance Smart Chain** — High throughput, lower cost
- **Solana** — High speed, low latency
- **Hyperledger Fabric** — Enterprise permissioned blockchain

## Connecting to Blockchains

### Using HTTP RPC Endpoints

Connect to blockchain via HTTP requests:

```javascript
// n8n HTTP Request node
{
  "url": "https://mainnet.infura.io/v3/YOUR_PROJECT_ID",
  "method": "POST",
  "body": {
    "jsonrpc": "2.0",
    "method": "eth_blockNumber",
    "params": [],
    "id": 1
  }
}
```

### RPC Providers

- **Infura** — Ethereum, Polygon, Arbitrum
- **Alchemy** — Multiple chains, enhanced APIs
- **QuickNode** — High-performance endpoints
- **Ankr** — Decentralized RPC infrastructure

### Node Libraries

Use web3.js or ethers.js via n8n Code nodes:

```javascript
// Using ethers.js in n8n Code node
const ethers = require('ethers');

const provider = new ethers.providers.JsonRpcProvider(
  'https://mainnet.infura.io/v3/PROJECT_ID'
);

const balance = await provider.getBalance('0x...');
return { balance: ethers.utils.formatEther(balance) };
```

## Smart Contract Interaction

### Reading Contract Data

```javascript
// n8n HTTP Request - call contract function
{
  "url": "https://mainnet.infura.io/v3/YOUR_KEY",
  "method": "POST",
  "body": {
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [
      {
        "to": "0xContractAddress",
        "data": "0x..." // Encoded function call
      },
      "latest"
    ],
    "id": 1
  }
}
```

### Writing to Contracts (Transactions)

```
[Decision to execute transaction]
  ↓
[Create transaction object]
  ├→ To: contract address
  ├→ Function: execute action
  ├→ Parameters: function arguments
  └→ Gas limit: estimate gas needed
  ↓
[Sign transaction]
  ├→ Using private key
  ├→ Calculate gas price
  └→ Set nonce
  ↓
[Broadcast to network]
  ↓
[Monitor transaction]
  ├→ Wait for confirmation
  ├→ Check for errors
  └→ Log transaction hash
```

## NFT Integration

### NFT Minting

Automate NFT creation workflow:

```
[Event triggers NFT creation]
  ↓
[Prepare metadata]
  ├→ Name, description
  ├→ Image URI
  └→ Attributes (traits)
  ↓
[Upload to IPFS or storage]
  ↓
[Create metadata JSON]
  ↓
[Call NFT contract mint function]
  ↓
[Log token ID and transaction hash]
```

### NFT Marketplace Integration

```
[Monitor NFT listing on marketplace]
  ↓
[On purchase event]
  ├→ Verify buyer credentials
  ├→ Transfer NFT
  └→ Record transaction
  ↓
[Update inventory]
  ├→ Mark as sold
  ├→ Update royalties
  └→ Notify seller
```

### Popular NFT Standards

- **ERC-721** — Unique NFTs, one token per address
- **ERC-1155** — Multiple types, supports fungible and non-fungible
- **ERC-4626** — Tokenized vaults

## DeFi Integration

### Token Swaps

Automate token exchanges on decentralized exchanges:

```
[Monitor token prices]
  ↓
[If price reaches target]
  ├→ Check wallet balance
  ├→ Estimate swap output
  └→ Set slippage tolerance
  ↓
[Execute swap]
  ├→ Approve token spend (if needed)
  └→ Call DEX contract
  ↓
[Monitor swap completion]
  ├→ Verify token received
  └→ Log swap details
```

### Lending Protocols

```
[Monitor borrow rates]
  ↓
[When rate favorable]
  ├→ Check collateral ratio
  ├→ Calculate borrowing power
  └→ Verify loan parameters
  ↓
[Execute borrow]
  ├→ Deposit collateral
  └→ Receive borrowed tokens
  ↓
[Monitor loan health]
  ├→ Track liquidation risk
  └→ Alert if near threshold
```

### Staking

```
[Monitor staking rewards]
  ↓
[If APY meets target]
  ├→ Approve tokens
  ├→ Check minimum stake
  └→ Calculate fees
  ↓
[Execute staking]
  ├→ Lock tokens
  └→ Begin earning rewards
  ↓
[Claim rewards periodically]
  ├→ Harvest APY
  └→ Reinvest or withdraw
```

## Wallet Integration

### Wallet Types

- **Hot Wallets** — Private key stored in environment
  - MetaMask, WalletConnect
  - Higher risk, higher automation

- **Cold Wallets** — Private key offline
  - Hardware wallets, multisig
  - Lower risk, requires manual signing

- **Smart Contract Wallets** — Account abstraction
  - Safe (formerly Gnosis Safe)
  - Batch operations, custom logic

### Signing Transactions

```javascript
// Sign transaction with private key (Development only)
// NEVER use in production - use hardware wallet or service instead
const ethers = require('ethers');

const privateKey = $credentials.wallet_private_key;
const wallet = new ethers.Wallet(privateKey, provider);

const tx = {
  to: '0xRecipient',
  value: ethers.utils.parseEther('1.0')
};

const signedTx = await wallet.signTransaction(tx);
await provider.sendTransaction(signedTx);
```

### Better: Use Wallet Service

```javascript
// Use professional wallet service (Fireblocks, Custody)
{
  "method": "POST",
  "url": "https://api.fireblocks.io/v1/vault/accounts/0/wallets/0/transactions",
  "headers": {
    "Authorization": "Bearer ${{ $credentials.fireblocks_api_key }}"
  },
  "body": {
    "operation": "TRANSFER",
    "assetId": "ETH",
    "amount": "1.0",
    "destination": "0xRecipient"
  }
}
```

## Transaction Monitoring

### Monitor Incoming Transactions

```
[Listen to blockchain events]
  ↓
[Filter for relevant transactions]
  ├→ To address: our wallet
  ├→ Token: specific ERC-20
  └→ Amount: minimum threshold
  ↓
[Execute action]
  ├→ Update database
  ├→ Send notification
  └→ Trigger workflow
```

### Monitor Gas Prices

```javascript
// Monitor gas prices and execute when optimal
async function waitForOptimalGasPrice() {
  const currentGas = await provider.getGasPrice();
  const maxGasPrice = ethers.utils.parseUnits('100', 'gwei');

  if (currentGas.lt(maxGasPrice)) {
    return true;  // Execute transaction now
  } else {
    return false; // Wait for better gas prices
  }
}
```

## Enterprise Considerations

### Compliance

- KYC/AML checks before transactions
- Regulatory reporting (transaction details)
- Audit trails for all on-chain activity
- Governance approvals for large transactions

### Security

1. **Private Key Management**
   - Use hardware wallets for large amounts
   - Never embed private keys in code
   - Rotate keys regularly

2. **Transaction Signing**
   - Multisig approval for significant transactions
   - Time locks for major operations
   - Emergency pause mechanism

3. **Smart Contract Audits**
   - Professional security audits before deployment
   - Formal verification for critical contracts
   - Test on testnet before mainnet

4. **Rate Limiting**
   - Limit transaction frequency
   - Cap transaction size
   - Monitor for unusual patterns

## Workflow Example: Automated Staking

```
[Cron trigger daily]
  ↓
[Check staking rewards]
  Get current APY and rewards accrued
  ↓
[Claim rewards]
  Call staking contract claim function
  ↓
[Decide to reinvest]
  If APY > threshold: reinvest rewards
  ↓
[Execute reinvestment]
  ├→ Approve tokens
  └→ Call stake function
  ↓
[Log transaction]
  Store hash and amount in database
```

## Popular Blockchain Tools

- **Etherscan** — Blockchain explorer, contract verification
- **OpenZeppelin** — Smart contract libraries, tools
- **Truffle Suite** — Development framework
- **Hardhat** — Ethereum development environment
- **Chainlink** — Oracles for external data

## Best Practices

### 1. Testing

- Always test on testnet first
- Use testnet tokens and faucets
- Verify contract behavior before mainnet
- Load test high-volume workflows

### 2. Error Handling

- Handle insufficient gas scenarios
- Manage slippage tolerance for swaps
- Deal with network congestion
- Retry failed transactions with backoff

### 3. Monitoring

- Track all transaction status
- Monitor wallet balances
- Alert on failed transactions
- Log gas spending

### 4. Security

- Use professional wallet services
- Never hardcode private keys
- Implement multisig for critical operations
- Regular security audits

## Related Documentation

- [Security Best Practices](../security-best-practices.md) — Blockchain security
- [Deployment Guide](../deployment-guide.md) — Production blockchain workflows
- [Contributing Guide](../contributing.md) — Blockchain workflow standards
