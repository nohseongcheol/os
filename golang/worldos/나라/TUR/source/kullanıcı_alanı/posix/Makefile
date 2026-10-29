CC ?= gcc
AR ?= ar
CFLAGS := -m32 -ffreestanding -fno-pie -fno-stack-protector -fno-builtin \
	-Wall -Wextra -Werror -nostdinc -Ibildirimler
BUILD := build
OBJECTS := $(BUILD)/syscall.o $(BUILD)/errno.o $(BUILD)/unistd.o \
	$(BUILD)/fcntl.o $(BUILD)/stat.o $(BUILD)/socket.o

.PHONY: all clean check runtime test-programs

all: $(BUILD)/libposix.a

$(BUILD):
	mkdir -p $@

$(BUILD)/errno.o: gerçekleme/hata_numarası.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/unistd.o: gerçekleme/unistd.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/fcntl.o: gerçekleme/dosya_denetimi.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/stat.o: gerçekleme/dosya_durumu.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/socket.o: gerçekleme/socket.c | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD)/syscall.o: gerçekleme/sistem_çağrısı.S | $(BUILD)
	$(CC) -m32 -c $< -o $@

$(BUILD)/crt0.o: gerçekleme/başlatma.S | $(BUILD)
	$(CC) -m32 -c $< -o $@

$(BUILD)/libposix.a: $(OBJECTS)
	$(AR) rcs $@ $^

$(BUILD)/compile-test.o: sınamalar/compile.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -c $< -o $@

check: $(BUILD)/compile-test.o
	@nm -u $(BUILD)/libposix.a | sed '/__syscall6/d' || true

$(BUILD)/runtime.o: sınamalar/runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-runtime: $(BUILD)/runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T bağlama_düzeni.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/runtime.o $(BUILD)/libposix.a

runtime: $(BUILD)/posix-runtime

$(BUILD)/exec-target.o: sınamalar/exec_target.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-exec-target: $(BUILD)/exec-target.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T bağlama_düzeni.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/exec-target.o $(BUILD)/libposix.a

$(BUILD)/exec-runtime.o: sınamalar/exec_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-exec-runtime: $(BUILD)/exec-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T bağlama_düzeni.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/exec-runtime.o $(BUILD)/libposix.a

$(BUILD)/heap-runtime.o: sınamalar/heap_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-heap-runtime: $(BUILD)/heap-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T bağlama_düzeni.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/heap-runtime.o $(BUILD)/libposix.a

$(BUILD)/fork-runtime.o: sınamalar/fork_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-fork-runtime: $(BUILD)/fork-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T bağlama_düzeni.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/fork-runtime.o $(BUILD)/libposix.a

$(BUILD)/stdin-runtime.o: sınamalar/stdin_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-stdin-runtime: $(BUILD)/stdin-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T bağlama_düzeni.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/stdin-runtime.o $(BUILD)/libposix.a

test-programs: runtime $(BUILD)/posix-exec-target $(BUILD)/posix-exec-runtime \
	$(BUILD)/posix-heap-runtime $(BUILD)/posix-fork-runtime \
	$(BUILD)/posix-stdin-runtime $(BUILD)/posix-socket-runtime

$(BUILD)/socket-runtime.o: sınamalar/socket_runtime.c $(BUILD)/libposix.a
	$(CC) $(CFLAGS) -fno-pic -c $< -o $@

$(BUILD)/posix-socket-runtime: $(BUILD)/socket-runtime.o $(BUILD)/crt0.o $(BUILD)/libposix.a
	ld -n -m elf_i386 -e _start -T bağlama_düzeni.ld -static --no-ld-generated-unwind-info \
		-o $@ $(BUILD)/crt0.o $(BUILD)/socket-runtime.o $(BUILD)/libposix.a

clean:
	rm -rf $(BUILD)
