# -*- coding: utf-8 -*-

# コマンドによる事前準備
# $ pip install watson-machine-learning-client-V4

import sys

# Watson ML credentails
apikey = 'xxxx'
instance_id = 'xxxx'

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
