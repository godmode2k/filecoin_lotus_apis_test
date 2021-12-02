# coding: utf-8

# Filecoin miner's block reward test
# hjkim, 2021.11.01


import urllib.request
from urllib.parse import urlparse
from pathlib import Path
import json
import time
import sys
import socket
import traceback



DAEMON_URL = "http://127.0.0.1:1234/rpc/v0"
DAEMON_TOKEN = "<token>"



# Request daemon API Source-based:
# https://github.com/s0nik42/lotus-farcaster/blob/main/lotus-exporter-farcaster/lotus-exporter-farcaster.py
# -----------------------------------
def daemon_get_json(method, params):
    """Request daemon api"""
    return get_json(DAEMON_URL, DAEMON_TOKEN, method, params)

def get_json(url, token, method, params):
    """standard request api function"""
    jsondata = json.dumps({"jsonrpc": "2.0", "method": "Filecoin." + method, "params": params, "id": 3}).encode("utf8")
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Bearer ' + token)
    req.add_header("Content-Type", "application/json")

    try:
        response = urllib.request.urlopen(req, jsondata)
    except urllib.error.URLError as e_url:
        print(f'ERROR accessing { url } : { e_url.reason }', file=sys.stderr)
        print(f'DEBUG: method { method } / params { params } ', file=sys.stderr)
        print('lotus_scrape_execution_succeed { } 0')
        sys.exit(0)

    try:
        res = response.read()
        page = res.decode("utf8")

        # parse json object
        obj = json.loads(page)
    except Exception as e_generic:
        print(f'ERROR parsing URL response : { e_generic }', file=sys.stderr)
        print(f'DEBUG: method { method } / params { params } ', file=sys.stderr)
        print(f'DEBUG: { page } ', file=sys.stderr)
        print('lotus_scrape_execution_succeed { } 0')
        sys.exit(0)

    # output some object attributes
    return obj

def bitfield_count(bitfield):
    """Count bits from golang Bitfield object.
    s0nik42 reverse engineering
    https://github.com/filecoin-project/go-bitfield/blob/master/rle/rleplus.go#L88"""

    count = 0
    if len(bitfield) < 2:
        return 0
    for i in range(0, len(bitfield), 2):
        count += bitfield[i+1]
        return count

def printj(parsed):
    """JSON PRETTY PRINT"""
    print(json.dumps(parsed, indent=4, sort_keys=True))
# -----------------------------------



# -----------------------------------



