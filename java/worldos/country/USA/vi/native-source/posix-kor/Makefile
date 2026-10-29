PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
DanhSáchMãNguồn := $(shell rg --files mãNguồn)
cácTênPhầnCàiĐặt := ĐầuRaĐầuVàoTệp ĐiểmCuốiỔCắmMạng ChuỗiByte vàoNgườiDùng
danhSáchTệpĐốiTượng := $(addprefix build/,$(addsuffix .o,$(cácTênPhầnCàiĐặt))) build/CácLờiGọiHệThốngĐiềuHành.o
thửCácTên := ThửABITệp ThửĐiệnDữLiệu ThửĐầuVàoChuẩn ThửViệcGiữNguyênTệp
thửDanhSách := $(addprefix build/,$(addsuffix .elf,$(thửCácTên)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/mãNguồn/TệpĐầuMục
.PHONY: all test test-tools
all: build/libposix-kor.a $(thửDanhSách)
build/đầyĐủPhépChuyểnĐổi: $(DanhSáchMãNguồn) CôngCụ/PhépChuyểnĐổiĐịnhDanh.py
	mkdir -p build
	$(PYTHON) CôngCụ/PhépChuyểnĐổiĐịnhDanh.py mãNguồn build/mãNguồn
	touch $@
build/%.o: build/đầyĐủPhépChuyểnĐổi
	$(CC) $(CFLAGS) -c build/mãNguồn/phầnCàiĐặt/$*.c -o $@
build/CácLờiGọiHệThốngĐiềuHành.o: máy/CácLờiGọiHệThốngĐiềuHành.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/bắtChạyChươngTrìnhNgườiDùng.o: máy/bắtChạyChươngTrìnhNgườiDùng.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(danhSáchTệpĐốiTượng)
	$(AR) rcs $@ $^
build/%.elf: build/đầyĐủPhépChuyểnĐổi build/bắtChạyChươngTrìnhNgườiDùng.o build/libposix-kor.a ../compiler/bốTríLiênKếtNgườiDùng.ld
	$(CC) $(CFLAGS) -c build/mãNguồn/KiểmThử/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/bốTríLiênKếtNgườiDùng.ld -o $@ build/bắtChạyChươngTrìnhNgườiDùng.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) CôngCụ/ThửPhépChuyểnĐổi.py

.PHONY: clean
clean:
	rm -rf -- build
