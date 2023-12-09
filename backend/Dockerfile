FROM python

RUN mkdir -p /par/backend
WORKDIR /par/backend
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD b_const.py .
ADD backend.py .
CMD python ./backend.py