def test_calc_miner_reward(block_height):
    # Filecoin.ChainGetTipSetByHeight
    res = daemon_get_json( "ChainGetTipSetByHeight", [block_height, []] )
    block_cid_list = []
    i = 0
    for data in res["result"]["Cids"]:
        block_cid = {}
        block_cid["Cid"] = data
        block_cid["Miner"] = res["result"]["Blocks"][i]["Miner"]
        block_cid["Parent"] = res["result"]["Blocks"][i]["Parents"]
        block_cid["ParentCount"] = len( res["result"]["Blocks"][i]["Parents"] )
        block_cid_list.append( block_cid )
        i += 1


    # Filecoin.StateVMCirculatingSupplyInternal
    # Current block: (block height)
    i = 0
    for block_cid in block_cid_list:
        res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[block_cid["Cid"]]] )
        block_cid["FilMined"] = res["result"]["FilMined"]
        i += 1


    # Filecoin.StateVMCirculatingSupplyInternal
    # Parent block: (block height - 1)
    i = 0
    for block_cid in block_cid_list:
        # why parent[0], not parent[0..x] ?
        # maybe it's okay even if has several parents
        # due to same values (FilMined, etc.) each other.
        res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[block_cid["Parent"][0]]] )
        block_cid["ParentFilMined"] = res["result"]["FilMined"]
        i += 1


    # Filecoin.StateCompute
    # current block cid
    i = 0
    for block_cid in block_cid_list:
        res = daemon_get_json( "StateCompute", [block_height, [], [block_cid["Cid"]]] )
        val_miner_tip = 0
        val_miner_penalty = 0
        val_miner_tip_fil = 0
        val_miner_penalty_fil = 0
        for data in res["result"]["Trace"]:
            val_miner_tip += int(data["GasCost"]["MinerTip"])
            val_miner_penalty += int(data["GasCost"]["MinerPenalty"])

        val_miner_tip_fil = val_miner_tip / 1000000000000000000
        val_miner_penalty_fil = val_miner_penalty / 1000000000000000000
        print( "total miner penalty  = " + str(val_miner_penalty) + ", " + str(val_miner_penalty_fil) + " FIL" )

        res_reward_info = {}
        res_reward_info["MinerTip"] = val_miner_tip
        res_reward_info["MinerTipFil"] = val_miner_tip_fil
        block_cid["MinerReward"] = res_reward_info


    # calculation
    #
    # (FilMined (current) - FilMined (parents[0])) / len(parents)
    #res_filmined = int(0)
    #
    # fee reward for messages (transactions)
    #res_miner_fee_reward
    #res_miner_fee_reward_fil
    #
    # total: miner reward
    #res_miner_reward = int(int(res_filmined) + int(res_miner_fee_reward))
    #res_miner_reward_fil = (res_miner_reward / 1000000000000000000)
    #res_miner_reward_info = "" +
    #    res_miner_reward_fil +
    #    " FIL ( " +
    #    res_filmined +
    #    " FIL Block Reward and " +
    #    res_miner_fee_reward_fil + " FIL Fee Reward )"
    i = 0
    for block_cid in block_cid_list:
        # (FilMined (current) - FilMined (parents[0])) / len(parents)
        res_filmined = int(block_cid["FilMined"]) - int(block_cid["ParentFilMined"])
        res_filmined = int( res_filmined / int(block_cid["ParentCount"]) )
        res_filmined_fil = res_filmined / 1000000000000000000

        # fee reward for messages (transactions)
        res_miner_fee_reward = int(block_cid["MinerReward"]["MinerTip"])
        res_miner_fee_reward_fil = block_cid["MinerReward"]["MinerTipFil"]

        # total: miner reward
        res_miner_reward = int(int(res_filmined) + int(res_miner_fee_reward))
        res_miner_reward_fil = res_miner_reward / 1000000000000000000
        res_miner_reward_info = "" + \
             str(res_miner_reward_fil) + \
             " FIL ( " + \
             str(res_filmined_fil) + \
             " FIL Block Reward and " + \
             str(res_miner_fee_reward_fil) + " FIL Fee Reward )"
        print( res_miner_reward_info )
        block_cid["MinerReward"]["MinerReward"] = res_miner_reward
        block_cid["MinerReward"]["MinerRewardFil"] = res_miner_reward_fil
        block_cid["MinerReward"]["BlockReward"] = res_filmined
        block_cid["MinerReward"]["BlockRewardFil"] = res_filmined_fil
        block_cid["MinerReward"]["result_str"] = res_miner_reward_info


    print( "result" )
    print( "-----------------------------" )
    result = []
    i = 0
    for block_cid in block_cid_list:
        miner = block_cid["Miner"]

        reward = block_cid["MinerReward"]["MinerReward"]
        reward_fil = block_cid["MinerReward"]["MinerRewardFil"]

        block_reward = block_cid["MinerReward"]["BlockReward"]
        block_reward_fil = block_cid["MinerReward"]["BlockRewardFil"]

        fee_reward = block_cid["MinerReward"]["MinerTip"]
        fee_reward_fil = block_cid["MinerReward"]["MinerTipFil"]

        miner_reward_info = block_cid["MinerReward"]["result_str"]

        result.append( {
            "tipset_height": str(block_height),
            "block_cid": str(block_cid["Cid"]["/"]),
            "miner": miner,
            "reward_fil": str(reward_fil),
            "reward": str(reward),
            "block_reward_fil": str(block_reward_fil),
            "block_reward": str(block_reward),
            "fee_reward_fil": str(fee_reward_fil),
            "fee_reward": str(fee_reward),
            "result_str": str(miner_reward_info)
        })

        print( f'[{i}] ' + str(block_height) + ", " + \
            miner + ", " + \
            str(reward_fil) + " (" + str(reward) + "), " + \
            str(block_reward_fil) + " (" + str(block_reward) + "), " + \
            str(fee_reward_fil) + "(" + str(fee_reward) + ")" )
        i += 1

    return result


# RUN
#block_height = 1239140 # 1 parent
block_height = 1256900 # parents
test_calc_miner_reward( block_height )


