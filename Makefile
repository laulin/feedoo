build:
	docker build -t feed .
	docker build -t feedtest -f dockerfile_test .

unittest: build
	docker run --rm --name feedtest feedtest /bin/bash /root/unittest.sh

inttest: build
	docker run --rm --name feedtest feedtest python3 feed.py -v -c /root/tests/conf/feed.yaml

inttest2: build
	rm tests/output/jarvis-2/* || true
	docker run --rm --name feedtest -v $(shell pwd)/tests/input:/input/pihole/jarvis-2 -v $(shell pwd)/tests/output:/output feedtest python3 feed.py -vv -c /root/tests/conf2/feed.yaml

rethinkdb:
	docker run --name rethink --rm -p 8080:8080 -p 28015:28015 -d rethinkdb

clear:
	docker images -a | grep none | grep -E -o "[0-9a-f]{12,12}" | xargs docker rmi -f

build_pip:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

clean_pip:
	rm -rf dist/ build/ *.egg-info/