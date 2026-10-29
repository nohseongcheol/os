자바컴파일러 ?= javac
자바실행기 ?= java
irsi_mənbə_Fayllar := $(shell find irsi_mənbə -type f -name '*.java' | sort)
클래스위치 := ölçü/Sinif_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 host 한글검사 CLEAN_qurmaq qurmaq_IMAGE

모두: 검사

$(완료표시): $(irsi_mənbə_Fayllar)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(irsi_mənbə_Fayllar)
	touch $(완료표시)

한글검사:
	@sh Alətlər/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Ermənistan.JArmOS.시험.전체시험

host: 검사
	$(자바실행기) -cp $(클래스위치) Ermənistan.JArmOS.host.host_yükləmə

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 irsi_mənbə/의 obyekt_VALUE 기반 관리 nüvə_VALUE 전체를 AOT 변환하는 대상은 아니다.
qurmaq_IMAGE:
	$(MAKE) -C os iso

CLEAN_qurmaq:
	rm -rf ölçü
