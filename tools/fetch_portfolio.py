import os
import json
import traceback
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
BASE_RPC = "https://mainnet.base.org"
# Ensure checksum
try:
    AAVE_POOL_ADDRESS = Web3.to_checksum_address("0xA238Dd80C259a72e81d7e4664a9801593F98D1c5")
except:
    AAVE_POOL_ADDRESS = "0xA238Dd80C259a72e81d7e4664a9801593F98D1c5"

AAVE_POOL_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
        "name": "getUserAccountData",
        "outputs": [
            {"internalType": "uint256", "name": "totalCollateralBase", "type": "uint256"},
            {"internalType": "uint256", "name": "totalDebtBase", "type": "uint256"},
            {"internalType": "uint256", "name": "availableBorrowsBase", "type": "uint256"},
            {"internalType": "uint256", "name": "currentLiquidationThreshold", "type": "uint256"},
            {"internalType": "uint256", "name": "ltv", "type": "uint256"},
            {"internalType": "uint256", "name": "healthFactor", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

TOKENS = {
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "cbBTC": "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",
    "WETH": "0x4200000000000000000000000000000000000006"
}

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

# RPC List for Redundancy (Cloud IPs often get blocked by the main one)
RPC_LIST = [
    "https://base.llamarpc.com",
    "https://base-mainnet.public.blastapi.io", 
    "https://mainnet.base.org",
    "https://1rpc.io/base"
]

def fetch_portfolio():
    portfolio = None
    
    # Try each RPC until one works
    for rpc_url in RPC_LIST:
        try:
            # print(f"Connecting to {rpc_url}...")
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 5}))
            
            if not w3.is_connected():
                continue
                
            address = Web3.to_checksum_address(WALLET_ADDRESS)
            
            # Temporary storage for this attempt
            temp_portfolio = {"wallet": {}, "aave": {}}
            success_tokens = 0
            
            # Fetch Wallet Balances
            for symbol, contract_address in TOKENS.items():
                c_addr = Web3.to_checksum_address(contract_address)
                contract = w3.eth.contract(address=c_addr, abi=ERC20_ABI)
                balance_raw = contract.functions.balanceOf(address).call()
                
                # Decimals
                try:
                    decimals = contract.functions.decimals().call()
                except:
                    decimals = 18
                
                temp_portfolio["wallet"][symbol] = balance_raw / (10 ** decimals)
                success_tokens += 1
            
            if success_tokens == 0:
                raise Exception("No tokens fetched")

            # Fetch Aave (Optional - Don't fail entire call if Aave fails)
            try:
                pool_contract = w3.eth.contract(address=AAVE_POOL_ADDRESS, abi=AAVE_POOL_ABI)
                user_data = pool_contract.functions.getUserAccountData(address).call()
                temp_portfolio["aave"]["total_collateral_usd"] = user_data[0] / 1e8
                temp_portfolio["aave"]["total_debt_usd"] = user_data[1] / 1e8
                hf = user_data[5] / 1e18
                temp_portfolio["aave"]["health_factor"] = "Infinity" if hf > 1000000 else hf
            except:
                pass # Aave failure is acceptable

            # If we got here, we have valid data
            portfolio = temp_portfolio
            break # Exit loop, we are good
            
        except Exception as e:
            print(f"RPC {rpc_url} failed: {e}")
            continue

    return portfolio

if __name__ == "__main__":
    data = fetch_portfolio()
    print(json.dumps(data, indent=2))
