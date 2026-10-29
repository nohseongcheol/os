자바컴파일러 ?= javac
자바실행기 ?= java
vanha_lähde_Files := $(shell find vanha_lähde -type f -name '*.java' | sort)
Luokka_tulos_Directory := TULOS/Luokka_ARVO
완료표시 := $(Luokka_tulos_Directory)/.완료

.PHONY: 모두 검사 isäntä 한글검사 SIIVOA_kääntää kääntää_KUVA

모두: 검사

$(완료표시): $(vanha_lähde_Files)
	mkdir -p $(Luokka_tulos_Directory)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(Luokka_tulos_Directory) $(vanha_lähde_Files)
	touch $(완료표시)

한글검사:
	@sh työkalut/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(Luokka_tulos_Directory) Viro.JEstOS.testit.전체시험

isäntä: 검사
	$(자바실행기) -cp $(Luokka_tulos_Directory) Viro.JEstOS.isäntä.isäntä_käynnistys

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 vanha_lähde/의 objekti_ARVO 기반 관리 ydin_ARVO 전체를 AOT 변환하는 대상은 아니다.
kääntää_KUVA:
	$(MAKE) -C os iso

SIIVOA_kääntää:
	rm -rf TULOS
