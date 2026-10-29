자바컴파일러 ?= javac
자바실행기 ?= java
nasljeđe_izvor_Datoteke := $(shell find nasljeđe_izvor -type f -name '*.java' | sort)
클래스위치 := REZULTAT/poduka_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 domaćin 한글검사 CLEAN_međuverzija međuverzija_IMAGE

모두: 검사

$(완료표시): $(nasljeđe_izvor_Datoteke)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(nasljeđe_izvor_Datoteke)
	touch $(완료표시)

한글검사:
	@sh Alati/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Srbija.JSrbOS.시험.전체시험

domaćin: 검사
	$(자바실행기) -cp $(클래스위치) Srbija.JSrbOS.domaćin.domaćin_pokretanje

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 nasljeđe_izvor/의 objekt_VALUE 기반 관리 jezgra_sustava_VALUE 전체를 AOT 변환하는 대상은 아니다.
međuverzija_IMAGE:
	$(MAKE) -C os iso

CLEAN_međuverzija:
	rm -rf REZULTAT
