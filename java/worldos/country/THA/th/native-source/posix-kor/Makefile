PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files รหัสต้นฉบับ)
구현이름 := แฟ้ม_รับเข้า_ส่งออก 통신종단점 ไบต์_สตริง ผู้ใช้_ใส่
วัตถุ_แฟ้ม_รายการ := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ระบบปฏิบัติการ_การโทร.o
시험이름 := 파일규약시험 เดตาแกรม_การทดสอบ อุปกรณ์นําเข้าข้อมูลมาตรฐาน_การทดสอบ 파일보존시험
รายการทดสอบ := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/รหัสต้นฉบับ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(รายการทดสอบ)
build/변환완료: $(원문목록) เครื่องมือ/ตัวระบุ_การแปลง.py
	mkdir -p build
	$(PYTHON) เครื่องมือ/ตัวระบุ_การแปลง.py รหัสต้นฉบับ build/รหัสต้นฉบับ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/รหัสต้นฉบับ/구현/$*.c -o $@
build/ระบบปฏิบัติการ_การโทร.o: เครื่อง/ระบบปฏิบัติการ_การโทร.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/เริ่ม_ผู้ใช้_แอป.o: เครื่อง/เริ่ม_ผู้ใช้_แอป.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(วัตถุ_แฟ้ม_รายการ)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/เริ่ม_ผู้ใช้_แอป.o build/libposix-kor.a ../compiler/ผู้ใช้_ลิงก์_การนําทาง.ld
	$(CC) $(CFLAGS) -c build/รหัสต้นฉบับ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ผู้ใช้_ลิงก์_การนําทาง.ld -o $@ build/เริ่ม_ผู้ใช้_แอป.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) เครื่องมือ/การแปลง_การทดสอบ.py

.PHONY: clean
clean:
	rm -rf -- build
