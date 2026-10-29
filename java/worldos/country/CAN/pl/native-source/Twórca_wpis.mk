자바컴파일러 ?= javac
자바실행기 ?= java
starsze_źródło_Files := $(shell find starsze_źródło -type f -name '*.java' | sort)
Klasa_produkt_wyjściowy_Katalog := WYNIK/Klasa_WARTOŚĆ
완료표시 := $(Klasa_produkt_wyjściowy_Katalog)/.완료

.PHONY: 모두 검사 host 한글검사 OCZYŚĆ_BLD BLD_OBRAZ

모두: 검사

$(완료표시): $(starsze_źródło_Files)
	mkdir -p $(Klasa_produkt_wyjściowy_Katalog)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(Klasa_produkt_wyjściowy_Katalog) $(starsze_źródło_Files)
	touch $(완료표시)

한글검사:
	@sh narzędzia/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(Klasa_produkt_wyjściowy_Katalog) Kanada.JCanOS.testy.전체시험

host: 검사
	$(자바실행기) -cp $(Klasa_produkt_wyjściowy_Katalog) Kanada.JCanOS.host.host_uruchomienie

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 starsze_źródło/의 obiekt_WARTOŚĆ 기반 관리 jądro_WARTOŚĆ 전체를 AOT 변환하는 대상은 아니다.
BLD_OBRAZ:
	$(MAKE) -C os iso

OCZYŚĆ_BLD:
	rm -rf WYNIK
