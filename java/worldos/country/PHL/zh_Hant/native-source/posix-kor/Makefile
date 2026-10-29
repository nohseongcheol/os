PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
原始碼列表 := $(shell rg --files 原始碼)
實現名稱列 := 檔案輸入輸出 通訊端端點 位元組字符串 用戶進入
物件檔案列表 := $(addprefix build/,$(addsuffix .o,$(實現名稱列))) build/運行系統調用列.o
測試名稱列 := 檔案ABI測試 數據報測試 標準輸入測試 檔案保留狀態測試
測試列表 := $(addprefix build/,$(addsuffix .elf,$(測試名稱列)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/原始碼/頭文件
.PHONY: all test test-tools
all: build/libposix-kor.a $(測試列表)
build/轉換結果完成: $(原始碼列表) 工具集/標識符轉換結果.py
	mkdir -p build
	$(PYTHON) 工具集/標識符轉換結果.py 原始碼 build/原始碼
	touch $@
build/%.o: build/轉換結果完成
	$(CC) $(CFLAGS) -c build/原始碼/實現/$*.c -o $@
build/運行系統調用列.o: 計算機/運行系統調用列.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/開始用戶程式.o: 計算機/開始用戶程式.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(物件檔案列表)
	$(AR) rcs $@ $^
build/%.elf: build/轉換結果完成 build/開始用戶程式.o build/libposix-kor.a ../compiler/用戶連接導航.ld
	$(CC) $(CFLAGS) -c build/原始碼/測試/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/用戶連接導航.ld -o $@ build/開始用戶程式.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) 工具集/轉換結果測試.py

.PHONY: clean
clean:
	rm -rf -- build
