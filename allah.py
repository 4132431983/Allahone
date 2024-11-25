import os
import subprocess

def get_wallet_file():
    # Get the current directory
    current_directory = os.getcwd()
    # List all files in the current directory
    files = os.listdir(current_directory)
    # Filter for wallet.dat file
    wallet_files = [f for f in files if f == 'wallet.dat']
    
    if wallet_files:
        return os.path.join(current_directory, 'wallet.dat')
    else:
        raise FileNotFoundError("wallet.dat not found in the current directory.")

def transfer_bitcoin(wallet_file, recipient_address, amount):
    # Command to transfer Bitcoin using bitcoin-cli
    command = f'bitcoin-cli -datadir={os.path.dirname(wallet_file)} sendtoaddress {recipient_address} {amount}'
    try:
        # Execute the command
        result = subprocess.check_output(command, shell=True)
        print(f'Transaction successful! Transaction ID: {result.decode().strip()}')
    except subprocess.CalledProcessError as e:
        print(f'An error occurred: {e.output.decode().strip()}')

def main():
    try:
        wallet_file = get_wallet_file()
        recipient_address = input("Enter the recipient's Bitcoin address: ")
        amount = float(input("Enter the amount of BTC to send: "))
        
        transfer_bitcoin(wallet_file, recipient_address, amount)
    except Exception as e:
        print(f'Error: {str(e)}')

if name == "__main__":
    main()