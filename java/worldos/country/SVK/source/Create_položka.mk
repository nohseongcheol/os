자바컴파일러 ?= javac
자바실행기 ?= java
starší_zdroj_Súbory := $(shell find starší_zdroj -type f -name '*.java' | sort)
클래스위치 := KR/lekcia_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 hostiteľ 한글검사 CLEAN_zostava zostava_IMAGE

모두: 검사

$(완료표시): $(starší_zdroj_Súbory)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(starší_zdroj_Súbory)
	touch $(완료표시)

한글검사:
	@sh Nástroje/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Slovensko.JSvkOS.시험.전체시험

hostiteľ: 검사
	$(자바실행기) -cp $(클래스위치) Slovensko.JSvkOS.hostiteľ.hostiteľ_spustenie

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 starší_zdroj/의 objekt_VALUE 기반 관리 jadro_VALUE 전체를 AOT 변환하는 대상은 아니다.
zostava_IMAGE:
	$(MAKE) -C os iso

CLEAN_zostava:
	rm -rf KR
