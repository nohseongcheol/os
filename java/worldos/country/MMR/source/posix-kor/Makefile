PYTHON ?= python3
CC := gcc
AR ?= ar
AS ?= as
LD ?= ld
မူရင်းကုဒ်စာရင်း := $(shell rg --files မူရင်းကုဒ်)
အကောင်အထည်ဖော်မှုအမည်များ := ဖိုင်အဝင်အထွက် 통신종단점 ဘိုက်အက္ခရာစဉ် 사용자진입
အရာဝတ္ထုဖိုင်စာရင်း := $(addprefix build/,$(addsuffix .o,$(အကောင်အထည်ဖော်မှုအမည်များ))) build/운영체제호출.o
အမည်များစမ်းသပ် := 파일규약시험 ဒေတာစာစမ်းသပ် စံအဝင်စမ်းသပ် 파일보존시험
စာရင်းစမ်းသပ် := $(addprefix build/,$(addsuffix .elf,$(အမည်များစမ်းသပ်)))
CFLAGS := -m32 -std=c11 -O2 -ffreestanding -fno-builtin -fno-pie -fno-pic -fno-stack-protector -fno-asynchronous-unwind-tables -fextended-identifiers -nostdinc -Wall -Wextra -Werror -Ibuild/မူရင်းကုဒ်/ခေါင်းစီးဖိုင်
.PHONY: all test test-tools
all: build/libposix-kor.a $(စာရင်းစမ်းသပ်)
build/변환완료: $(မူရင်းကုဒ်စာရင်း) ကိရိယာစု/식별자변환.py
	mkdir -p build
	$(PYTHON) ကိရိယာစု/식별자변환.py မူရင်းကုဒ် build/မူရင်းကုဒ်
	touch $@
build/%.o: build/변환완료
	$(CC) $(CFLAGS) -c build/မူရင်းကုဒ်/အကောင်အထည်ဖော်မှု/$*.c -o $@
build/운영체제호출.o: စက်/운영체제호출.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/သုံးစွဲသူပရိုဂရမ်စတင်.o: စက်/သုံးစွဲသူပရိုဂရမ်စတင်.s
	mkdir -p build
	$(AS) --32 -o $@ $<
build/libposix-kor.a: $(အရာဝတ္ထုဖိုင်စာရင်း)
	$(AR) rcs $@ $^
build/%.elf: build/변환완료 build/သုံးစွဲသူပရိုဂရမ်စတင်.o build/libposix-kor.a ../compiler/သုံးစွဲသူချိတ်နေရာချပုံ.ld
	$(CC) $(CFLAGS) -c build/မူရင်းကုဒ်/စမ်းသပ်မှု/$*.c -o build/$*.o
	$(LD) -m elf_i386 -T ../compiler/သုံးစွဲသူချိတ်နေရာချပုံ.ld -o $@ build/သုံးစွဲသူပရိုဂရမ်စတင်.o build/$*.o build/libposix-kor.a
test:
	$(MAKE) -C ../os test-posix
test-tools:
	$(PYTHON) ကိရိယာစု/변환시험.py

.PHONY: clean
clean:
	rm -rf -- build
