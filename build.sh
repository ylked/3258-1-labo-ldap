#!/bin/bash

build(){
	docker buildx build --tag $1 --platform linux/amd64,linux/arm64 . -f $2 --push
}

build ylked/ldap dockerfiles/ldap-dockerfile
build ylked/ldap-flask dockerfiles/flask-dockerfile
