PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
源代码列表 := $(shell rg --files 源代码)
实现名称列 := 文件输入输出 套接字端点 字节字符串 用户进入
对象文件列表 := $(addprefix build/,$(addsuffix .o,$(实现名称列))) build/运行系统调用列.o
测试名称列 := 文件ABI测试 数据报测试 标准输入测试 文件保留状态测试
测试列表 := $(addprefix build/,$(addsuffix .elf,$(测试名称列)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/源代码/头文件
.PHONY: all test test-tools
all: build/libposix-kor.a $(测试列表)
build/转换结果完成: $(源代码列表) 工具集/标识符转换结果.py
	mkdir -p build
	$(PYTHON) 工具集/标识符转换结果.py 源代码 build/源代码
	touch $@
build/%.o: build/转换结果完成
	$(CC) $(CFLAGS) -c build/源代码/实现/$*.c -o $@
build/运行系统调用列.o: 计算机/运行系统调用列.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/开始用户程序.o: 计算机/开始用户程序.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(对象文件列表)
	$(AR) rcs $@ $^
build/%.elf: build/转换结果完成 build/开始用户程序.o build/libposix-kor.a ../compiler/用户连接导航.ld
	$(CC) $(CFLAGS) -c build/源代码/测试/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/用户连接导航.ld -o $@ build/开始用户程序.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) 工具集/转换结果测试.py

.PHONY: clean
clean:
	rm -rf -- build
