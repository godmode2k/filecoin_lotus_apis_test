#!/usr/bin/python3
# -*- coding: utf-8 -*-



# -------------------------------------------------------------------
# Purpose: Filecoin Lotus APIs test (Miner rewards: block, fee)
# Author: Ho-Jung Kim (godmode2k@hotmail.com)
# Filename: lotus_apis_miner_reward_test.py
# Date: Since November 1, 2021
#
#
# Reference:
# - https://docs.filecoin.io/reference/lotus-api/
# - https://github.com/filecoin-project/lotus/blob/master/api/api_full.go
#
#
# Note:
# - Environment: Mainnet
# - Mainnet: USE THIS AT YOUR OWN RISK
#
#
# License:
#
#*
#* Copyright (C) 2021 Ho-Jung Kim (godmode2k@hotmail.com)
#*
#* Licensed under the Apache License, Version 2.0 (the "License");
#* you may not use this file except in compliance with the License.
#* You may obtain a copy of the License at
#*
#*      http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software
#* distributed under the License is distributed on an "AS IS" BASIS,
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#* See the License for the specific language governing permissions and
#* limitations under the License.
#*
# -------------------------------------------------------------------



# Request daemon API Source-based:
# https://github.com/s0nik42/lotus-farcaster/blob/main/lotus-exporter-farcaster/lotus-exporter-farcaster.py
# ------------------------------------------------------------------------
import urllib.request
from urllib.parse import urlparse
from pathlib import Path
import json
import time
import sys
import socket

import base64

#
# CONFIG VARIABLES // OPTIONAL THEY ARE NORMALLY AUTODETECTED
#
# Example : MINER_URL = "http://127.0.0.1:2345/rpc/v0"
MINER_URL = ""
# MINER_TOKEN is the content of the ~/.lotusminer/token file
MINER_TOKEN = ""
DAEMON_URL = ""
DAEMON_TOKEN = ""

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

    # Check if the answer contain results / otherwize quit
    if "result" not in obj.keys():
        print(f'ERROR { url } returned no result', file=sys.stderr)
        print(f'DEBUG: method { method } / params { params } ', file=sys.stderr)
        print(f'DEBUG: { obj } ', file=sys.stderr)

        # inform the dashboard execution failed
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



# ------------------------------------------------------------------------



