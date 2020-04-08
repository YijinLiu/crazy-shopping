WORK_DIR:=$(shell readlink -f $(dir $(lastword $(MAKEFILE_LIST))))

default:
	cd $(WORK_DIR)
	docker build -t $(USER)/crazy-shopping:`date '+%Y-%m-%d'` \
	    --build-arg NAME=${USER} --build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) .
