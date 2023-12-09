FROM python

RUN mkdir -p /par/frontend
WORKDIR /par/frontend
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD f_const.py .
ADD front.py .
CMD python ./front.py
