FROM public.ecr.aws/lambda/python:3.12

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY game_scraper_logo.png .
COPY Jersey15-Regular.ttf .
COPY generate_report.py .

CMD [ "generate_report.handler" ]