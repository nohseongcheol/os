자바컴파일러 ?= javac
자바실행기 ?= java
legatu_iturburu_Fitxategiak := $(shell find legatu_iturburu -type f -name '*.java' | sort)
클래스위치 := EMAITZA/Gela_balio
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 Ostalari 한글검사 GARBITU_eraiki eraiki_irudi

모두: 검사

$(완료표시): $(legatu_iturburu_Fitxategiak)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(legatu_iturburu_Fitxategiak)
	touch $(완료표시)

한글검사:
	@sh Tresnak/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Espainia.JEspOS.시험.전체시험

Ostalari: 검사
	$(자바실행기) -cp $(클래스위치) Espainia.JEspOS.Ostalari.Ostalari_abio

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 legatu_iturburu/의 objektu_balio 기반 관리 nukleo_balio 전체를 AOT 변환하는 대상은 아니다.
eraiki_irudi:
	$(MAKE) -C os iso

GARBITU_eraiki:
	rm -rf EMAITZA
