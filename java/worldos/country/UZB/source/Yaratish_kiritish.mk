자바컴파일러 ?= javac
자바실행기 ?= java
meros_manba_Fayllar := $(shell find meros_manba -type f -name '*.java' | sort)
클래스위치 := o_lchov/Sinf_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 tashkilotchi 한글검사 Toza_nashr nashr_rasm

모두: 검사

$(완료표시): $(meros_manba_Fayllar)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(meros_manba_Fayllar)
	touch $(완료표시)

한글검사:
	@sh Vositalar/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Oʻzbekiston.JUzbOS.시험.전체시험

tashkilotchi: 검사
	$(자바실행기) -cp $(클래스위치) Oʻzbekiston.JUzbOS.tashkilotchi.tashkilotchi_yuklash

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 meros_manba/의 obyekt_VALUE 기반 관리 o_zak_VALUE 전체를 AOT 변환하는 대상은 아니다.
nashr_rasm:
	$(MAKE) -C os iso

Toza_nashr:
	rm -rf o_lchov
