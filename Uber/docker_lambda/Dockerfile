FROM public.ecr.aws/lambda/python:3.7

RUN pip3 install --upgrade pip
COPY app.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt .


COPY data ${LAMBDA_TASK_ROOT}

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["app.handler"]