FROM public.ecr.aws/lambda/python:3.8

RUN python3.8 -m pip install onnxruntime requests Pillow numpy -t .

COPY requirements.txt *.onnx *.json ./

COPY app.py ./

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
