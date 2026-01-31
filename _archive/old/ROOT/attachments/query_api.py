from tf_api_device import TfApiDevice

tf_api_object = TfApiDevice()
tf_api_object.import_token()

endpoint = "test_success"
options = {}

result = tf_api_object.query_api(endpoint, options)
print(result)