def test_calc_miner_reward_test():
    global DAEMON_URL
    global DAEMON_TOKEN

    if DAEMON_URL == '':
        with open(str(Path.home()) + "/.lotus/api", "r") as text_file:
            daemon_api_line = text_file.read()
        daemon_api = daemon_api_line.split("/")
        daemon_api_ip = daemon_api[2]
        daemon_api_port = daemon_api[4]
        DAEMON_URL = "http://" + daemon_api_ip + ":" + daemon_api_port + "/rpc/v0"

    if DAEMON_TOKEN == '':
        with open(str(Path.home()) + "/.lotus/token", "r") as text_file:
            DAEMON_TOKEN = text_file.read()

    # Filecoin.ChainGetTipSetByHeight
    # curl -X POST -H "Authorization: Bearer $(cat ./token)" -d '{"method": "Filecoin.ChainGetTipSetByHeight", "params": [1239003, []], "id": 0}' http://127.0.0.1:1234/rpc/v0
    #
    #block_height = 1239003
    #res = daemon_get_json( "ChainGetTipSetByHeight", [block_height, []] )
    #block_cid_list = []
    #print( res )

    # ---------- {
    #'''
    #block_height = 1239003 # 1 parent
    #block_height = 1256880 # parents
    #block_height = 1239140 # 1 parent
    block_height = 1256900 # parents

    res = daemon_get_json( "ChainGetTipSetByHeight", [block_height, []] )
    #print( res )

    block_cid = res["result"]["Cids"][0]
    miner = res["result"]["Blocks"][0]["Miner"]
    parent_block_cid_list = res["result"]["Blocks"][0]["Parents"]

    #print( parent_block_cid_list )
    print( "miner = " + miner )

    i = 0
    for data in parent_block_cid_list:
        #print( f'[{i}] ' + miner + ", " + data["/"] )
        print( data )

        i += 1
    #'''
    # ---------- }



    # Filecoin.StateVMCirculatingSupplyInternal
    # Current block: (block height)
    #curl -X POST -H "Authorization: Bearer $(cat ./token)" -d '{"method": "Filecoin.StateVMCirculatingSupplyInternal", "params": [[{"/": "<current block cid>"}]], "id": 0}' http://127.0.0.1:1234/rpc/v0
    #
    #current_block_cid = {}
    #current_block_cid["/"] = "<current block cid>"
    #res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[current_block_cid]] )
    #print( res )
    #print( "FilVested: " + res["result"]["FilVested"] ) 
    #print( "FilMined: " + res["result"]["FilMined"] )
    #print( "FilBurnt: " + res["result"]["FilBurnt"] )
    #print( "FilLocked: " + res["result"]["FilLocked"] )
    #print( "FilCirculating: " + res["result"]["FilCirculating"] )
    #print( "FilReserveDisbursed: " + res["result"]["FilReserveDisbursed"] )

    # ---------- {
    res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[block_cid]] )
    FilMined = res["result"]["FilMined"]
    print( res )
    print ( "FilMined: " + str(FilMined) )
    # ---------- }



    # Filecoin.StateVMCirculatingSupplyInternal
    # Parent block: (block height - 1)
    # curl -X POST -H "Authorization: Bearer $(cat ./token)" -d '{"method": "Filecoin.StateVMCirculatingSupplyInternal", "params": [[{"/": "<parent block cid>"}]], "id": 0}' http://127.0.0.1:1234/rpc/v0
    #
    #parent_block_cid = {}
    #parent_block_cid["/"] = "<parent block cid>"
    #res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[parent_block_cid]] )
    #print( res )
    #print( "FilVested: " + res["result"]["FilVested"] ) 
    #print( "FilMined: " + res["result"]["FilMined"] )
    #print( "FilBurnt: " + res["result"]["FilBurnt"] )
    #print( "FilLocked: " + res["result"]["FilLocked"] )
    #print( "FilCirculating: " + res["result"]["FilCirculating"] )
    #print( "FilReserveDisbursed: " + res["result"]["FilReserveDisbursed"] )

    # ---------- {
    i = 0
    parent_FilMined_list = []
    for parent_cid in parent_block_cid_list:
        print( parent_cid )
        res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[parent_cid]] )
        #print( f'[{i}] {res}' )
        filmined = res["result"]["FilMined"]
        parent_FilMined_list.append( filmined )

        print( f'[{i}] ' + "parent FilMined: " + str(filmined) )

        i += 1
    # ---------- }



    # Filecoin.StateCompute
    # current block cid
    # curl -X POST -H "Authorization: Bearer $(cat ./token)" -d '{"method": "Filecoin.StateCompute", "params": [1239003, [], [{"/": "<current block cid>"}]], "id": 0}' http://127.0.0.1:1234/rpc/v0
    #
    #block_height = 1239003
    #block_cid = {}
    #block_cid["/"] = "<current block cid>"
    #res = daemon_get_json( "StateCompute", [block_height, [], [block_cid]] )
    #print( res )

    # ---------- {
    res = daemon_get_json( "StateCompute", [block_height, [], [block_cid]] )

    val_miner_tip = 0
    #val_total_cost = 0
    #val_refund = 0
    val_miner_penalty = 0
    val_miner_tip_fil = 0
    #val_total_cost_fil = 0
    #val_refund_fil = 0
    val_miner_penalty_fil = 0
    for data in res["result"]["Trace"]:
        #print( "BaseFeeBurn = " + data["GasCost"]["BaseFeeBurn"] )
        #print( "OverEstimationBurn = " + data["GasCost"]["OverEstimationBurn"] )
        #print( "MinerTip = " + data["GasCost"]["MinerTip"] )

        #print( '{"BaseFeeBurn": "' + data["GasCost"]["BaseFeeBurn"] + '", ' +
        #       '"OverEstimationBurn": "' + data["GasCost"]["OverEstimationBurn"] + '", ' +
        #       '"MinerTip": "' + data["GasCost"]["MinerTip"] + '"}' )

        #val_fil += int(data["GasCost"]["MinerTip"]) / 1000000000000000000

        val_miner_tip += int(data["GasCost"]["MinerTip"])
        #val_total_cost += int(data["GasCost"]["TotalCost"])
        #val_refund += int(data["GasCost"]["Refund"])
        val_miner_penalty += int(data["GasCost"]["MinerPenalty"])

    val_miner_tip_fil = val_miner_tip / 1000000000000000000
    #val_total_cost_fil = val_total_cost / 1000000000000000000
    #val_refund_fil = val_refund / 1000000000000000000
    val_miner_penalty_fil = val_miner_penalty / 1000000000000000000

    print( "total miner tip  = " + str(val_miner_tip) + ", " + str(val_miner_tip_fil) + " FIL" )
    #print( "total total cost = " + str(val_total_cost) + ", " + str(val_total_cost_fil) + " FIL"  )
    #print( "total refund     = " + str(val_refund) + ", " + str(val_refund_fil) + " FIL"  )
    print( "total miner penalty  = " + str(val_miner_penalty) + ", " + str(val_miner_penalty_fil) + " FIL" )

    # ---------- }



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
    #res_miner_reward = int(int(res_filmined) - int(res_miner_fee_reward))
    #res_miner_reward_fil = (res_miner_reward / 1000000000000000000)
    #res_miner_reward_info = "" +
    #    res_miner_reward_fil +
    #    " FIL ( " +
    #    res_filmined +
    #    " FIL Block Reward and " +
    #    res_miner_fee_reward_fil + " FIL Fee Reward )"

    # ---------- {

    # //! FIXME
    # FilMined (current) - FilMined (parent)
    #for i in range(0, len(parent_FilMined_list) - 1):
    #    res_filmined = int(parent_FilMined_list[i+1]) - int(parent_FilMined_list[i])
    res_filmined = int(parent_FilMined_list[0])

    res_filmined = int((int(FilMined) - int(res_filmined)) / len(parent_FilMined_list))
    res_filmined_fil = res_filmined / 1000000000000000000

    print( "filmined = " + str(res_filmined) )
    print( "filmined_fil = " + str(res_filmined_fil) )


    # fee reward for messages (transactions)
    res_miner_fee_reward = int(val_miner_tip)
    res_miner_fee_reward_fil = val_miner_tip_fil

    # total: miner reward
    res_miner_reward = int(int(res_filmined) + int(res_miner_fee_reward))
    res_miner_reward_fil = res_miner_reward / 1000000000000000000
    res_miner_reward_info = "" + \
        str(res_miner_reward_fil) + \
        " FIL ( " + \
        str(res_filmined_fil) + \
        " FIL Block Reward and " + \
        str(res_miner_fee_reward_fil) + " FIL Fee Reward )"

    #block_cid["MinerReward"]["MinerReward"] = res_miner_reward
    #block_cid["MinerReward"]["MinerRewardFil"] = res_miner_reward_fil
    #block_cid["MinerReward"]["BlockReward"] = res_filmined
    #block_cid["MinerReward"]["BlockRewardFil"] = res_filmined_fil

    print( res_miner_reward_info )
    print( "miner = " + miner )

    # ---------- }


