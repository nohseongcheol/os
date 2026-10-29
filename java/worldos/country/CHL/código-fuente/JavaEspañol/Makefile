PYTHON ?= python3
JAVAC ?= javac
JAR ?= jar
SOURCES := $(shell find fuente -name '*.java')
.PHONY: all
all: build/JavaEspañol.jar
build/JavaEspañol.jar: $(SOURCES)
	mkdir -p build/classes
	$(JAVAC) --release 11 -encoding UTF-8 -d build/classes $(SOURCES)
	$(JAR) --create --file $@ -C build/classes .

.PHONY: clean
clean:
	rm -rf -- build
