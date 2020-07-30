# -*- coding: utf-8 -*-

# コマンドによる事前準備
# $ pip install watson-machine-learning-client-V4
# $ MACでは次が重要
# $ export COPYFILE_DISABLE=1
# $ tar czvf warehouse-model.tar.gz warehouse_ml.mod

import sys

# Watson ML credentails
apikey = 'xxxx'
instance_id = 'xxxx'

tarfile = 'warehouse-model.tar.gz'

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

    print('List Models')
    client.repository.list_models()

    print('List Deployments')
    client.deployments.list()
    
    # 登録に必要な情報の設定
    mdl_07_metadata = {
        client.repository.ModelMetaNames.NAME: "WAREHOUSE OPL",
        client.repository.ModelMetaNames.DESCRIPTION: "WAREHOUSE OPL",
        #client.repository.ModelMetaNames.TYPE: "do-docplex_12.10",
        client.repository.ModelMetaNames.TYPE: "do-opl_12.10",
        client.repository.ModelMetaNames.RUNTIME_UID: "do_12.10"
    }

    # モデルの登録
    model_details = client.repository.store_model(model=tarfile, meta_props=mdl_07_metadata)

    # モデルUIDの取得
    model_uid = client.repository.get_model_uid(model_details)
    print( model_uid )

    # Webサービス化に必要な情報
    meta_props = {
        client.deployments.ConfigurationMetaNames.NAME: "WAREHOUSE OPL Deployment",
        client.deployments.ConfigurationMetaNames.DESCRIPTION: "WAREHOUSE OPL Deployment",
        client.deployments.ConfigurationMetaNames.BATCH: {},
        client.deployments.ConfigurationMetaNames.COMPUTE: {'name': 'S', 'nodes': 1}
    }

    # Webサービス化
    deployment_details = client.deployments.create(model_uid, meta_props=meta_props)

    deployment_uid = client.deployments.get_uid(deployment_details)
    print( deployment_uid )
    
    client.deployments.list()
    
