/* --------------------------------------------------------------
Purpose:    Filecoin Lotus APIs test
Author:     Ho-Jung Kim (godmode2k@hotmail.com)
Filename:   lotus_apis_example.go
Date:       Since March 30, 2021


Reference:
- https://docs.filecoin.io/reference/lotus-api/
- https://github.com/filecoin-project/lotus/blob/master/api/api_full.go
- https://github.com/filecoin-shipyard/filecoin.js/tree/master/tests/src


Note:
- Environment: local-devnet
- Mainnet: USE THIS AT YOUR OWN RISK


License:

*
* Copyright (C) 2021 Ho-Jung Kim (godmode2k@hotmail.com)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*      http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*
-----------------------------------------------------------------
Note:
-----------------------------------------------------------------
1. Build:
	$ go build lotus_apis_example.go
    or
	$ go run lotus_apis_example.go
-------------------------------------------------------------- */
package main



//! Header
// ---------------------------------------------------------------

import (
    "fmt"
    "log"
    "bytes"
    "strconv"
    //"math"
    "math/big"
    //"encoding/hex"
    "strings"
    //"time"
    //"reflect"

	"os"
	"io"
	"bufio"


    //"net"
    //"net/rpc"
    //"net/rpc/jsonrpc"


    "net/http"
    "io/ioutil"
    "encoding/json"


	"lotus_apis_test_golang/types"
)



//! Definition
// --------------------------------------------------------------------
var SERVER_LOTUS_NODE_IP = ""
var SERVER_LOTUS_MINER_IP = ""
var SERVER_LOTUS_NODE_PORT = ""
var SERVER_LOTUS_MINER_PORT = ""

var LOTUS_NODE_TOKEN = ""
var LOTUS_MINER_TOKEN = ""
var LOTUS_NODE_URL = ""
var LOTUS_MINER_URL = ""

// LOTUS_NODE_URL = "http://" + SERVER_LOTUS_NODE_IP + ":" + SERVER_LOTUS_NODE_PORT + "/rpc/v0"
// LOTUS_MINER_URL = "http://" + SERVER_LOTUS_MINER_IP + ":" + SERVER_LOTUS_MINER_PORT + "/rpc/v0"



//! Implementation
// --------------------------------------------------------------------
func request_lotus_node_api(_method string, _params []interface{}, result interface{})  {
    //var result types.Result

    //var params []interface{}
    //params = append( params, "...", "..." )
    request_data := types.RequestData { Jsonrpc: "2.0", Method: "Filecoin." + _method, Params: _params, Id: 0 } 
    //request_data := types.RequestData { Jsonrpc: "2.0", Method: "...",
    //  Params: []interface{}{"...", "..."}, Id: 0 } 

    message, _ := json.Marshal( request_data )
    //fmt.Println( "request: ", request_data )

    //response, err := http.Post( LOTUS_NODE_URL, "application/json", bytes.NewBuffer(message) )
	client := &http.Client{}
    req, err := http.NewRequest( "POST", LOTUS_NODE_URL, bytes.NewBuffer(message) )
    if err != nil {
        log.Fatal( "http.Post: ", err )
	}
	req.Header.Add( "Content-Type", "application/json" )
	req.Header.Add( "Authorization", "Bearer " + LOTUS_NODE_TOKEN )
	response, err := client.Do( req )

    defer response.Body.Close()
    if err != nil {
        log.Fatal( "http.Post: ", err )
    }   

    responseBody, err := ioutil.ReadAll( response.Body )
    if err != nil {
        log.Fatal( "ioutil.ReadAll: ", err )
    }   
    //fmt.Println( string(responseBody) )

    err = json.Unmarshal( responseBody, &result )
    if err != nil {
        log.Fatal( "json.Unmarshal: ", err )
    }   
    //fmt.Println( "jsonrpc =" , result.Jsonrpc, ", id =", result.Id, ", result =", result.Result )
    //fmt.Println( "result =" , result )

	//return result
}

