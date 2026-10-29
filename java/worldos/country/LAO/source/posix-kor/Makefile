PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
원문목록 := $(shell rg --files ແຫຼ່ງທີ່ມາ)
구현이름 := ຟາຍ_ໄອ_ໂອ 통신종단점 ໄບ_ສະຕຣິງ ຜູ້ໃຊ້_ປ້ອນ_ເຂົ້າ
ວັດ_ຖຸ_ຟາຍ_ລາຍຊື່ := $(addprefix build/,$(addsuffix .o,$(구현이름))) build/ລະບົບປະຕິບັດການ_ໂທ.o
시험이름 := 파일규약시험 자료전문시험 표준입력시험 파일보존시험
시험목록 := $(addprefix build/,$(addsuffix .elf,$(시험이름)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/ແຫຼ່ງທີ່ມາ/포함
.PHONY: all test test-tools
all: build/libposix-kor.a $(시험목록)
build/변환완료: $(원문목록) ເຄື່ອງມື/식별자변환.py
	mkdir -p build
	$(PYTHON) ເຄື່ອງມື/식별자변환.py ແຫຼ່ງທີ່ມາ build/ແຫຼ່ງທີ່ມາ
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/ແຫຼ່ງທີ່ມາ/구현/$*.c -o $@
build/ລະບົບປະຕິບັດການ_ໂທ.o: ເຄື່ອງຈັກ/ລະບົບປະຕິບັດການ_ໂທ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/ເລີ່ມ_ຜູ້ໃຊ້_ແອັບ.o: ເຄື່ອງຈັກ/ເລີ່ມ_ຜູ້ໃຊ້_ແອັບ.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(ວັດ_ຖຸ_ຟາຍ_ລາຍຊື່)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/ເລີ່ມ_ຜູ້ໃຊ້_ແອັບ.o build/libposix-kor.a ../compiler/ຜູ້ໃຊ້_ລິ້ງ_ຮູບແບບ.ld
	$(CC) $(CFLAGS) -c build/ແຫຼ່ງທີ່ມາ/시험/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/ຜູ້ໃຊ້_ລິ້ງ_ຮູບແບບ.ld -o $@ build/ເລີ່ມ_ຜູ້ໃຊ້_ແອັບ.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ເຄື່ອງມື/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
