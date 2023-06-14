.PHONY: build check docs clean

%.txt: %.in
	CUSTOM_COMPILE_COMMAND="make" pip-compile --generate-hashes "$<"

sync: requirements.txt
	pip-sync $^

build:
	python setup.py build_ext --inplace

check:
	python setup.py test

docs:
	make -C docs html

clean:
	rm -rf build
	rm -f src/ringing.cpp
	rm -f ringing*so
	rm -rf ringing_lib.egg-info/
	make -C docs clean
