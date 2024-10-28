FROM alpine:3.20

RUN apk add --no-cache go poetry just
RUN apk add --no-cache gcc musl-dev

ENV CGO_ENABLED=1
 
WORKDIR /task

COPY cucumber ./cucumber
RUN cd cucumber && poetry install
COPY . .

CMD ["just", "test"]
#CMD ["tail", "-f", "/dev/null"]
