# -*- coding: utf-8 -*-

# コマンドによる事前準備
# $ pip install -U ibm-watson-machine-learning 

import sys

# Watson ML credentails
apikey = 'xxxx'
location = 'us-south'

import pandas as pd

# Watson ML credentails

# DO Deployment ID
deployment_uid = 'xxxx'

# Input CSV File
input_data1 = 'diet_food.csv'
input_data2 = 'diet_nutrients.csv'
input_data3 = 'diet_food_nutrients.csv'

# --------------------------------------------------------
# メインルーチン
# --------------------------------------------------------
if __name__ == '__main__':

    # 引数の受け取り
    argv = sys.argv
    argc = len(argv)

    wml_credentials = {
        "apikey": apikey,
        "url": 'https://' + location + '.ml.cloud.ibm.com'
    }

    from ibm_watson_machine_learning import APIClient
    client = APIClient(wml_credentials)

    client.spaces.list()
    space_id = '20f3d4c5-1faa-4c80-a361-4da68d362b0f'
    client.set.default_space(space_id)

    input_df1 = pd.read_csv(input_data1)
    input_df2 = pd.read_csv(input_data2)
    input_df3 = pd.read_csv(input_data3)
    
    solve_payload = {
        client.deployments.DecisionOptimizationMetaNames.INPUT_DATA: [
            {
                "id": input_data1,
                "values" : input_df1
            },
            {
                "id": input_data2,
                "values" : input_df2
            },
            {
                "id": input_data3,
                "values" : input_df3
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
    
    for item in detail:
        id = item['id']
        fields = item['fields']
        values = item['values']
        df_work = pd.DataFrame(values, columns=fields)
        name = id[:id.index('.csv')]
        print('name = ', name)
        print(df_work.head())
        df_work.to_csv(id, index=False)
