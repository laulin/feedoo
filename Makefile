build: build_pip
	sudo docker build -t feedoo .

build_fast:
	sudo docker build -t feedoofast -f dockerfile_fast .

unittest: build
	sudo docker run -it --rm --net=host --name feedoo feedoo python3 -m unittest discover -s /root/tests -p "test_*.py"

fast_unittest: build_fast
	sudo docker run -it --rm --net=host -v $(shell pwd)/tests:/root/tests -v $(shell pwd)/feedoo:/usr/local/lib/python3.8/dist-packages/feedoo --name feedoo feedoofast python3 -m unittest discover -s /root/tests -p "test_*.py"

run: build
	sudo docker run -it --rm --net=host --name feedoo feedoo feedoo

clear:
	docker images -a | grep none | grep -E -o "[0-9a-f]{12,12}" | xargs docker rmi -f

build_pip:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

clean_pip:
	rm -rf dist/ build/ *.egg-info/