PYTHON ?= python3
JAVAC ?= javac
JAR ?= jar
SOURCES := $(shell find မူရင်းကုဒ် -name '*.java')
.PHONY: all
all: build/မြန်မာJava.jar
build/မြန်မာJava.jar: $(SOURCES)
	mkdir -p build/classes
	$(JAVAC) --release 11 -encoding UTF-8 -d build/classes $(SOURCES)
	$(JAR) --create --file $@ -C build/classes .

.PHONY: clean
clean:
	rm -rf -- build
