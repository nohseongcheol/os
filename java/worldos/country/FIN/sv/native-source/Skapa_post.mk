자바컴파일러 ?= javac
자바실행기 ?= java
äldre_källa_Filer := $(shell find äldre_källa -type f -name '*.java' | sort)
Kurs_utleverans_Katalog := RESULTAT/Kurs_värde
완료표시 := $(Kurs_utleverans_Katalog)/.완료

.PHONY: 모두 검사 värd 한글검사 Rent_version version_BILD

모두: 검사

$(완료표시): $(äldre_källa_Filer)
	mkdir -p $(Kurs_utleverans_Katalog)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(Kurs_utleverans_Katalog) $(äldre_källa_Filer)
	touch $(완료표시)

한글검사:
	@sh verktyg/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(Kurs_utleverans_Katalog) Finland.JFinOS.tester.전체시험

värd: 검사
	$(자바실행기) -cp $(Kurs_utleverans_Katalog) Finland.JFinOS.värd.värd_start

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 äldre_källa/의 objekt_värde 기반 관리 kärna_värde 전체를 AOT 변환하는 대상은 아니다.
version_BILD:
	$(MAKE) -C os iso

Rent_version:
	rm -rf RESULTAT
