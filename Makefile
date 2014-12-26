.PHONY: build clean

build:
	python setup.py build_ext --inplace

clean:
	rm -f ringing-lib/*.cpp
	rm -f *.so
