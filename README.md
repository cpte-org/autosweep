# autosweep
autosweep is a Python script that automatically sweeps the balance of an Ethereum account to a specified recipient address at regular intervals. The script uses the web3 library to interact with an Ethereum node and send transactions.

Usage
To use autosweep, follow these steps:

1- Clone the repository:

`git clone https://github.com/cpte-org/autosweep.git`

2- Install the required Python libraries:

`pip install -r requirements.txt`

3- Create a file named .env in the root directory of the repository with the following contents:

`
RPC_ENDPOINT=<your Ethereum RPC endpoint (e.g., https://mainnet.infura.io/v3/your-project-id)>
PRIV_KEY=<your account private key>
RCVING_ADDR=<the recipient address>
`
Replace your_project_id, your_private_key, and recipient_address with your own values.
Note: Example Ethereum RPC endpoint is infura.


4- Run the script using the following command:

`./watchdog.sh`

This script starts the main.py script and monitors its output. If the script stops producing output or encounters an error, the watchdog.sh script restarts it.

Files

- watchdog.sh
This is a Bash script that monitors the main.py script and restarts it if necessary. It also sets the path to the Python script, the log file path, and the maximum idle time.

- main.py
This is the Python script that monitors the Ethereum account balance and sends a transaction to the recipient address when the balance exceeds a specified threshold. It uses the web3 library to interact with the Ethereum network and the dotenv library to read the environment variables from the .env file. The script is configured to run every 20 seconds, but this can be changed by modifying the time.sleep() statement at the end of the script.

License
This project is licensed under the chat-GPT v3.5 License.