func main() {

	var ip_port []string

	// Lotus Node API (IP:PORT)
	{
		ip_port = nil

		fp, err := os.OpenFile( os.Getenv("HOME") + "/.lotus/api", os.O_RDONLY, os.ModePerm )
		if err != nil {
			log.Fatal( err )
		}
		defer fp.Close()

		reader := bufio.NewReader( fp )
		for {
			line, err := reader.ReadString( '\n' )
			//line, _, err := reader.ReadLine()

			//fmt.Println( "line = ", line )
			ip_port = strings.Split( line, "/" )
			SERVER_LOTUS_NODE_IP = ip_port[2]
			SERVER_LOTUS_NODE_PORT = ip_port[4]
			LOTUS_NODE_URL = "http://" + SERVER_LOTUS_NODE_IP + ":" + SERVER_LOTUS_NODE_PORT + "/rpc/v0"

			if err != nil {
				if err == io.EOF {
					break
				}

				log.Fatalf( "[Error] read file: %v", err )
				return
			}
		}

		//fmt.Println( "Lotus Node API: ", ip_port )
	}

	/*
	// Lotus Miner API (IP:PORT)
	{
		ip_port = nil

		fp, err := os.OpenFile( os.Getenv("HOME") + "/.lotusminer/api", os.O_RDONLY, os.ModePerm )
		if err != nil {
			log.Fatal( err )
		}
		defer fp.Close()

		reader := bufio.NewReader( fp )
		for {
			line, err := reader.ReadString( '\n' )
			//line, _, err := reader.ReadLine()

			//fmt.Println( "line = ", line )
			ip_port = strings.Split( line, "/" )
			SERVER_LOTUS_MINER_IP = ip_port[2]
			SERVER_LOTUS_MINER_PORT = ip_port[4]
			LOTUS_MINER_URL = "http://" + SERVER_LOTUS_MINER_IP + ":" + SERVER_LOTUS_MINER_PORT + "/rpc/v0"

			if err != nil {
				if err == io.EOF {
					break
				}

				log.Fatalf( "[Error] read file: %v", err )
				return
			}
		}

		//fmt.Println( "Lotus Miner API: ", ip_port )
	}
	*/

	// Lotus Node Token
	{
		fp, err := os.OpenFile( os.Getenv("HOME") + "/.lotus/token", os.O_RDONLY, os.ModePerm )
		if err != nil {
			log.Fatal( err )
		}
		defer fp.Close()

		reader := bufio.NewReader( fp )
		for {
			line, err := reader.ReadString( '\n' )
			//line, _, err := reader.ReadLine()

			//fmt.Println( "line = ", line )
			LOTUS_NODE_TOKEN = line

			if err != nil {
				if err == io.EOF {
					break
				}

				log.Fatalf( "[Error] read file: %v", err )
				return
			}
		}

		//fmt.Println( "Lotus Node Token: ", LOTUS_NODE_TOKEN )
	}

	/*
	// Lotus Miner Token
	{
		fp, err := os.OpenFile( os.Getenv("HOME") + "/.lotusminer/token", os.O_RDONLY, os.ModePerm )
		if err != nil {
			log.Fatal( err )
		}
		defer fp.Close()

		reader := bufio.NewReader( fp )
		for {
			line, err := reader.ReadString( '\n' )
			//line, _, err := reader.ReadLine()

			//fmt.Println( "line = ", line )
			LOTUS_MINER_TOKEN = line

			if err != nil {
				if err == io.EOF {
					break
				}

				log.Fatalf( "[Error] read file: %v", err )
				return
			}
		}

		//fmt.Println( "Lotus Miner Token: ", LOTUS_MINER_TOKEN )
	}
	*/





    // APIs test
    // ------------------------------------------------------------------------

    //empty_tipsetkey = []



    // ------------------------------------------------------------------------
    // Wallet
    // ------------------------------------------------------------------------
    // Wallet list
    // WalletSign
    // WalletSignMessage

	fmt.Println( "--------------------------------------" )
	fmt.Println( "[WalletList]" )
	fmt.Println( "--------------------------------------" )

	// Filecoin.WalletList
	//  
	// request:
	// $ curl -X POST --data
	//  '{"jsonrpc":"2.0",
	//  "method":"Filecoin.WalletList",
	//  "params":[],"id":0}'
	//  -H "Content-Type: application/json; Authorization: Bearer <LOTUS_NODE_TOKEN>"
	//  http://127.0.0.1:1234/

	var result_WalletList types.Results
	var params []interface{}

	request_lotus_node_api( "WalletList", params, &result_WalletList )
	fmt.Println( "jsonrpc =" , result_WalletList.Jsonrpc, ", id =", result_WalletList.Id, ", result =", result_WalletList.Result )
	fmt.Println( "" )

	fmt.Println( "Address, Balance" )
	for i := 0; i < len(result_WalletList.Result); i++ {
		address := result_WalletList.Result[i]
		params := append( params, address )

		var result_WalletBalance types.Result
		request_lotus_node_api( "WalletBalance", params, &result_WalletBalance )

		//! DO NOT USE THIS
		//balance_attofil_int := new(big.Int)
		//balance_attofil_int.SetString( result_WalletBalance.Result, 10 )
		//balance_attofil_float := new(big.Float)
		//balance_attofil_float.SetString( balance_attofil_int.String() )
		//balance_fil_ := new(big.Float).Quo(balance_attofil_float, big.NewFloat(math.Pow10(18)))
		//fmt.Printf( "%d: %s, %.18f FIL, %s\n", i, address, balance_fil_, result_WalletBalance.Result )

		{
			balance_fil := ""
			balance_attofil_int := new(big.Int)
			balance_attofil_int.SetString( result_WalletBalance.Result, 10 )

			// build.FilecoinPrecision
			// SEE: build/params_shared_vals.go:75
			const FilecoinPrecision = uint64(1_000_000_000_000_000_000)

			// chain/types/fil.go:18
			// func (f FIL) Unitless() string {...}
			r := new(big.Rat).SetFrac(balance_attofil_int, big.NewInt(int64(FilecoinPrecision)))
			if r.Sign() == 0 {
				balance_fil = "0"
			}
			balance_fil = strings.TrimRight(strings.TrimRight(r.FloatString(18), "0"), ".")

			fmt.Printf( "%d: %s, %s FIL (%s)\n", i, address, balance_fil, result_WalletBalance.Result )
		}

	}


	/*
	result:
	Address, Balance
	0: t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy, 200.0 FIL
	1: t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q, 0.0 FIL
	2: t3wqmq6ymuti6vjtd7x5htepaynwokk7plyxfs4m2d2dndqwmnza25o66r5wv6lu73ha5uae3wpbwyjcyxepna, 49479257.99991438 FIL
	*/



    // ------------------------------------------------------------------------
    // Miner
    // ------------------------------------------------------------------------
    // n/a



    // ------------------------------------------------------------------------
    // Mpool(Message Pool) Pending list
    // ------------------------------------------------------------------------
    // MpoolPending

    fmt.Println( "" )
	fmt.Println( "--------------------------------------" )
	fmt.Println( "[MpoolPending]" )
	fmt.Println( "--------------------------------------" )

	// Filecoin.MpoolPending
	//  
	// request:
	// $ curl -X POST --data
	//  '{"jsonrpc":"2.0",
	//  "method":"Filecoin.MpoolPending",
	//  "params":[[]],"id":0}'
	//  -H "Content-Type: application/json"
	//  -H "Authorization: Bearer <LOTUS_NODE_TOKEN>"
	//  http://127.0.0.1:1234/

	var result_MpoolPending types.Result_block
	params = nil
	params = append( params, new([]string) )

	request_lotus_node_api( "MpoolPending", params, &result_MpoolPending )
	fmt.Println( "jsonrpc =" , result_MpoolPending.Jsonrpc, ", id =", result_MpoolPending.Id, ", result =", result_MpoolPending.Result )
	fmt.Println( "" )

	//fmt.Println( result_MpoolPending.Result.([]interface{}) )

	count := 0
	for i := 0; i < len(result_MpoolPending.Result.([]interface{})); i++ {
		//fmt.Println( i, ":", result_MpoolPending.Result.([]interface{})[i] )
		from_address := result_MpoolPending.Result.([]interface{})[i].(map[string]interface{})["Message"].(map[string]interface{})["From"]
		//fmt.Println( i, ":", "From address:", from_address )

		for j := 0; j < len(result_WalletList.Result); j++ {
			if from_address == result_WalletList.Result[i] {
				//fmt.Println( count, ":", result_MpoolPending.Result.([]interface{})[i], "\n" )
    			data, _ := json.Marshal( result_MpoolPending.Result.([]interface{})[i] )
				fmt.Println( count, ":", string(data), "\n" )
				count += 1
			}
		}
	}

	/*
	result:
	0 : {"CID":{"/":"bafy2bzacedz3mefhrexxw4bvzkvt5xghmpukfahz7wbijjkfn3zokqfysdeoy"},"Message":{"CID":{"/":"bafy2bzaceapnhc2wtwb4wldmny6tutgja3n6yrvji5533jy5ywlnsenxhi4ia"},"From":"t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy","GasFeeCap":"222111","GasLimit":657085,"GasPremium":"139027","Method":0,"Nonce":2,"Params":null,"To":"t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q","Value":"1000000000000000000","Version":0},"Signature":{"Data":"KKnxPAjKPwOJXVhU0RZTCsYH4EMV7ka3infNzJt6Z/JUtqJ24q9bi0AhPpbUdOuzdiy3k7c4WRzDgIua+xKXiwE=","Type":1}}

1 : {"CID":{"/":"bafy2bzacedz3mefhrexxw4bvzkvt5xghmpukfahz7wbijjkfn3zokqfysdeoy"},"Message":{"CID":{"/":"bafy2bzaceapnhc2wtwb4wldmny6tutgja3n6yrvji5533jy5ywlnsenxhi4ia"},"From":"t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy","GasFeeCap":"222111","GasLimit":657085,"GasPremium":"139027","Method":0,"Nonce":2,"Params":null,"To":"t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q","Value":"1000000000000000000","Version":0},"Signature":{"Data":"KKnxPAjKPwOJXVhU0RZTCsYH4EMV7ka3infNzJt6Z/JUtqJ24q9bi0AhPpbUdOuzdiy3k7c4WRzDgIua+xKXiwE=","Type":1}}

2 : {"CID":{"/":"bafy2bzacedz3mefhrexxw4bvzkvt5xghmpukfahz7wbijjkfn3zokqfysdeoy"},"Message":{"CID":{"/":"bafy2bzaceapnhc2wtwb4wldmny6tutgja3n6yrvji5533jy5ywlnsenxhi4ia"},"From":"t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy","GasFeeCap":"222111","GasLimit":657085,"GasPremium":"139027","Method":0,"Nonce":2,"Params":null,"To":"t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q","Value":"1000000000000000000","Version":0},"Signature":{"Data":"KKnxPAjKPwOJXVhU0RZTCsYH4EMV7ka3infNzJt6Z/JUtqJ24q9bi0AhPpbUdOuzdiy3k7c4WRzDgIua+xKXiwE=","Type":1}}
	*/



    // ------------------------------------------------------------------------
    // Transaction (CID)
    // ------------------------------------------------------------------------
    // ChainGetMessage

    fmt.Println( "" )
    fmt.Println( "--------------------------------------" )
    fmt.Println( "[ChainGetMessage]" )
    fmt.Println( "--------------------------------------" )

	var result_ChainGetMessage types.Result_block
	cid := make( map[string]string )
	cid["/"] = "bafy2bzacea4vvb36j2dndxghv3n47u3rihvqk6bo7dstrmapmlbexilxlj3py"
	params = nil
	params = append( params, cid )

	request_lotus_node_api( "ChainGetMessage", params, &result_ChainGetMessage )
	fmt.Println( "jsonrpc =" , result_ChainGetMessage.Jsonrpc, ", id =", result_ChainGetMessage.Id, ", result =", result_ChainGetMessage.Result )
	fmt.Println( "" )

	cid_json, _ := json.Marshal( cid )
    fmt.Println( "CID =", string(cid_json) )
	data, _ := json.Marshal( result_ChainGetMessage.Result )
    fmt.Println( string(data) )

    /*
    result:
    {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 0, 'Value': '1000000000000000000', 'GasLimit': 2722522, 'GasFeeCap': '101606', 'GasPremium': '100552', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzacedi7gjirpoe2mo27si42ygkdzidgd6ahcqwivdczuli77yygohwoa'}}
    */



    // ------------------------------------------------------------------------
    // Gas
    // ------------------------------------------------------------------------
    // GasEstimateFeeCap
    // GasEstimateGasLimit
    // GasEstimateGasPremium
    // GasEstimateMessageGas

    fmt.Println( "" )
    fmt.Println( "--------------------------------------" )
    fmt.Println( "[GasEstimate]" )
    fmt.Println( "--------------------------------------" )

	msg_To := "t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q"
	msg_From := "t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy"
	msg_Value := "2" + "000000000000000000" // atto-FIL (1e+18), nano-FIL (1e+9)
	msg_GasLimit := 0 // int64
	msg_GasFeeCap := "0"
	msg_GasPremium := "0"
	//msg_Method := 0
	//msg_Nonce := 0
	//msg_Params := ""
	msg_MaxFee := "0"
	message := make( map[string]interface{} )
	message["To"] = string( msg_To )
	message["From"] = string( msg_From )
	message["Value"] = string( msg_Value )
	message["GasLimit"] = int( msg_GasLimit )
	message["GasFeeCap"] = string( msg_GasFeeCap )
	message["GasPremium"] = string( msg_GasPremium )
	//message["Method"] = string( msg_Method )
	//message["Nonce"] = string( msg_Nonce )
	//message["Params"] = string( msg_Params )
	message_block_incl := 0 // n block include
	message_params := new( []string ) // Params: CIDs

	var result_GasEstimateFeeCap types.Result
	params = nil
	params = append( params, message )
	params = append( params, message_block_incl )
	params = append( params, message_params )

	request_lotus_node_api( "GasEstimateFeeCap", params, &result_GasEstimateFeeCap )
	fmt.Println( "jsonrpc =" , result_GasEstimateFeeCap.Jsonrpc, ", id =", result_GasEstimateFeeCap.Id, ", result =", result_GasEstimateFeeCap.Result )
	fmt.Println( "" )

	gas_feecap := result_GasEstimateFeeCap.Result
	gas_feecap_int, _ := strconv.Atoi( gas_feecap )
    fmt.Println( "GasEstimateFeeCap =", gas_feecap )
	fmt.Println( "" )

	/*
    result:
    {'jsonrpc': '2.0', 'result': '100', 'id': 3}
	*/


	var result_GasEstimateGasLimit types.Result_block
	params = nil
	params = append( params, message )
	params = append( params, message_params )

	request_lotus_node_api( "GasEstimateGasLimit", params, &result_GasEstimateGasLimit )
	fmt.Println( "jsonrpc =" , result_GasEstimateGasLimit.Jsonrpc, ", id =", result_GasEstimateGasLimit.Id, ", result =", result_GasEstimateGasLimit.Result )
	fmt.Println( "" )
    fmt.Println( "GasEstimateGasLimit =", result_GasEstimateGasLimit.Result )
	fmt.Println( "" )

	/*
    result:
    {'jsonrpc': '2.0', 'result': 525668, 'id': 3}
    */


	var result_MpoolGetConfig types.Result_block
	params = nil

	request_lotus_node_api( "MpoolGetConfig", params, &result_MpoolGetConfig )
	fmt.Println( "jsonrpc =" , result_MpoolGetConfig.Jsonrpc, ", id =", result_MpoolGetConfig.Id, ", result =", result_MpoolGetConfig.Result )
	fmt.Println( "" )
	data, _ = json.Marshal( result_MpoolGetConfig.Result )
    fmt.Println( "MpoolGetconfig =", string(data) )
	fmt.Println( "" )

	/*
    result:
    MpoolGetConfig = {'jsonrpc': '2.0', 'result': {'PriorityAddrs': None, 'SizeLimitHigh': 30000, 'SizeLimitLow': 20000, 'ReplaceByFeeRatio': 1.25, 'PruneCooldown': 60000000000, 'GasLimitOverestimation': 1.25}, 'id': 3}
	*/


    fmt.Println( "GasEstimateGasLimit =", result_GasEstimateGasLimit.Result, "GasLimitOverestimation = ", result_MpoolGetConfig.Result.(map[string]interface{})["GasLimitOverestimation"] )

	GasLimitOverestimation_float := result_MpoolGetConfig.Result.(map[string]interface{})["GasLimitOverestimation"].(float64)
	GasEstimateGasLimit_float := result_GasEstimateGasLimit.Result.(float64)

	gas_limit_int := int( GasEstimateGasLimit_float * GasLimitOverestimation_float )
    fmt.Printf( "GasLimit = (%f x %f) = %d (int, truncated)\n", GasEstimateGasLimit_float, GasLimitOverestimation_float, gas_limit_int )
	fmt.Println( "" )

	/*
	result:
	GasEstimateGasLimit = 525668 GasLimitOverestimation =  1.25
	GasLimit = (525668.000000 x 1.250000) = 657085 (int, truncated)
	*/


	var result_GasEstimateGasPremium types.Result
	params = nil
	params = append( params, message_block_incl )
	params = append( params, msg_From )
	params = append( params, gas_limit_int )
	params = append( params, message_params )

	request_lotus_node_api( "GasEstimateGasPremium", params, &result_GasEstimateGasPremium )
	fmt.Println( "jsonrpc =" , result_GasEstimateGasPremium.Jsonrpc, ", id =", result_GasEstimateGasPremium.Id, ", result =", result_GasEstimateGasPremium.Result )
	fmt.Println( "" )

	gas_premium := result_GasEstimateGasPremium.Result
	gas_premium_int, _ := strconv.Atoi( gas_premium )
    fmt.Println( "GasEstimateGasPremium =", gas_premium )

	/*
    result:
    {'jsonrpc': '2.0', 'result': '200839', 'id': 3}
	*/



    // ------------------------------------------------------------------------
    // Replacing messages in the pool
    // ------------------------------------------------------------------------
    // mpool replace --gas-feecap <feecap> --gas-premium <premium> <from> <nonce>

    fmt.Println( "" )
    fmt.Println( "--------------------------------------" )
    fmt.Println( "[Replacing messages in the pool]" )
    fmt.Println( "--------------------------------------" )

    // get a message (pending)
	var result_pending_ChainGetMessage types.Result_block
	cid = nil
	cid = make( map[string]string )
	cid["/"] = "bafy2bzacebsnh3xawp6stifqbir2gtfdya74tccb7xw5fdbjdlemmz3v24qzk"
	params = nil
	params = append( params, cid )

    //result_ChainGetMessage = daemon_get_json( "ChainGetMessage", [cid] )
    //fmt.Println( result_ChainGetMessage["result"] )

	request_lotus_node_api( "ChainGetMessage", params, &result_pending_ChainGetMessage )
	fmt.Println( "jsonrpc =" , result_pending_ChainGetMessage.Jsonrpc, ", id =", result_pending_ChainGetMessage.Id, ", result =", result_pending_ChainGetMessage.Result )
	data, _ = json.Marshal( result_pending_ChainGetMessage.Result )
    fmt.Println( "ChainGetMessage (pending) =", string(data) )
    fmt.Println( "" )

	/*
    result:
    {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 2, 'Value': '1000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '101354', 'GasPremium': '100300', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceauqsv73z35kfasyjddbmmxc4b5ui2zxumb7fohyg74g34gnakw2i'}}
	*/


    // replace
	//ReplaceByFeeRatioDefault := result_MpoolGetConfig.Result.(map[string]interface{})["ReplaceByFeeRatio"]
	ReplaceByFeeRatioDefault_float := result_MpoolGetConfig.Result.(map[string]interface{})["ReplaceByFeeRatio"].(float64)
	//
    // SEE: lotus/chain/messagepool/messagepool.go: 179: func ComputeMinRBF(...) {...}
    // - gas_premium = int( int(gas_premium) + ((int(gas_premium) * ((float(ReplaceByFeeRatioDefault) - 1) * 256)) / 256) )
    gas_premium_int = int( float64(gas_premium_int) + ((float64(gas_premium_int) * ((ReplaceByFeeRatioDefault_float - float64(1)) * float64(256))) / float64(256)) )
	//
    //gas_feecap_int = int(222111) // test
    //gas_premium_int = int(111222) // test
    gas_feecap_int = int(gas_premium_int + int((float64(gas_premium_int) * 1.25)/100.0) ) // test
    //
	new_ChainGetMessage := result_pending_ChainGetMessage.Result
    new_ChainGetMessage.(map[string]interface{})["GasFeeCap"] = strconv.Itoa(gas_feecap_int) // not int, string here
    new_ChainGetMessage.(map[string]interface{})["GasPremium"] = strconv.Itoa(gas_premium_int) // not int, string here
    //fmt.Println( "new_ChainGetMessage =", new_ChainGetMessage )
	data, _ = json.Marshal( new_ChainGetMessage )
    fmt.Println( "new_ChainGetMessage =", string(data) )
    fmt.Println( "" )
	

    // sign
	var result_WalletSignMessage types.Result_block
	params = nil
	params = append( params, new_ChainGetMessage.(map[string]interface{})["From"] )
	params = append( params, new_ChainGetMessage )

	request_lotus_node_api( "WalletSignMessage", params, &result_WalletSignMessage )
	fmt.Println( "jsonrpc =" , result_WalletSignMessage.Jsonrpc, ", id =", result_WalletSignMessage.Id, ", result =", result_WalletSignMessage.Result )
    fmt.Println( "" )
	data, _ = json.Marshal( result_WalletSignMessage.Result )
    fmt.Println( "WalletSignMessage (pending) =", string(data) )
    fmt.Println( "" )


    // send
    fmt.Println( "skip..." )
	/*
	var result_MpoolPush types.Result_block
	params = nil
	params = append( params, result_WalletSignMessage.Result )

	request_lotus_node_api( "MpoolPush", params, &result_MpoolPush )
	fmt.Println( "jsonrpc =" , result_MpoolPush.Jsonrpc, ", id =", result_MpoolPush.Id, ", result =", result_MpoolPush.Result )
	fmt.Println( "" )
	data, _ = json.Marshal( result_MpoolPush.Result )
    fmt.Println( "result_MpoolPush (pending) =", string(data) )
    fmt.Println( "" )
	*/

	/*
    result:
    {'jsonrpc': '2.0', 'result': {'/': 'bafy2bzacecltfip2a4j2uvhtn5244kc42kgfy52lb42s53lyxzuwquaktkofc'}, 'id': 0}
	*/



    // Iteration
	/*
    fmt.Println( "Iteration:" )

	var result_iter_MpoolPending types.Result_block
	params = nil
	params = append( params, new([]string) )

	request_lotus_node_api( "MpoolPending", params, &result_iter_MpoolPending )
	//fmt.Println( "jsonrpc =" , result_iter_MpoolPending.Jsonrpc, ", id =", result_iter_MpoolPending.Id, ", result =", result_iter_MpoolPending.Result )
	//fmt.Println( "" )

	count := 0
	for i := 0; i < len(result_iter_MpoolPending.Result.([]interface{})); i++ {
		//fmt.Println( i, ":", result_iter_MpoolPending.Result.([]interface{})[i] )
		from_address := result_iter_MpoolPending.Result.([]interface{})[i].(map[string]interface{})["Message"].(map[string]interface{})["From"]
		//fmt.Println( i, ":", "From address:", from_address )

		for j := 0; j < len(result_WalletList.Result); j++ {
			if from_address == result_WalletList.Result[i] {
				//fmt.Println( count, ":", result_iter_MpoolPending.Result.([]interface{})[i], "\n" )
    			data, _ := json.Marshal( result_iter_MpoolPending.Result.([]interface{})[i] )
				fmt.Println( count, ":", string(data), "\n" )

				// replace
				//ReplaceByFeeRatioDefault := result_MpoolGetConfig.Result.(map[string]interface{})["ReplaceByFeeRatio"]
				ReplaceByFeeRatioDefault_float := result_MpoolGetConfig.Result.(map[string]interface{})["ReplaceByFeeRatio"].(float64)
				//
				// SEE: lotus/chain/messagepool/messagepool.go: 179: func ComputeMinRBF(...) {...}
				// - gas_premium = int( int(gas_premium) + ((int(gas_premium) * ((float(ReplaceByFeeRatioDefault) - 1) * 256)) / 256) )
				gas_premium_int = int( float64(gas_premium_int) + ((float64(gas_premium_int) * ((ReplaceByFeeRatioDefault_float - float64(1)) * float64(256))) / float64(256)) )
				//
				//gas_feecap_int = int(222111) // test
				//gas_premium_int = int(111222) // test
				//gas_feecap_int = int(gas_premium_int + int((float64(gas_premium_int) * 1.25)/100.0) ) // test
				//
				new_ChainGetMessage := result_iter_pending_ChainGetMessage.Result
				new_ChainGetMessage.(map[string]interface{})["Message"].(map[string]interface{})["GasFeeCap"] = strconv.Itoa(gas_feecap_int) // not int, string here
				new_ChainGetMessage.(map[string]interface{})["Message"].(map[string]interface{})["GasPremium"] = strconv.Itoa(gas_premium_int) // not int, string here
				//fmt.Println( "new_ChainGetMessage =", new_ChainGetMessage )
				data, _ = json.Marshal( new_ChainGetMessage )
				fmt.Println( "new_ChainGetMessage =", string(data) )
				fmt.Println( "" )


				// sign
				var result_WalletSignMessage types.Result_block
				params = nil
				params = append( params, new_ChainGetMessage.(map[string]interface{})["Message"].(map[string]interface{})["From"] )
				params = append( params, new_ChainGetMessage.(map[string]interface{})["Message"] )

				request_lotus_node_api( "WalletSignMessage", params, &result_WalletSignMessage )
				//fmt.Println( "jsonrpc =" , result_WalletSignMessage.Jsonrpc, ", id =", result_WalletSignMessage.Id, ", result =", result_WalletSignMessage.Result )
				//fmt.Println( "" )
				//data, _ = json.Marshal( result_WalletSignMessage.Result )
				//fmt.Println( "WalletSignMessage (pending) =", string(data) )
				//fmt.Println( "" )


				// send
				fmt.Println( "skip..." )
				//var result_MpoolPush types.Result_block
				//params = nil
				//params = append( params, result_WalletSignMessage.Result )

				request_lotus_node_api( "MpoolPush", params, &result_MpoolPush )
				//fmt.Println( "jsonrpc =" , result_MpoolPush.Jsonrpc, ", id =", result_MpoolPush.Id, ", result =", result_MpoolPush.Result )
				//fmt.Println( "" )
				//data, _ = json.Marshal( result_MpoolPush.Result )
				//fmt.Println( "result_MpoolPush (pending) =", string(data) )
				//fmt.Println( "" )


				count += 1
			}
		}
	}
	*/



    // ------------------------------------------------------------------------
    // Send
    // ------------------------------------------------------------------------
    // MpoolPush
    // MpoolPushMessage

    fmt.Println( "" )
    fmt.Println( "--------------------------------------" )
    fmt.Println( "[MpoolPushMessage]" )
    fmt.Println( "--------------------------------------" )
	msg_To = "t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q"
    msg_From = "t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy"
    msg_Value = "2" + "000000000000000000" // atto-FIL (1e+18), nano-FIL (1e+9)
    msg_GasLimit = 0 // int64
    msg_GasFeeCap = "0"
    msg_GasPremium = "0"
	message = make( map[string]interface{} )
	message["To"] = string( msg_To )
	message["From"] = string( msg_From )
	message["Value"] = string( msg_Value )
	message["GasLimit"] = int( msg_GasLimit )
	message["GasFeeCap"] = string( msg_GasFeeCap )
	message["GasPremium"] = string( msg_GasPremium )
	msg_MaxFee = "0"
	message_maxfee := make( map[string]string )
    message_maxfee["MaxFee"] = msg_MaxFee
    fmt.Println( "message =", message )
	fmt.Println( "maxfee =" , message_maxfee )
    fmt.Println( "" )
    //
    fmt.Println( "skip..." )
	/*
	var result_MpoolPushMessage types.Result_block
	params = nil
	params = append( params, message )
	params = append( params, message_maxfee )

	request_lotus_node_api( "MpoolPushMessage", params, &result_MpoolPushMessage )
	fmt.Println( "jsonrpc =" , result_MpoolPushMessage.Jsonrpc, ", id =", result_MpoolPushMessage.Id, ", result =", result_MpoolPushMessage.Result )
	fmt.Println( "" )
	data, _ = json.Marshal( result_MpoolPushMessage.Result )
    fmt.Println( "MpoolPushMessage =", string(data) )
	fmt.Println( "" )
	*/


	/*
    result:
    {'jsonrpc': '2.0', 'result': {'Message': {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 1, 'Value': '2', 'GasLimit': 2711147, 'GasFeeCap': '100471', 'GasPremium': '99417', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzacecuwkzzrmpmgb4jjl3beainzbzxy4vy4gxqg4lppba7e47uazjhau'}}, 'Signature': {'Type': 1, 'Data': 'vYg5Kd/pl/ekwbU0Wiv0S2IiLHgSjXRcwkoCWOhSagR9EkPQvfMkPS7XLmmPVnuS4R7BsDaeqaBhDvOACFavkwE='}, 'CID': {'/': 'bafy2bzaced4bfm3uqtwscqrejs7qixj3lexxneazzwxuawgyz7p6onph72ffe'}}, 'id': 3}
	*/

}

