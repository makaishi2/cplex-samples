# -*- coding: utf-8 -*-

# コマンドによる事前準備
# pip install watson-machine-learning-client-V4

import sys
import pandas as pd

# Watson ML credentails
apikey = 'xxxx'
instance_id = 'xxxx'

# DO Deployment ID
deployment_uid = 'xxxx'

# Input CSV File
input_data1 = 'warehouses.csv'
input_data2 = 'supplyCosts.csv'

# --------------------------------------------------------
# メインルーチン
# --------------------------------------------------------
if __name__ == '__main__':

    # 引数の受け取り
    argv = sys.argv
    argc = len(argv)

    wml_credentials = {
        "apikey": apikey,
        "instance_id": instance_id,
        "url": 'https://us-south.ml.cloud.ibm.com'
    }

    from watson_machine_learning_client import WatsonMachineLearningAPIClient
    client = WatsonMachineLearningAPIClient(wml_credentials)

    input_df1 = pd.read_csv(input_data1)
    input_df2 = pd.read_csv(input_data2)
    
    solve_payload = {
        client.deployments.DecisionOptimizationMetaNames.INPUT_DATA: [
            {
                "id": input_data1,
                "values" : input_df1
            },
            {
                "id": input_data2,
                "values" : input_df2
            }
        ],
        client.deployments.DecisionOptimizationMetaNames.OUTPUT_DATA: [
            {
                "id":".*\.csv"
            }
        ]
    }

    # DO Job 投入
    job_details = client.deployments.create_job(deployment_uid, solve_payload)
    job_uid = client.deployments.get_job_uid(job_details)
    print( job_uid )


    #  status確認
    from time import sleep
    while job_details['entity']['decision_optimization']['status']['state'] not in ['completed', 'failed', 'canceled']:
        print(job_details['entity']['decision_optimization']['status']['state'] + '...')
        sleep(5)
        job_details=client.deployments.get_job_details(job_uid)

    detail =  job_details['entity']['decision_optimization']['output_data']

    # 結果確認
    import json
    detail2 =  job_details['entity']['decision_optimization']
    
    # 最終ステータス表示
    print(json.dumps(detail2['status'], indent=2))
    
    # 結果表示
    for item in detail:
        id = item['id']
        fields = item['fields']
        values = item['values']
        df_work = pd.DataFrame(values, columns=fields)
        print(df_work.head(10))
