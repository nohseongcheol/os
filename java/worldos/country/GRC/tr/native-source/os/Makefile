PYTHON ?= python3
QEMU ?= qemu-system-i386
AS ?= as
LD ?= ld
SOURCES := $(sort $(wildcard kaynakKod/*.java))
COMPILER := ../compiler/미리번역.sh
COMPILER_SOURCES := $(wildcard ../compiler/자바도구/*)
IP_CONFIG_TOOL := ../platforms/rpi4-native/tools/ip_config.py
NET_ARGS ?= -netdev user,id=net0,$(shell $(PYTHON) $(IP_CONFIG_TOOL) --root .. --qemu) -device rtl8139,netdev=net0
JAVA_FILES ?=
STORE_ARGS ?=
include kullanıcı_alanı/program_f5044b9b.mk
USER_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(APP_NAMES)))
POSIX_NAMES := posixcheck posixudp posixinput posixstore
POSIX_OBJECTS := $(addprefix build/apps/,$(addsuffix .elf,$(POSIX_NAMES)))
USER_SUPPORT := kullanıcı_alanı/bildirim/kullanıcı_alanı.java ../compiler/Start_kullanıcı_program.s ../compiler/kullanıcı_köprü_Düzen.ld ../compiler/CLR_Destek.s $(COMPILER) $(COMPILER_SOURCES)

.PHONY: all iso run run-gui test apps test-network test-java
.PHONY: vbox vbox-status FORCE
all: build/kernel.elf

build:
	mkdir -p build

build/java.o: $(SOURCES) $(COMPILER) $(COMPILER_SOURCES) ../compiler/CLR_Destek.s FORCE | build
	$(PYTHON) $(IP_CONFIG_TOOL) --root .. --java kaynakKod/ağ_Yığın.java build/network-source/ağ_Yığın.java
	sh $(COMPILER) --target kernel --entry Çekirdek.çalıştır --export kernel_dispatch=sistem_çağrısı.işlem_değer_girdi -o $@ $(filter-out kaynakKod/ağ_Yığın.java,$(SOURCES)) build/network-source/ağ_Yığın.java

build/boot.o: makine_başlatma/giriş_noktası_değer.s | build
	$(AS) --32 -o $@ $<

build/java-files.bin: FORCE araçlar/자바파일묶기.py | build
	$(PYTHON) araçlar/자바파일묶기.py -o $@ $(JAVA_FILES)

build/user.o: makine_başlatma/kullanıcı_alanı.s build/java-files.bin | build
	$(AS) --32 -o $@ $<

FORCE:

define APP_RULE
build/apps/$(1).elf: $$(APP_SOURCE_$(1)) $$(USER_SUPPORT)
	sh $$(COMPILER) --target user --entry $$(APP_ENTRY_$(1)) -o $$@ kullanıcı_alanı/bildirim/kullanıcı_alanı.java $$(APP_SOURCE_$(1))
endef
$(foreach app,$(APP_NAMES),$(eval $(call APP_RULE,$(app))))

build/posix-ready: FORCE
	$(MAKE) -C ../posix-kor
	mkdir -p build/apps
	cp -u ../posix-kor/build/Dosya_ABI_test.elf build/apps/posixcheck.elf
	cp -u ../posix-kor/build/veri_birimi_test.elf build/apps/posixudp.elf
	cp -u ../posix-kor/build/STDIN_test.elf build/apps/posixinput.elf
	cp -u ../posix-kor/build/파일보존시험.elf build/apps/posixstore.elf

$(POSIX_OBJECTS): build/posix-ready
	@test -f $@

apps: $(USER_OBJECTS) $(POSIX_OBJECTS)

build/apps.bin: $(USER_OBJECTS) $(POSIX_OBJECTS) kullanıcı_alanı/program_f5044b9b.mk araçlar/BIND_uç_nokta.py
	$(PYTHON) araçlar/BIND_uç_nokta.py -o $@ $(foreach app,$(APP_NAMES) $(POSIX_NAMES),$(app)=build/apps/$(app).elf)

build/apps.o: build/apps.bin makine_başlatma/yürütülebilir_paket_iş.s
	$(AS) --32 -o $@ makine_başlatma/yürütülebilir_paket_iş.s

build/kernel.elf: build/boot.o build/java.o build/user.o build/apps.o makine_başlatma/bağlama_düzeni.ld
	$(LD) -m elf_i386 -T makine_başlatma/bağlama_düzeni.ld -o $@ build/boot.o build/java.o build/user.o build/apps.o
	grub-file --is-x86-multiboot $@

build/kernel.iso: build/kernel.elf makine_başlatma/grub.cfg
	mkdir -p build/iso/boot/grub
	cp build/kernel.elf build/iso/boot/kernel.elf
	cp makine_başlatma/grub.cfg build/iso/boot/grub/grub.cfg
	grub-mkrescue -o $@ build/iso

iso: build/kernel.iso

run: build/kernel.elf
	$(QEMU) -m 64M -kernel $< $(NET_ARGS) $(STORE_ARGS) -display none -serial stdio -monitor none -no-reboot

run-gui: build/kernel.iso
	$(QEMU) -m 64M -cdrom $< $(NET_ARGS) $(STORE_ARGS) -serial stdio -no-reboot

.PHONY: run-store
build/files.img: araçlar/açmak_Depolama_Medya.py | build
	$(PYTHON) araçlar/açmak_Depolama_Medya.py $@
run-store: build/files.img
	$(MAKE) run STORE_ARGS='-drive file=build/files.img,format=raw,if=ide,index=0'

vbox:
	$(MAKE) -C .. vbox

vbox-status:
	$(MAKE) -C .. vbox-status

test: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) sınamalar/paket_test.py
	$(PYTHON) sınamalar/부팅시험.py
	$(PYTHON) sınamalar/test_kullanıcı_ağ.py
	$(PYTHON) sınamalar/자바시험.py
	$(PYTHON) sınamalar/자바파일시험.py
	$(PYTHON) sınamalar/iş_test.py
	$(PYTHON) sınamalar/보존시험.py

.PHONY: test-posix
test-posix: build/kernel.iso
	$(MAKE) -C ../posix-kor test-tools
	$(PYTHON) sınamalar/iş_test.py
	$(PYTHON) sınamalar/보존시험.py
	$(PYTHON) sınamalar/자바파일시험.py

test-java: build/kernel.iso
	$(PYTHON) sınamalar/자바시험.py
	$(PYTHON) sınamalar/자바파일시험.py

test-network: build/kernel.iso
	$(PYTHON) sınamalar/test_kullanıcı_ağ.py

.PHONY: clean
clean:
	# Keep the persistent file-storage disk.
	@if test -d build; then \
		find build -mindepth 1 -maxdepth 1 ! -name files.img -exec rm -rf -- {} +; \
	fi
