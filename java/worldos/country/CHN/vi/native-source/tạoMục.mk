TrìnhBiênDịchJava ?= javac
trìnhKhởiChạyJava ?= java
cácTệpNguồnKếThừa := $(shell find NguồnNềnTảng -type f -name '*.java' | sort)
thưMụcĐầuRaLớp := kếtQuả/giáTrịLớp
dấuMốcHoànTất := $(thưMụcĐầuRaLớp)/.làĐầyĐủ

.PHONY: xâyDựngTấtCả CácPhépKiểmTra Chủ kiểmTraHangul xâyDựngSạch xâyDựngẢnh

xâyDựngTấtCả: CácPhépKiểmTra

$(dấuMốcHoànTất): $(cácTệpNguồnKếThừa)
	mkdir -p $(thưMụcĐầuRaLớp)
	$(TrìnhBiênDịchJava) -encoding UTF-8 -Xlint:all -Werror -d $(thưMụcĐầuRaLớp) $(cácTệpNguồnKếThừa)
	touch $(dấuMốcHoànTất)

kiểmTraHangul:
	@sh CôngCụ/KiểmTênĐịnhDanh.sh

CácPhépKiểmTra: kiểmTraHangul $(dấuMốcHoànTất)
	$(trìnhKhởiChạyJava) -ea -cp $(thưMụcĐầuRaLớp) Trung_Quốc.JChnOS.KiểmThử.thửTấtCả

Chủ: CácPhépKiểmTra
	$(trìnhKhởiChạyJava) -cp $(thưMụcĐầuRaLớp) Trung_Quốc.JChnOS.Chủ.lúcKhởiChạyChủ

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 NguồnNềnTảng/의 giáTrịĐốiTượng nềnTảng 관리 giáTrịNhân 전체를 AOT 변환하는 대상은 아니다.
xâyDựngẢnh:
	$(MAKE) -C os iso

xâyDựngSạch:
	rm -rf kếtQuả
