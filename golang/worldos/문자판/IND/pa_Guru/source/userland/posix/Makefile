CC ?= gcc
AR ?= ar
CFLAGS := -m32 -ffreestanding -fno-pie -fno-stack-protector -fno-builtin \
	-Wall -Wextra -Werror -nostdinc -Iheaders
BUILD := build
OBJECTS := $(BUILD)/syscall.o $(BUILD)/errno.o $(BUILD)/unistd.o \
	$(BUILD)/fcntl.o $(BUILD)/stat.o $(BUILD)/socket.o

.PHONY: all clean check runtime test-programs

all: $(BUILD)/libposix.a

$(BUILD):
	mkdir -p $@

$(BUILD)/errno.o: src/errno.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/unistd.o: src/unistd.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/fcntl.o: src/fcntl.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/stat.o: src/stat.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/socket.o: src/socket.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/syscall.o: src/syscall.S | $(BUILD)
	$(CC) -m32 -c $< -o $@

$(BUILD)/crt0.o: src/crt0.S | $(BUILD)
	$(CC) -m32 -c $< -o $@

$(BUILD)/libposix.a: $(OBJECTS)
	$(AR) rcs $@ $^

$(BUILD)/compile-test.o: ਜਾਂਚ/compile.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -c $< -o $@

check: $(BUILD)/compile-test.o
	@nm -u $(BUILD)/libposix.a | sed '/__syscall6/d' || true

$(BUILD)/runtime.o: ਜਾਂਚ/runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-runtime: $(BUILD)/runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T linker.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/runtime.o $(BUILD)/libposix.a

runtime: $(BUILD)/posix-runtime

$(BUILD)/exec-target.o: ਜਾਂਚ/exec_target.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-exec-target: $(BUILD)/exec-target.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T linker.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/exec-target.o $(BUILD)/libposix.a

$(BUILD)/exec-runtime.o: ਜਾਂਚ/exec_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-exec-runtime: $(BUILD)/exec-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T linker.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/exec-runtime.o $(BUILD)/libposix.a

$(BUILD)/heap-runtime.o: ਜਾਂਚ/heap_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-heap-runtime: $(BUILD)/heap-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T linker.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/heap-runtime.o $(BUILD)/libposix.a

$(BUILD)/fork-runtime.o: ਜਾਂਚ/fork_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-fork-runtime: $(BUILD)/fork-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T linker.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/fork-runtime.o $(BUILD)/libposix.a

$(BUILD)/stdin-runtime.o: ਜਾਂਚ/stdin_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-stdin-runtime: $(BUILD)/stdin-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T linker.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/stdin-runtime.o $(BUILD)/libposix.a

test-programs: runtime $(BUILD)/posix-exec-target $(BUILD)/posix-exec-runtime \
	$(BUILD)/posix-heap-runtime $(BUILD)/posix-fork-runtime \
	$(BUILD)/posix-stdin-runtime $(BUILD)/posix-socket-runtime

$(BUILD)/socket-runtime.o: ਜਾਂਚ/socket_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-socket-runtime: $(BUILD)/socket-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T linker.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/socket-runtime.o $(BUILD)/libposix.a

clean:
	rm -rf $(BUILD)
