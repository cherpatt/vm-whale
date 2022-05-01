import datetime
from datetime import timedelta

def get_address():
    x = datetime.date.today()
    start_lastmonth = (x.replace(day=1) - timedelta(days=1)).replace(day= 1)
    start_thismonth = x.replace(day=1) 

    from google.cloud import bigquery
    client = bigquery.Client.from_service_account_json('./thesis-328311-e3e617ef9cad.json')

    # Construct a BigQuery client object.
    query_sql = f"SELECT from_address FROM `bigquery-public-data.crypto_ethereum.transactions` WHERE DATE(block_timestamp) >='{start_lastmonth}' and DATE(block_timestamp) <='{start_thismonth}' GROUP BY from_address ORDER BY sum(cast(value as float64)) desc LIMIT 25"
    query_job = client.query(query_sql)  # API request
    rows = query_job.result()

    address_all = []
    for row in rows:
        address_all.append(row.get('from_address'))

    cex = ['0x28c6c06298d514db089934071355e5743bf21d60','0x53d284357ec70ce289d6d64134dfac8e511c8a3d','0x876eabf441b2ee5b5b0554fd502a8e0600950cfa',
            '0xc098b2a3aa256d2140208c3de6543aaef5cd3a94','0x56eddb7aa87536c09ccc2793473599fd21a8b17f','0xddfabcdc4d8ffc6d5beaf154f18b778f892a0740',
            '0xd24400ae8bfebb18ca49be86258a3c749cf46853','0x4976a4a02f38326660d17bf34b431dc6e2eb2327','0xb5d85cbf7cb3ee0d56b3bb207d5fc4b82f43f511',
            '0xeb2629a2734e272bcc07bda959863f316f4bd4cf','0x3cd751e6b0078be393132286c442345e5dc49699','0x9696f59e4d72e237be84ffd425dcad154bf96976',
            '0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0','0x742d35cc6634c0532925a3b844bc454e4438f44e','0xdfd5293d8e347dfe59e90efd55b2956a1343963d',
            '0xe853c56864a2ebe4576a807d26fdc4a0ada51919','0x21a31ee1afc51d94c2efccaa2092ad1028285549','0x0548f59fee79f8832c299e01dca5c76f034f558e',
            '0xa7efae728d2936e78bda97dc267687568dd593f3','0xb4cd0386d2db86f30c1a11c2b8c4f4185c1dade9','0xf977814e90da44bfa03b6295a0616a897441acec',
            '0x229b5c097f9b35009ca1321ad2034d4b3d5070f6','0xdc76cd25977e0a5ae17155770273ad58648900d3','0x65b0bf8ee4947edd2a500d74e50a3d757dc79de0',
            '0xf66852bc122fd40bfecc63cd48217e88bda12109','0x4f6742badb049791cd9a37ea913f2bac38d01279','0x712d0f306956a6a4b4f9319ad9b9de48c5345996',
            '0xc5ed2333f8a2c351fca35e5ebadb2a82f5d254c3','0x6262998ced04146fa42253a5c0af90ca02dfd2a3']

    addresses_list = list(set(address_all) - set(cex))
    addresses_list = addresses_list[:3]
    return addresses_list
    