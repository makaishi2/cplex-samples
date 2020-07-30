# -*- coding: utf-8 -*-

# コマンドによる事前準備
# $ pip install watson-machine-learning-client-V4
# $ MACでは次が重要
# $ export COPYFILE_DISABLE=1
# $ tar czvf diet-model.tar.gz main.py model.py

import sys

# Watson ML credentails
apikey = 'xxxx'
instance_id = 'xxxx'

tarfile = 'diet-model.tar.gz'

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

    # 登録に必要な情報の設定
    mdl_metadata = {
        client.repository.ModelMetaNames.NAME: "DIET_PYTHON",
        client.repository.ModelMetaNames.DESCRIPTION: "DIET_PYTHON",
        client.repository.ModelMetaNames.TYPE: "do-docplex_12.10",
        #client.repository.ModelMetaNames.TYPE: "do-opl_12.10",
        client.repository.ModelMetaNames.RUNTIME_UID: "do_12.10"
    }

    # モデルの登録
    model_details = client.repository.store_model(model=tarfile, meta_props=mdl_metadata)

    # モデルUIDの取得
    model_uid = client.repository.get_model_uid(model_details)
    print( model_uid )

    # モデルの一覧表示
    print('List Models')
    client.repository.list_models()


    # Webサービス化に必要な情報
    meta_props = {
        client.deployments.ConfigurationMetaNames.NAME: "DIET_PYTHON Deployment",
        client.deployments.ConfigurationMetaNames.DESCRIPTION: "DIET PYTHON Deployment",
        client.deployments.ConfigurationMetaNames.BATCH: {},
        client.deployments.ConfigurationMetaNames.COMPUTE: {'name': 'S', 'nodes': 1}
    }

    # Webサービス化
    deployment_details = client.deployments.create(model_uid, meta_props=meta_props)

    deployment_uid = client.deployments.get_uid(deployment_details)
    print( deployment_uid )
    
    # Webサービスの一覧表示
    client.deployments.list()
    
