PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard မူရင်းကုဒ်/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/Javaကိရိယာ/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include သုံးစွဲသူ/ပရိုဂရမ်.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := သုံးစွဲသူ/ကြေညာချက်/သုံးစွဲသူ.java ../compiler/သုံးစွဲသူပရိုဂရမ်စတင်.s ../compiler/သုံးစွဲသူချိတ်နေရာချပုံ.ld ../compiler/လည်ပတ်ဝန်းကျင်ထောက်ပံ့မှု.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/လည်ပတ်ဝန်းကျင်ထောက်ပံ့မှု.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java မူရင်းကုဒ်/ကွန်ရက်အလွှာစု.java build/network-source/ကွန်ရက်အလွှာစု.java
	sh $(COMPILER) --target kernel --entry အူတိုင်.လုပ်ဆောင် --export kernel_dispatch=စနစ်ခေါ်ဆိုမှု.လုပ်ငန်းစဉ်တန်ဖိုးအချက် -o $@ $(filter-out မူရင်းကုဒ်/ကွန်ရက်အလွှာစု.java,$(SOURCES)) build/network-source/ကွန်ရက်အလွှာစု.java

build/boot.o: စက်တင်/အချက်အမှတ်တစ်ခုတန်ဖိုး.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE ကိရိယာစု/Javaဖိုင်ထုပ်ပိုး.py | build
	$(PYTHON) ကိရိယာစု/Javaဖိုင်ထုပ်ပိုး.py -o $@ $(JAVA_FILES)

build/user.o: စက်တင်/သုံးစွဲသူ.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ သုံးစွဲသူ/ကြေညာချက်/သုံးစွဲသူ.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/파일규약시험.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/ဒေတာစာစမ်းသပ်.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/စံအဝင်စမ်းသပ်.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) သုံးစွဲသူ/ပရိုဂရမ်.mk ကိရိယာစု/စက်ဖိုင်ထုပ်ပိုး.py
	$(PYTHON) ကိရိယာစု/စက်ဖိုင်ထုပ်ပိုး.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin စက်တင်/စက်ဖိုင်အထုပ်.s
	$(AS) --32 -o $@ စက်တင်/စက်ဖိုင်အထုပ်.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o စက်တင်/နေရာချထားပုံ.ld
	$(LD) -m elf_i386 -T စက်တင်/နေရာချထားပုံ.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf စက်တင်/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp စက်တင်/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: ကိရိယာစု/သိုလှောင်မီဒီယာဖန်တီး.py | build
	$(PYTHON) ကိရိယာစု/သိုလှောင်မီဒီယာဖန်တီး.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) စမ်းသပ်မှု/ဒေတာထုပ်စမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/စက်တင်စမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/သုံးစွဲဆက်သွယ်စမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/Javaစမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/Javaဖိုင်စမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/စည်းမျဉ်းစမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/ထိန်းသိမ်းမှုစမ်းသပ်.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) စမ်းသပ်မှု/စည်းမျဉ်းစမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/ထိန်းသိမ်းမှုစမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/Javaဖိုင်စမ်းသပ်.py

test-java: build/kernel.iso
	$(PYTHON) စမ်းသပ်မှု/Javaစမ်းသပ်.py
	$(PYTHON) စမ်းသပ်မှု/Javaဖိုင်စမ်းသပ်.py

test-network: build/kernel.iso
	$(PYTHON) စမ်းသပ်မှု/သုံးစွဲဆက်သွယ်စမ်းသပ်.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