# ------------------------------------------------------------


def test_calc_miner_reward():
    global DAEMON_URL
    global DAEMON_TOKEN

    if DAEMON_URL == '':
        with open(str(Path.home()) + "/.lotus/api", "r") as text_file:
            daemon_api_line = text_file.read()
        daemon_api = daemon_api_line.split("/")
        daemon_api_ip = daemon_api[2]
        daemon_api_port = daemon_api[4]
        DAEMON_URL = "http://" + daemon_api_ip + ":" + daemon_api_port + "/rpc/v0"

    if DAEMON_TOKEN == '':
        with open(str(Path.home()) + "/.lotus/token", "r") as text_file:
            DAEMON_TOKEN = text_file.read()


    # Filecoin.ChainGetTipSetByHeight
    # curl -X POST -H "Authorization: Bearer $(cat ./token)" -d '{"method": "Filecoin.ChainGetTipSetByHeight", "params": [1239003, []], "id": 0}' http://127.0.0.1:1234/rpc/v0
    #
    #block_height = 1239003
    #res = daemon_get_json( "ChainGetTipSetByHeight", [block_height, []] )
    #block_cid_list = []
    #print( res )

    # ---------- {
    #'''
    #block_height = 1239003 # 1 parent
    #block_height = 1256880 # parents
    #block_height = 1239140 # 1 parent
    block_height = 1256900 # parents

    res = daemon_get_json( "ChainGetTipSetByHeight", [block_height, []] )

    block_cid_list = []

    i = 0
    for data in res["result"]["Cids"]:
        #print( f'[{i}] ' + data["/"] )
        block_cid = {}
        block_cid["Cid"] = data
        block_cid["Miner"] = res["result"]["Blocks"][i]["Miner"]

        #block_cid["Parent"] = res["result"]["Blocks"][i]["Parents"][0] # FIXME: if ( parents > 1 )

        #parents = []
        #parent_list = {}
        #parent_list["Cid"] = res["result"]["Blocks"][i]["Parents"][0] # FIXME: if ( parents > 1 )
        #parents.append( parent_list )
        #block_cid["Parent"] = parents

        # USE THIS
        block_cid["Parent"] = res["result"]["Blocks"][i]["Parents"]
        block_cid["ParentCount"] = len( res["result"]["Blocks"][i]["Parents"] )
        block_cid_list.append( block_cid )

        i += 1
    #'''
    # ---------- }

    #print( block_cid_list )



    # Filecoin.StateVMCirculatingSupplyInternal
    # Current block: (block height)
    #curl -X POST -H "Authorization: Bearer $(cat ./token)" -d '{"method": "Filecoin.StateVMCirculatingSupplyInternal", "params": [[{"/": "<current block cid>"}]], "id": 0}' http://127.0.0.1:1234/rpc/v0
    #
    #current_block_cid = {}
    #current_block_cid["/"] = "<current block cid>"
    #res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[current_block_cid]] )
    #print( res )
    #print( "FilVested: " + res["result"]["FilVested"] ) 
    #print( "FilMined: " + res["result"]["FilMined"] )
    #print( "FilBurnt: " + res["result"]["FilBurnt"] )
    #print( "FilLocked: " + res["result"]["FilLocked"] )
    #print( "FilCirculating: " + res["result"]["FilCirculating"] )
    #print( "FilReserveDisbursed: " + res["result"]["FilReserveDisbursed"] )

    # ---------- {
    #filmined_list = {}

    i = 0
    for block_cid in block_cid_list:
        res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[block_cid["Cid"]]] )
        #print( f'[{i}] {res}' )
        #FilMined = {}
        #FilMined["FilMined"] = res["result"]["FilMined"]
        #filmined_list[block_cid["cid"]["/"]] = FilMined
        #block_cid["FilMined"] = FilMined

        block_cid["FilMined"] = res["result"]["FilMined"]

        i += 1

    #print ( filmined_list )
    # ---------- }



    # Filecoin.StateVMCirculatingSupplyInternal
    # Parent block: (block height - 1)
    # curl -X POST -H "Authorization: Bearer $(cat ./token)" -d '{"method": "Filecoin.StateVMCirculatingSupplyInternal", "params": [[{"/": "<parent block cid>"}]], "id": 0}' http://127.0.0.1:1234/rpc/v0
    #
    #parent_block_cid = {}
    #parent_block_cid["/"] = "<parent block cid>"
    #res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[parent_block_cid]] )
    #print( res )
    #print( "FilVested: " + res["result"]["FilVested"] ) 
    #print( "FilMined: " + res["result"]["FilMined"] )
    #print( "FilBurnt: " + res["result"]["FilBurnt"] )
    #print( "FilLocked: " + res["result"]["FilLocked"] )
    #print( "FilCirculating: " + res["result"]["FilCirculating"] )
    #print( "FilReserveDisbursed: " + res["result"]["FilReserveDisbursed"] )

    # ---------- {
    #parent_filmined_list = {}

    i = 0
    for block_cid in block_cid_list:
        #res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[block_cid["Parent"][0]["Cid"]]] )

        # why parent[0], not parent[0..x] ?
        # maybe it's okay even if has several parents
        # due to same values (FilMined, etc.) each other.
        res = daemon_get_json( "StateVMCirculatingSupplyInternal", [[block_cid["Parent"][0]]] )
        #print( f'[{i}] {res}' )
        #FilMined = {}
        #FilMined["FilMined"] = res["result"]["FilMined"]
        #parent_filmined_list[block_cid["cid"]["/"]] = FilMined
        #block_cid["ParentFilMined"] = FilMined

        block_cid["ParentFilMined"] = res["result"]["FilMined"]

        i += 1

    #print ( parent_filmined_list )
    # ---------- }



    # Filecoin.StateCompute
    # current block cid
    # curl -X POST -H "Authorization: Bearer $(cat ./token)" -d '{"method": "Filecoin.StateCompute", "params": [1239003, [], [{"/": "<current block cid>"}]], "id": 0}' http://127.0.0.1:1234/rpc/v0
    #
    #block_height = 1239003
    #block_cid = {}
    #block_cid["/"] = "<current block cid>"
    #res = daemon_get_json( "StateCompute", [block_height, [], [block_cid]] )
    #print( res )

    # ---------- {
    i = 0
    for block_cid in block_cid_list:
        res = daemon_get_json( "StateCompute", [block_height, [], [block_cid["Cid"]]] )

        val_miner_tip = 0
        #val_total_cost = 0
        #val_refund = 0
        val_miner_penalty = 0
        val_miner_tip_fil = 0
        #val_total_cost_fil = 0
        #val_refund_fil = 0
        val_miner_penalty_fil = 0
        for data in res["result"]["Trace"]:
            #print( "BaseFeeBurn = " + data["GasCost"]["BaseFeeBurn"] )
            #print( "OverEstimationBurn = " + data["GasCost"]["OverEstimationBurn"] )
            #print( "MinerTip = " + data["GasCost"]["MinerTip"] )

            #print( '{"BaseFeeBurn": "' + data["GasCost"]["BaseFeeBurn"] + '", ' +
            #       '"OverEstimationBurn": "' + data["GasCost"]["OverEstimationBurn"] + '", ' +
            #       '"MinerTip": "' + data["GasCost"]["MinerTip"] + '"}' )

            #val_fil += int(data["GasCost"]["MinerTip"]) / 1000000000000000000

            val_miner_tip += int(data["GasCost"]["MinerTip"])
            #val_total_cost += int(data["GasCost"]["TotalCost"])
            #val_refund += int(data["GasCost"]["Refund"])
            val_miner_penalty += int(data["GasCost"]["MinerPenalty"])

        val_miner_tip_fil = val_miner_tip / 1000000000000000000
        #val_total_cost_fil = val_total_cost / 1000000000000000000
        #val_refund_fil = val_refund / 1000000000000000000
        val_miner_penalty_fil = val_miner_penalty / 1000000000000000000

        #print( "total miner tip  = " + str(val_miner_tip) + ", " + str(val_miner_tip_fil) + " FIL" )
        #print( "total total cost = " + str(val_total_cost) + ", " + str(val_total_cost_fil) + " FIL"  )
        #print( "total refund     = " + str(val_refund) + ", " + str(val_refund_fil) + " FIL"  )
        print( "total miner penalty  = " + str(val_miner_penalty) + ", " + str(val_miner_penalty_fil) + " FIL" )

        res_reward_info = {}
        res_reward_info["MinerTip"] = val_miner_tip
        res_reward_info["MinerTipFil"] = val_miner_tip_fil
        block_cid["MinerReward"] = res_reward_info
    # ---------- }



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
    #res_miner_reward = int(int(res_filmined) - int(res_miner_fee_reward))
    #res_miner_reward_fil = (res_miner_reward / 1000000000000000000)
    #res_miner_reward_info = "" +
    #    res_miner_reward_fil +
    #    " FIL ( " +
    #    res_filmined +
    #    " FIL Block Reward and " +
    #    res_miner_fee_reward_fil + " FIL Fee Reward )"

    # ---------- {
    i = 0
    for block_cid in block_cid_list:
        # //! FIXME
        # FilMined (current) - FilMined (parents[0]))
        #res_filmined = int(block_cid["FilMined"]) - int(block_cid["ParentFilMined"])

        # USE THIS
        # (FilMined (current) - FilMined (parents[0])) / len(parents)
        res_filmined = int(block_cid["FilMined"]) - int(block_cid["ParentFilMined"])
        res_filmined = int( res_filmined / int(block_cid["ParentCount"]) )
        #print( "parent count = " + str(block_cid["ParentCount"]) )
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

        block_cid["MinerReward"]["MinerReward"] = res_miner_reward
        block_cid["MinerReward"]["MinerRewardFil"] = res_miner_reward_fil
        block_cid["MinerReward"]["BlockReward"] = res_filmined
        block_cid["MinerReward"]["BlockRewardFil"] = res_filmined_fil

        #print( block_cid["Miner"] + ", " + res_miner_reward_info )

    # ---------- }



    print( "result" )
    print( "-----------------------------" )

    i = 0
    for block_cid in block_cid_list:
        miner = block_cid["Miner"]

        reward = block_cid["MinerReward"]["MinerReward"]
        reward_fil = block_cid["MinerReward"]["MinerRewardFil"]

        block_reward = block_cid["MinerReward"]["BlockReward"]
        block_reward_fil = block_cid["MinerReward"]["BlockRewardFil"]

        fee_reward = block_cid["MinerReward"]["MinerTip"]
        fee_reward_fil = block_cid["MinerReward"]["MinerTipFil"]

        print( f'[{i}] ' + miner + ", " + \
                str(reward_fil) + " (" + str(reward) + "), " + \
                str(block_reward_fil) + " (" + str(block_reward) + "), " + \
                str(fee_reward_fil) + "(" + str(fee_reward) + ")" )
        i += 1



# -----------------------------------------------


if __name__ == "__main__":
    #test_calc_miner_reward_test()

    # USE THIS
    # change: block_height = <tipset height>
    #test_calc_miner_reward()



