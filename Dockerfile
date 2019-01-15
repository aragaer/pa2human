FROM python:3.7-alpine
LABEL "component"="pa2human"

ADD requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ADD pa2human /opt/pa2human/pa2human
ADD human2pa /opt/pa2human/human2pa
ADD pa2human.py /opt/pa2human/pa2human.py
WORKDIR /opt/pa2human/
ENTRYPOINT ["/opt/pa2human/pa2human.py"]
EXPOSE 8001/tcp
CMD ["--socket", ":8001"]
