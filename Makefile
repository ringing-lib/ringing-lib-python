.PHONY: build check clean

build:
	python setup.py build_ext --inplace

check:
	python setup.py test

clean:
	rm -f ringing-lib/*.cpp
	rm -f *.so
	rm -rf ringing_lib.egg-info/
