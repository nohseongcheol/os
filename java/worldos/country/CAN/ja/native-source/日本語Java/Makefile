PYTHON ?= python3
JAVAC ?= javac
JAR ?= jar
SOURCES := $(shell find ソース -name '*.java')
.PHONY: all
all: build/日本語Java.jar
build/日本語Java.jar: $(SOURCES)
	mkdir -p build/classes
	$(JAVAC) --release 11 -encoding UTF-8 -d build/classes $(SOURCES)
	$(JAR) --create --file $@ -C build/classes .

.PHONY: clean
clean:
	rm -rf -- build
