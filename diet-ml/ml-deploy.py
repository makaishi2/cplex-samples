# -*- coding: utf-8 -*-

# コマンドによる事前準備
# $ pip install -U ibm-watson-machine-learning 
# $ MACでは次が重要
# $ export COPYFILE_DISABLE=1
# $ tar czvf diet-model.gz main.py model.py
# main.py 共通に使われるmodel呼び出し用コード
# model.py DO実装コード model.builderで動作確認したもの

import sys

# Watson ML credentails
apikey = 'xxxx'
location = 'us-south'

tarfile = 'diet-model.gz'

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
    space_id = 'xxxx'
    client.set.default_space(space_id)
    
    software_spec_uid = client.software_specifications.get_uid_by_name("do_12.10")
    print(software_spec_uid)
    
    # 登録に必要な情報の設定
    mdl_metadata = {
        client.repository.ModelMetaNames.NAME: "Diet Python",
        client.repository.ModelMetaNames.DESCRIPTION: "Diet Python",
        client.repository.ModelMetaNames.TYPE: "do-docplex_12.10",
        client.repository.ModelMetaNames.SOFTWARE_SPEC_UID: software_spec_uid
    }

    # モデルの登録
    model_details = client.repository.store_model(model=tarfile, meta_props=mdl_metadata)

    # モデルUIDの取得
    model_uid = client.repository.get_model_uid(model_details)
    print( model_uid )

    # Webサービス化に必要な情報
    
    meta_props = {
        client.deployments.ConfigurationMetaNames.NAME: "Diet Python Web",
        client.deployments.ConfigurationMetaNames.DESCRIPTION: "Diet Python Web",
        client.deployments.ConfigurationMetaNames.BATCH: {},
        client.deployments.ConfigurationMetaNames.HARDWARE_SPEC: {'name': 'S', 'nodes': 1}  # S / M / XL
    }

    # Webサービス化
    deployment_details = client.deployments.create(model_uid, meta_props=meta_props)

    deployment_uid = client.deployments.get_uid(deployment_details)
    print( deployment_uid )
    
    # Webサービスの一覧表示
    client.deployments.list()
