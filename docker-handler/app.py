import json
from io import BytesIO
import time

import requests
import numpy as np
import onnxruntime
import urllib.request
from PIL import Image

def load_image_from_url(url):
    print(f"Getting image from URL: {url}")
    response = requests.get(url)
    print("Load image into memory")
    img = Image.open(BytesIO(response.content))
    print("Resize image")
    return img.resize((224, 224))

def load_labels(path):
    with open(path) as f:
        data = json.load(f)
    return np.asarray(data)

def preprocess(input_data):
    # convert the input data into the float32 input
    img_data = input_data.astype('float32')

    #normalize
    mean_vec = np.array([0.485, 0.456, 0.406])
    stddev_vec = np.array([0.229, 0.224, 0.225])
    norm_img_data = np.zeros(img_data.shape).astype('float32')
    for i in range(img_data.shape[0]):
        norm_img_data[i,:,:] = (img_data[i,:,:]/255 - mean_vec[i]) / stddev_vec[i]
        
    #add batch channel
    norm_img_data = norm_img_data.reshape(1, 3, 224, 224).astype('float32')
    return norm_img_data

def softmax(x):
    x = x.reshape(-1)
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def postprocess(result):
    return softmax(np.array(result)).tolist()

labels = load_labels('imagenet-simple-labels.json')
session = onnxruntime.InferenceSession('resnet50v2.onnx', None)
input_name = session.get_inputs()[0].name

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    print("Received event: " + json.dumps(event, indent=2))
    body = json.loads(event['body'])
    print(f"Body is: {body}")
    image = load_image_from_url(body['url'])
    image_data = np.array(image).transpose(2, 0, 1)
    input_data = preprocess(image_data)
    start = time.time()
    raw_result = session.run([], {input_name: input_data})
    end = time.time()
    res = postprocess(raw_result)
    inference_time = np.round((end - start) * 1000, 2)
    idx = np.argmax(res)
    result = labels[idx]
    print(f'Result is: {result}')
    print(f'Inference time is: {str(inference_time)} ms')
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "class": result,
                "probability": "%.4f" % res[idx]
            }
        ),
    }
