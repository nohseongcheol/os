자바컴파일러 ?= javac
자바실행기 ?= java
hen_ffynhonnell_Ffeil := $(shell find hen_ffynhonnell -type f -name '*.java' | sort)
클래스위치 := mesur/Dosbarth_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 lletya 한글검사 Glân_llunio llunio_llun

모두: 검사

$(완료표시): $(hen_ffynhonnell_Ffeil)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(hen_ffynhonnell_Ffeil)
	touch $(완료표시)

한글검사:
	@sh Offer/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Y_Deyrnas_Unedig.JGbrOS.시험.전체시험

lletya: 검사
	$(자바실행기) -cp $(클래스위치) Y_Deyrnas_Unedig.JGbrOS.lletya.lletya_bwtio

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 hen_ffynhonnell/의 gwrthrych_VALUE 기반 관리 cnewyllyn_VALUE 전체를 AOT 변환하는 대상은 아니다.
llunio_llun:
	$(MAKE) -C os iso

Glân_llunio:
	rm -rf mesur
