FROM alpine
RUN apk add curl 
COPY test.sh /data/test.sh
WORKDIR /data
RUN chmod +x test.sh
CMD ./test.sh
