CC ?= gcc
AR ?= ar
CFLAGS := -m32 -ffreestanding -fno-pie -fno-stack-protector -fno-builtin \
	-Wall -Wextra -Werror -nostdinc -Iоголошення
BUILD := build
OBJECTS := $(BUILD)/syscall.o $(BUILD)/errno.o $(BUILD)/unistd.o \
	$(BUILD)/fcntl.o $(BUILD)/stat.o $(BUILD)/socket.o

.PHONY: all clean check runtime test-programs

all: $(BUILD)/libposix.a

$(BUILD):
	mkdir -p $@

$(BUILD)/errno.o: реалізація/номер_помилки.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/unistd.o: реалізація/unistd.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/fcntl.o: реалізація/керування_файлом.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/stat.o: реалізація/стан_файла.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/socket.o: реалізація/socket.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/syscall.o: реалізація/системний_виклик.S | $(BUILD)
	$(CC) -m32 -c $< -o $@

$(BUILD)/crt0.o: реалізація/запуск.S | $(BUILD)
	$(CC) -m32 -c $< -o $@

$(BUILD)/libposix.a: $(OBJECTS)
	$(AR) rcs $@ $^

$(BUILD)/compile-test.o: випробування/compile.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -c $< -o $@

check: $(BUILD)/compile-test.o
	@nm -u $(BUILD)/libposix.a | sed '/__syscall6/d' || true

$(BUILD)/runtime.o: випробування/runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-runtime: $(BUILD)/runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T схема_компонування.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/runtime.o $(BUILD)/libposix.a

runtime: $(BUILD)/posix-runtime

$(BUILD)/exec-target.o: випробування/exec_target.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-exec-target: $(BUILD)/exec-target.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T схема_компонування.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/exec-target.o $(BUILD)/libposix.a

$(BUILD)/exec-runtime.o: випробування/exec_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-exec-runtime: $(BUILD)/exec-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T схема_компонування.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/exec-runtime.o $(BUILD)/libposix.a

$(BUILD)/heap-runtime.o: випробування/heap_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-heap-runtime: $(BUILD)/heap-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T схема_компонування.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/heap-runtime.o $(BUILD)/libposix.a

$(BUILD)/fork-runtime.o: випробування/fork_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-fork-runtime: $(BUILD)/fork-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T схема_компонування.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/fork-runtime.o $(BUILD)/libposix.a

$(BUILD)/stdin-runtime.o: випробування/stdin_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-stdin-runtime: $(BUILD)/stdin-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T схема_компонування.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/stdin-runtime.o $(BUILD)/libposix.a

test-programs: runtime $(BUILD)/posix-exec-target $(BUILD)/posix-exec-runtime \
	$(BUILD)/posix-heap-runtime $(BUILD)/posix-fork-runtime \
	$(BUILD)/posix-stdin-runtime $(BUILD)/posix-socket-runtime

$(BUILD)/socket-runtime.o: випробування/socket_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-socket-runtime: $(BUILD)/socket-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T схема_компонування.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/socket-runtime.o $(BUILD)/libposix.a

clean:
	rm -rf $(BUILD)
