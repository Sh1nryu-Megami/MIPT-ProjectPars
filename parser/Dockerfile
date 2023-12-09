FROM python

RUN mkdir -p /par/parser
WORKDIR /par/parser
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD p_const.py .
ADD quaries.py .
ADD parser.py .
CMD python ./parser.py
