자바컴파일러 ?= javac
자바실행기 ?= java
llegat_font_Fitxers := $(shell find llegat_font -type f -name '*.java' | sort)
클래스위치 := RESULTAT/Classe_VALOR
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 allotjar 한글검사 NETEJA_generar generar_IMATGE

모두: 검사

$(완료표시): $(llegat_font_Fitxers)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(llegat_font_Fitxers)
	touch $(완료표시)

한글검사:
	@sh Eines/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Espanya.JEspOS.시험.전체시험

allotjar: 검사
	$(자바실행기) -cp $(클래스위치) Espanya.JEspOS.allotjar.allotjar_inici

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 llegat_font/의 objecte_VALOR 기반 관리 nucli_VALOR 전체를 AOT 변환하는 대상은 아니다.
generar_IMATGE:
	$(MAKE) -C os iso

NETEJA_generar:
	rm -rf RESULTAT
