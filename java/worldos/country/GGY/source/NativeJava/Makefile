PYTHON ?= python3
JAVAC ?= javac
JAR ?= jar
SOURCES := $(shell find source -name '*.java')
.PHONY: all
all: build/NativeJava.jar
build/NativeJava.jar: $(SOURCES)
	mkdir -p build/classes
	$(JAVAC) --release 11 -encoding UTF-8 -d build/classes $(SOURCES)
	$(JAR) --create --file $@ -C build/classes .

.PHONY: clean
clean:
	rm -rf -- build
