#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=C0301, W0511, W0603, W0703, R0914, R0912, R0915


# -------------------------------------------------------------------
# Purpose: Filecoin Lotus APIs test
# Author: Ho-Jung Kim (godmode2k@hotmail.com)
# Filename: lotus_apis_test.py
# Date: Since March 30, 2021
#
#
# Reference:
# - https://docs.filecoin.io/reference/lotus-api/
# - https://github.com/filecoin-project/lotus/blob/master/api/api_full.go
# - https://github.com/filecoin-shipyard/filecoin.js/tree/master/tests/src
#
#
# Note:
# - Environment: local-devnet
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

#
# CONFIG VARIABLES // OPTIONAL THEY ARE NORMALLY AUTODETECTED
#
# Example : MINER_URL = "http://127.0.0.1:2345/rpc/v0"
MINER_URL = ""
# MINER_TOKEN is the content of the ~/.lotusminer/token file
MINER_TOKEN = ""
DAEMON_URL = ""
DAEMON_TOKEN = ""

# REQUEST FUNCTIONS
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


def main():
    """ main function """

    global MINER_URL, MINER_TOKEN, DAEMON_URL, DAEMON_TOKEN

    # SET API IP PORT AND AUTH
    """
    if MINER_URL == '':
        with open(str(Path.home()) + "/.lotusminer/api", "r") as text_file:
            miner_api_line = text_file.read()
        miner_api = miner_api_line.split("/")
        miner_api_ip = miner_api[2]
        miner_api_port = miner_api[4]
        MINER_URL = "http://" + miner_api_ip + ":" + miner_api_port + "/rpc/v0"
    """
    if DAEMON_URL == '':
        with open(str(Path.home()) + "/.lotus/api", "r") as text_file:
            daemon_api_line = text_file.read()
        daemon_api = daemon_api_line.split("/")
        daemon_api_ip = daemon_api[2]
        daemon_api_port = daemon_api[4]
        DAEMON_URL = "http://" + daemon_api_ip + ":" + daemon_api_port + "/rpc/v0"

    """
    if MINER_TOKEN == '':
        with open(str(Path.home()) + "/.lotusminer/token", "r") as text_file:
            MINER_TOKEN = text_file.read()
    """
    if DAEMON_TOKEN == '':
        with open(str(Path.home()) + "/.lotus/token", "r") as text_file:
            DAEMON_TOKEN = text_file.read()
    # ------------------------------------------------------------------------







    # APIs test
    # ------------------------------------------------------------------------

    empty_tipsetkey = []



    # ------------------------------------------------------------------------
    # Wallet
    # ------------------------------------------------------------------------
    # Wallet list
    # WalletSign
    # WalletSignMessage

    print( "\n" )
    print( "--------------------------------------" )
    print( "[WalletList]" )
    print( "--------------------------------------" )
    result_WalletList = daemon_get_json( "WalletList", [] )
    count = 0
    print( "Address, Balance" )
    for address in result_WalletList["result"]:
        result_WalletBalance = daemon_get_json( "WalletBalance", [address] )
        print( f'{ count }: { address }, { int(result_WalletBalance["result"])/1000000000000000000 } FIL' )
        count += 1

    """
    result:
    Address, Balance
    0: t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy, 200.0 FIL
    1: t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q, 0.0 FIL
    2: t3wqmq6ymuti6vjtd7x5htepaynwokk7plyxfs4m2d2dndqwmnza25o66r5wv6lu73ha5uae3wpbwyjcyxepna, 49479257.99991438 FIL
    """



    # ------------------------------------------------------------------------
    # Miner
    # ------------------------------------------------------------------------
    # n/a



    # ------------------------------------------------------------------------
    # Mpool(Message Pool) Pending list
    # ------------------------------------------------------------------------
    # MpoolPending

    print( "\n" )
    print( "--------------------------------------" )
    print( "[MpoolPending]" )
    print( "--------------------------------------" )
    result_MpoolPending = daemon_get_json( "MpoolPending", [empty_tipsetkey] )
    count = 0
    for message in result_MpoolPending["result"]:
        from_address = message["Message"]["From"]
        if from_address in result_WalletList["result"]:
            print( f'{ count}: { message["Message"] }' )
            count += 1
    if count == 0:
        print( "None..." )

    """
    result:
    0: {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 2, 'Value': '1000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '101354', 'GasPremium': '100300', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceauqsv73z35kfasyjddbmmxc4b5ui2zxumb7fohyg74g34gnakw2i'}}
    1: {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 3, 'Value': '1100000000000000000', 'GasLimit': 657085, 'GasFeeCap': '101691', 'GasPremium': '100637', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceaweh4ocpw6qndxgd4ju64arsope7pbkk7dvrplytmouhfzfs4hru'}}
    """



    # ------------------------------------------------------------------------
    # Transaction (CID)
    # ------------------------------------------------------------------------
    # ChainGetMessage

    print( "\n" )
    print( "--------------------------------------" )
    print( "[ChainGetMessage]" )
    print( "--------------------------------------" )
    cid = { "/": "bafy2bzacea4vvb36j2dndxghv3n47u3rihvqk6bo7dstrmapmlbexilxlj3py" }
    #cid_json = json.dumps( cid )
    #print("cid json = %s\n" % cid_json)
    result_ChainGetMessage = daemon_get_json( "ChainGetMessage", [cid] )
    print( f'CID = { [cid] }' )
    #print( f'{ result_ChainGetMessage }' )
    print( f'{ result_ChainGetMessage["result"] }' )

    """
    result:
    {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 0, 'Value': '1000000000000000000', 'GasLimit': 2722522, 'GasFeeCap': '101606', 'GasPremium': '100552', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzacedi7gjirpoe2mo27si42ygkdzidgd6ahcqwivdczuli77yygohwoa'}}
    """



    # ------------------------------------------------------------------------
    # Gas
    # ------------------------------------------------------------------------
    # GasEstimateFeeCap
    # GasEstimateGasLimit
    # GasEstimateGasPremium
    # GasEstimateMessageGas

    print( "\n" )
    print( "--------------------------------------" )
    print( "[GasEstimate]" )
    print( "--------------------------------------" )
    msg_To = "t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q"
    msg_From = "t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy"
    msg_Value = "2" + "000000000000000000" # atto-FIL (1e+18), nano-FIL (1e+9)
    msg_GasLimit = 0 # int64
    msg_GasFeeCap = "0"
    msg_GasPremium = "0"
    #msg_Method = 0
    #msg_Nonce = 0
    #msg_Params = ""
    message = { "To": msg_To,
            "From": msg_From,
            "Value": msg_Value,
            "GasLimit": msg_GasLimit,
            "GasFeeCap": msg_GasFeeCap,
            "GasPremium": msg_GasPremium
            #,"Method": msg_Method
            #,"Nonce": msg_Nonce
            #,"Params": msg_Params
            }
    message_block_incl= 0 # n block include
    message_params = [] # Params: CIDs

    result_GasEstimateFeeCap = daemon_get_json( "GasEstimateFeeCap", [message, message_block_incl, message_params] )
    gas_feecap = result_GasEstimateFeeCap["result"]
    print( f'GasEstimateFeeCap = { result_GasEstimateFeeCap }' )

    """
    result:
    {'jsonrpc': '2.0', 'result': '100', 'id': 3}
    """

    result_GasEstimateGasLimit = daemon_get_json( "GasEstimateGasLimit", [message, message_params] )
    print( f'GasEstimateGasLimit = { result_GasEstimateGasLimit }' )

    """
    result:
    {'jsonrpc': '2.0', 'result': 525668, 'id': 3}
    """

    result_MpoolGetConfig = daemon_get_json( "MpoolGetConfig", [] )
    print( f'MpoolGetConfig = { result_MpoolGetConfig }' )

    """
    result:
    MpoolGetConfig = {'jsonrpc': '2.0', 'result': {'PriorityAddrs': None, 'SizeLimitHigh': 30000, 'SizeLimitLow': 20000, 'ReplaceByFeeRatio': 1.25, 'PruneCooldown': 60000000000, 'GasLimitOverestimation': 1.25}, 'id': 3}
    """

    # Note: In Python 3.x use int instead of long
    gas_limit = int(result_GasEstimateGasLimit["result"]) * int(float(result_MpoolGetConfig["result"]["GasLimitOverestimation"]))
    #print( f'GasEstimateGasLimit = {result_GasEstimateGasLimit["result"]}, GasLimitOverestimation = {result_MpoolGetConfig["result"]["GasLimitOverestimation"]}' )
    print( f'GasLimit = ({result_GasEstimateGasLimit["result"]} x {result_MpoolGetConfig["result"]["GasLimitOverestimation"]}) = { gas_limit } (int, truncated)' )

    result_GasEstimateGasPremium = daemon_get_json( "GasEstimateGasPremium", [message_block_incl, msg_From, gas_limit, message_params] )
    gas_premium = result_GasEstimateGasPremium["result"]
    print( f'GasEstimateGasPremium = { result_GasEstimateGasPremium }' )

    """
    result:
    {'jsonrpc': '2.0', 'result': '200839', 'id': 3}
    """



    # ------------------------------------------------------------------------
    # Replacing messages in the pool
    # ------------------------------------------------------------------------
    # mpool replace --gas-feecap <feecap> --gas-premium <premium> <from> <nonce>

    print( "\n" )
    print( "--------------------------------------" )
    print( "[Replacing messages in the pool]" )
    print( "--------------------------------------" )

    # get a message (pending)
    cid = { "/": "bafy2bzaced6zrni7bq7il6dmtyfnifqegnp4anwq2jlvgbqqxiwq7jxvdlsku" }
    result_ChainGetMessage = daemon_get_json( "ChainGetMessage", [cid] )
    print( f'{ result_ChainGetMessage["result"] }\n' )

    """
    result:
    {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 2, 'Value': '1000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '101354', 'GasPremium': '100300', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceauqsv73z35kfasyjddbmmxc4b5ui2zxumb7fohyg74g34gnakw2i'}}
    """

    # replace
    ReplaceByFeeRatioDefault = result_MpoolGetConfig["result"]["ReplaceByFeeRatio"]
    #
    # SEE: lotus/chain/messagepool/messagepool.go: 179: func ComputeMinRBF(...) {...}
    # - gas_premium = int( int(gas_premium) + ((int(gas_premium) * ((float(ReplaceByFeeRatioDefault) - 1) * 256)) / 256) )
    gas_premium = int( int(gas_premium) + ((int(gas_premium) * ((float(ReplaceByFeeRatioDefault) - 1) * 256)) / 256) )
    #
    #gas_feecap = int(222111) # test
    #gas_premium = int(111222) # test
    #gas_feecap_int = int(gas_premium + int((float(gas_premium) * 1.25)/100.0) ) # test
    #
    new_ChainGetMessage = result_ChainGetMessage["result"]
    new_ChainGetMessage["GasFeeCap"] = str(gas_feecap) # not int, string here
    new_ChainGetMessage["GasPremium"] = str(gas_premium) # not int, string here
    print( f'new_ChainGetMessage = { new_ChainGetMessage }\n' )

    # sign
    result_WalletSignMessage = daemon_get_json( "WalletSignMessage", [new_ChainGetMessage["From"], new_ChainGetMessage] )
    print( f'result_WalletSignMessage = { result_WalletSignMessage }\n' )
    print( f'result_WalletSignMessage = { result_WalletSignMessage["result"] }\n' )

    # send
    print( "skip..." )
    #result_MpoolPush = daemon_get_json( "MpoolPush", [result_WalletSignMessage["result"]] )
    #print( f'result_MpoolPush = { result_MpoolPush }\n' )

    """
    result:
    {'jsonrpc': '2.0', 'result': {'/': 'bafy2bzacedz3mefhrexxw4bvzkvt5xghmpukfahz7wbijjkfn3zokqfysdeoy'}, 'id': 3}
    """



    # Iteration
    """
    print( "Iteration:" )
    result_MpoolPending = daemon_get_json( "MpoolPending", [empty_tipsetkey] )
    count = 0
    for message in result_MpoolPending["result"]:
        from_address = message["Message"]["From"]
        if from_address in result_WalletList["result"]:
            print( f'{ count}: { message["Message"] }' )

            # replace
            ReplaceByFeeRatioDefault = result_MpoolGetConfig["result"]["ReplaceByFeeRatio"]
            # SEE: lotus/chain/messagepool/messagepool.go: 179: func ComputeMinRBF(...) {...}
            # - gas_premium = int( int(gas_premium) + ((int(gas_premium) * ((float(ReplaceByFeeRatioDefault) - 1) * 256)) / 256) )
            gas_premium = int( int(gas_premium) + ((int(gas_premium) * ((float(ReplaceByFeeRatioDefault) - 1) * 256)) / 256) )
            #
            #gas_feecap = int(222111) # test
            #gas_premium = int(111222) # test
            #gas_feecap_int = int(gas_premium + int((float(gas_premium) * 1.25)/100.0) ) # test
            #
            new_ChainGetMessage = message["Message"]
            new_ChainGetMessage["GasFeeCap"] = str(gas_feecap) # not int, string here
            new_ChainGetMessage["GasPremium"] = str(gas_premium) # not int, string here
            print( f'new_ChainGetMessage = { new_ChainGetMessage }\n' )

            # sign
            result_WalletSignMessage = daemon_get_json( "WalletSignMessage", [new_ChainGetMessage["From"], new_ChainGetMessage] )
            print( f'result_WalletSignMessage = { result_WalletSignMessage }\n' )
            print( f'result_WalletSignMessage = { result_WalletSignMessage["result"] }\n' )

            # send
            print( "skip..." )
            #result_MpoolPush = daemon_get_json( "MpoolPush", [result_WalletSignMessage["result"]] )
            #print( f'result_MpoolPush = { result_MpoolPush }\n' )


            count += 1
    if count == 0:
        print( "None..." )
    """



    # ------------------------------------------------------------------------
    # Send
    # ------------------------------------------------------------------------
    # MpoolPush
    # MpoolPushMessage

    print( "\n" )
    print( "--------------------------------------" )
    print( "[MpoolPushMessage]" )
    print( "--------------------------------------" )
    msg_To = "t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q"
    msg_From = "t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy"
    msg_Value = "2" + "000000000000000000" # atto-FIL (1e+18), nano-FIL (1e+9)
    msg_GasLimit = 0 # int64
    msg_GasFeeCap = "0"
    msg_GasPremium = "0"
    message = { "To": msg_To,
            "From": msg_From,
            "Value": msg_Value,
            "GasLimit": msg_GasLimit,
            "GasFeeCap": msg_GasFeeCap,
            "GasPremium": msg_GasPremium }
    msg_MaxFee = "0"
    message_maxfee = { "MaxFee": msg_MaxFee }
    print( "message = \n%s" % [message, message_maxfee] )
    #message_json = json.dumps( message )
    #print( "message (json) = %s\n" % message_json )
    #
    print( "skip..." )
    #result_MpoolPushMessage = daemon_get_json( "MpoolPushMessage", [message, message_maxfee] )
    #print( f'result_MpoolPushMessage = { result_MpoolPushMessage }' )

    """
    result:
    {'jsonrpc': '2.0', 'result': {'Message': {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 1, 'Value': '2', 'GasLimit': 2711147, 'GasFeeCap': '100471', 'GasPremium': '99417', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzacecuwkzzrmpmgb4jjl3beainzbzxy4vy4gxqg4lppba7e47uazjhau'}}, 'Signature': {'Type': 1, 'Data': 'vYg5Kd/pl/ekwbU0Wiv0S2IiLHgSjXRcwkoCWOhSagR9EkPQvfMkPS7XLmmPVnuS4R7BsDaeqaBhDvOACFavkwE='}, 'CID': {'/': 'bafy2bzaced4bfm3uqtwscqrejs7qixj3lexxneazzwxuawgyz7p6onph72ffe'}}, 'id': 3}
    """





if __name__ == "__main__":
    main()
