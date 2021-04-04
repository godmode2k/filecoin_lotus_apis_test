# Filecoin Lotus JSON-RPC Test


Summary
----------
> Filecoin Lotus JSON-RPC Test: </br>
> Wallet (WalletSignMessage), Mpool, Estimate Gas, Send, Replacing messages, ... </br>


Environment
----------
> build all and tested on GNU/Linux

    GNU/Linux: Ubuntu 20.04_x64 LTS
    Filecoin Lotus: (Daemon): 1.5.2+2k+git.a54c6bfb0+api1.1.0, (Local): lotus version 1.5.2+2k+git.a54c6bfb0
    Python: v3.8.5
    Go: go1.16.2 linux/amd64
    Network: Filecoin Lotus Local devnet


Run
----------
```sh
// Python version
$ python3 ./lotus_apis_test.py

// Go version
$ cd lotus_apis_test_golang
$ go run ./lotus_apis_example.go



--------------------------------------
[WalletList]
--------------------------------------
Address, Balance
0: Address = "t1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy", 198.99999945621377 FIL
1: Address = "t3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q", 1.0 FIL
2: Address = "t3wqmq6ymuti6vjtd7x5htepaynwokk7plyxfs4m2d2dndqwmnza25o66r5wv6lu73ha5uae3wpbwyjcyxepna", 49479257.99991438 FIL


--------------------------------------
[MpoolPending]
--------------------------------------
0: {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 2, 'Value': '1000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '222111', 'GasPremium': '139027', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceapnhc2wtwb4wldmny6tutgja3n6yrvji5533jy5ywlnsenxhi4ia'}}
1: {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 3, 'Value': '1100000000000000000', 'GasLimit': 657085, 'GasFeeCap': '101691', 'GasPremium': '100637', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceaweh4ocpw6qndxgd4ju64arsope7pbkk7dvrplytmouhfzfs4hru'}}
2: {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 4, 'Value': '2000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '101264', 'GasPremium': '100210', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceboi2pfxgowxzo7keg5cvnmopyopssqcld4skrzxqbu6he2yxhcka'}}


--------------------------------------
[ChainGetMessage]
--------------------------------------
CID = [{'/': 'bafy2bzacea4vvb36j2dndxghv3n47u3rihvqk6bo7dstrmapmlbexilxlj3py'}]
{'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 0, 'Value': '1000000000000000000', 'GasLimit': 2722522, 'GasFeeCap': '101606', 'GasPremium': '100552', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzacedi7gjirpoe2mo27si42ygkdzidgd6ahcqwivdczuli77yygohwoa'}}


--------------------------------------
[GasEstimate]
--------------------------------------
GasEstimateFeeCap = {'jsonrpc': '2.0', 'result': '100', 'id': 3}
GasEstimateGasLimit = {'jsonrpc': '2.0', 'result': 525668, 'id': 3}
MpoolGetConfig = {'jsonrpc': '2.0', 'result': {'PriorityAddrs': None, 'SizeLimitHigh': 30000, 'SizeLimitLow': 20000, 'ReplaceByFeeRatio': 1.25, 'PruneCooldown': 60000000000, 'GasLimitOverestimation': 1.25}, 'id': 3}
GasLimit = (525668 x 1.25) = 525668 (int, truncated)
GasEstimateGasPremium = {'jsonrpc': '2.0', 'result': '199256', 'id': 3}


--------------------------------------
[Replacing messages in the pool]
--------------------------------------
{'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 2, 'Value': '1000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '101354', 'GasPremium': '100300', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceauqsv73z35kfasyjddbmmxc4b5ui2zxumb7fohyg74g34gnakw2i'}}

new_ChainGetMessage = {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 2, 'Value': '1000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '100', 'GasPremium': '249070', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzaceauqsv73z35kfasyjddbmmxc4b5ui2zxumb7fohyg74g34gnakw2i'}}

result_WalletSignMessage = {'jsonrpc': '2.0', 'result': {'Message': {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 2, 'Value': '1000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '100', 'GasPremium': '249070', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzacecvs6waerp6443rrdkoffk3prazgju7tcqgdq4ta2fkp3s6eba7wg'}}, 'Signature': {'Type': 1, 'Data': 'LIK/rM4ToMYDhPEIWLReSrcODf+5ihSKNrm4uOiBd9piuLSd4DCmyVaPUxJCbq9rbXaCird5bt7+z4y4CuLxugA='}, 'CID': {'/': 'bafy2bzacebespz6xedz74oz4svakxwhcwitcossk5p4p3cw2kcchdbuxxv4gk'}}, 'id': 3}

result_WalletSignMessage = {'Message': {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 2, 'Value': '1000000000000000000', 'GasLimit': 657085, 'GasFeeCap': '100', 'GasPremium': '249070', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzacecvs6waerp6443rrdkoffk3prazgju7tcqgdq4ta2fkp3s6eba7wg'}}, 'Signature': {'Type': 1, 'Data': 'LIK/rM4ToMYDhPEIWLReSrcODf+5ihSKNrm4uOiBd9piuLSd4DCmyVaPUxJCbq9rbXaCird5bt7+z4y4CuLxugA='}, 'CID': {'/': 'bafy2bzacebespz6xedz74oz4svakxwhcwitcossk5p4p3cw2kcchdbuxxv4gk'}}

result_MpoolPush = {'jsonrpc': '2.0', 'result': {'/': 'bafy2bzacedz3mefhrexxw4bvzkvt5xghmpukfahz7wbijjkfn3zokqfysdeoy'}, 'id': 3}


--------------------------------------
[MpoolPushMessage]
--------------------------------------
message = 
[{'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Value': '2000000000000000000', 'GasLimit': 0, 'GasFeeCap': '0', 'GasPremium': '0'}, {'MaxFee': '0'}]

result_MpoolPushMessage = {'jsonrpc': '2.0', 'result': {'Message': {'Version': 0, 'To': 't3sm2ujbr5dw6wjff3zz7bplrupon4el35qab2b2iokvn5o5q5co2i2jos3hphdeg3x2qnzikh7qyfczdnww3q', 'From': 't1ce6kwh5rdu3pmvp6rb4z2ge65ryafnl7ciqr5yy', 'Nonce': 1, 'Value': '2', 'GasLimit': 2711147, 'GasFeeCap': '100471', 'GasPremium': '99417', 'Method': 0, 'Params': None, 'CID': {'/': 'bafy2bzacecuwkzzrmpmgb4jjl3beainzbzxy4vy4gxqg4lppba7e47uazjhau'}}, 'Signature': {'Type': 1, 'Data': 'vYg5Kd/pl/ekwbU0Wiv0S2IiLHgSjXRcwkoCWOhSagR9EkPQvfMkPS7XLmmPVnuS4R7BsDaeqaBhDvOACFavkwE='}, 'CID': {'/': 'bafy2bzaced4bfm3uqtwscqrejs7qixj3lexxneazzwxuawgyz7p6onph72ffe'}}, 'id': 3}
```


## Donation
If this project help you reduce time to develop, you can give me a cup of coffee :)

(BitcoinCash) -> bitcoincash:qqls8jsln7w5vzd32g4yrwprstu57aa8rgf4yvsm3m <br>
(Bitcoin) -> 16kC7PUd75rvmwom4oftXRyg3gR9KTPb4m <br>
(Ethereum) -> 0x90B45D2CBBB0367D50590659845C486497F89cBB <br>


