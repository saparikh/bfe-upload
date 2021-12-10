# required imports and default settings
import pandas as pd
from pybfe.client.session import Session
import os

try:
    from dotenv import load_dotenv
    from pathlib import Path
    env_path = Path('.') / 'env_vars'
    load_dotenv(dotenv_path=env_path)
except:
    print("No env file specified, relying on env settings")

pd.set_option("display.width", 300)
pd.set_option("display.max_rows", 1000)
pd.set_option("display.max_colwidth", -1)
pd.set_option("display.max_columns", 20)

NETWORK = os.environ.get("INPUT_NETWORK_NAME")
BF_HOST = os.environ.get("INPUT_SERVER_NAME")
BF_PORT = os.environ.get("INPUT_SERVER_PORT")
BF_SNAPSHOT_DIR = os.environ.get("INPUT_SNAPSHOT_FOLDER")

BF_SNAPSHOT = os.environ.get("INPUT_SNAPSHOT_NAME")
if len(BF_SNAPSHOT) == 0:
    BF_SNAPSHOT = os.environ.get("GITHUB_SHA", "error")

if BF_SNAPSHOT == "error":
    print("Unable to retrieve snapshot name")
    exit(1)

BF_INIT_SNAPSHOT = os.environ.get("INPUT_INIT_SNAPSHOT", "yes")

bf = Session.get('bfe', host=BF_HOST, ssl=True, port=BF_PORT)
bf.set_network(NETWORK)

ss_list = bf.list_snapshots()

if BF_INIT_SNAPSHOT == "yes":
    if len(ss_list) >= 1 and BF_SNAPSHOT in ss_list:
        print("Re-using already initialized snapshot, ignoring BF_INIT_SNAPSHOT = yes setting")
        cur_ss = bf.set_snapshot(BF_SNAPSHOT)
    else:
        cur_ss = bf.init_snapshot(BF_SNAPSHOT_DIR, BF_SNAPSHOT)
        print(f"Initializing new snapshot {BF_SNAPSHOT}")
else:
    cur_ss = bf.list_snapshots()[0]

exit(0)
