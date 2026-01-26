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

def fetch_portfolio():
    w3 = Web3(Web3.HTTPProvider(BASE_RPC))
    if not w3.is_connected():
        print("Error: Could not connect to Base RPC")
        return

    try:
        address = Web3.to_checksum_address(WALLET_ADDRESS)
    except ValueError:
        print(f"Invalid address format: {WALLET_ADDRESS}")
        return

    portfolio = {"wallet": {}, "aave": {}}

    # print("Fetching Wallet Balances...")
    for symbol, contract_address in TOKENS.items():
        try:
            c_addr = Web3.to_checksum_address(contract_address)
            contract = w3.eth.contract(address=c_addr, abi=ERC20_ABI)
            balance_raw = contract.functions.balanceOf(address).call()
            # Try to get decimals, default to 18 if fail
            try:
                decimals = contract.functions.decimals().call()
            except:
                decimals = 18
            
            balance = balance_raw / (10 ** decimals)
            portfolio["wallet"][symbol] = balance
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    # print("Fetching Aave Data...")
    try:
        pool_contract = w3.eth.contract(address=AAVE_POOL_ADDRESS, abi=AAVE_POOL_ABI)
        user_data = pool_contract.functions.getUserAccountData(address).call()
        # Aave returns values in USD (8 decimals)
        portfolio["aave"]["total_collateral_usd"] = user_data[0] / 1e8
        portfolio["aave"]["total_debt_usd"] = user_data[1] / 1e8
        # Health Factor is 18 decimals
        hf = user_data[5] / 1e18
        # If HF is max uint256, it's infinite (user has no debt)
        if hf > 1000000:
            portfolio["aave"]["health_factor"] = "Infinity"
        else:
            portfolio["aave"]["health_factor"] = hf
            
    except Exception as e:
        print(f"Error fetching Aave data: {e}")
        # traceback.print_exc()

    return portfolio

if __name__ == "__main__":
    data = fetch_portfolio()
    print(json.dumps(data, indent=2))
