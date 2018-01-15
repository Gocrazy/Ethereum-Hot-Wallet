# Ethereum-Hot-Wallet
* Enviorment
    *  python Go version: 1.9.2
    * Python library: Flask==0.12.1, web3==3.16.4
    * Go version: 1.9.2
    * geth version: v1.8.0-unstable-56152b31
    
* geth command: geth -rpc -rpcaddr "localhost" --rpcport 8545  --rpcapi web3,eth,miner,admin --datadir "./chain" --nodiscover console 2>>eth_output.log 
---
* API:
    - /admin.nodeinfo (require login: basic authenticate user:admin password:1234)
    - /miner method: PUT start miner (require login).
    - /miner method: DELETE stop miner (require login).
    - /block method: GET query block by number.
        - request:
            - number (Integer)
        - response:
            - result
                - {
                    - difficulty  (Integer)
                    - gasLimit (Integer)
                    - gasUsed (Integer)
                    - hash (String)
                    - miner (String)
                    - parentHash (String)
                    - totalDifficulty  (Integer)
                - }
    - /transaction method: GET query transaction by hash.
        - request:
            - hask (String)
        - response:
            - result
                - {
                    - blockHash  (String)
                    - blockNumber (Integer)
                    - from (String)
                    - gas (Integer)
                    - gasPrice (Integer)
                    - hash (String)
                    - nonce (Integer)
                    - to (String) 
                    - value  (Integer)
                - }
    
* Error response format
    - {
        - error: {
              message : "Error message"
        - }
    - }

* Basic http error code
    - 400 for wrong parameter format.
        - {
            - error: {
                  message : "Error message"
            - }
        - }
    - 404 for not found of block, transcation.
        - {
            - error: {
                  message : "Error message"
            - }
            - result : null
        - }
    - 500 for other error which is responsibility of this api server, log.


