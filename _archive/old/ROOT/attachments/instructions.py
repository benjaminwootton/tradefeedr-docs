I have attached a client library to allow you to connect to our API from your local Jupyter.

We use Auth0 for authentication and you must follow the steps for "device flow" in the link below to obtain an access token
( https://auth0.com/docs/flows/device-authorization-flow )

You should import the class and follow these steps:

        0.) Create object tf = TfApiDevice()
        1.) Call tf.request_login()
        2.) Visit the url provided by 1.) in a web browser and authenticate
        3.) Call tf.request_token()
        4.) Call tf.query_api(endpoint="", options={}) function to use API