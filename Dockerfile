FROM python:2.7.18-stretch

RUN mkdir /automata
WORKDIR /automata
COPY ./ /automata
RUN pip install -r requirements.txt

EXPOSE 5001 8080 9000
ENTRYPOINT ["python", "auto.py"]
CMD ["handler"]
