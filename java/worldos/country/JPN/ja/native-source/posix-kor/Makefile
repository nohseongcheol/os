PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
ソース一覧 := $(shell rg --files ソース)
実装名前一覧 := ファイル入力出力 ソケット通信端点 バイト文字列 利用者入場
オブジェクトファイル一覧 := $(addprefix build/,$(addsuffix .o,$(実装名前一覧))) build/稼働システム呼出し一覧.o
名前一覧試験 := ファイルABI試験 データグラム試験 標準入力試験 ファイル保持状態試験
一覧試験 := $(addprefix build/,$(addsuffix .elf,$(名前一覧試験)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ソース/ヘッダー
.PHONY: all test test-tools
all: build/libposix-kor.a $(一覧試験)
build/変換結果完了: $(ソース一覧) 道具/識別子変換結果.py
	mkdir -p build
	$(PYTHON) 道具/識別子変換結果.py ソース build/ソース
	touch $@
build/%.o: build/変換結果完了
	$(CC) $(CFLAGS) -c build/ソース/実装/$*.c -o $@
build/稼働システム呼出し一覧.o: 機械/稼働システム呼出し一覧.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/利用者プログラム開始処理.o: 機械/利用者プログラム開始処理.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(オブジェクトファイル一覧)
	$(AR) rcs $@ $^
build/%.elf: build/変換結果完了 build/利用者プログラム開始処理.o build/libposix-kor.a ../compiler/利用者連結配置.ld
	$(CC) $(CFLAGS) -c build/ソース/試験/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/利用者連結配置.ld -o $@ build/利用者プログラム開始処理.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) 道具/変換結果試験.py

.PHONY: clean
clean:
	rm -rf -- build
