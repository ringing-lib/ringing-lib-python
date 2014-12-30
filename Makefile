.PHONY: build check docs clean

build:
	python setup.py build_ext --inplace

check:
	python setup.py test

docs:
	make -C docs html

clean:
	rm -rf build
	rm -f src/row.cpp src/change.cpp
	rm -f ringing*so
	rm -rf ringing_lib.egg-info/
	make -C docs clean
