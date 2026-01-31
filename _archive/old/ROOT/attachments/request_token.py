import time
from tf_api_device import TfApiDevice


def request_token():
    tf_api_object = TfApiDevice()
    print(tf_api_object.request_login())
    for i in range(10):
        print("sleep 10s ( %s / 6 )" % str(1 + i))
        time.sleep(10)
        try:
            tf_api_object.request_token()
            print("Received access token")
            return tf_api_object
        except Exception as e:
            pass


if __name__ == '__main__':
    request_token().export_token()