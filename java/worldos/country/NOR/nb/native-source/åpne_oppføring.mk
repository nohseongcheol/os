자바컴파일러 ?= javac
자바실행기 ?= java
eldre_kilde_Filer := $(shell find eldre_kilde -type f -name '*.java' | sort)
time_produksjon_katalog := KR/time_VERDI
완료표시 := $(time_produksjon_katalog)/.완료

.PHONY: 모두 검사 vert 한글검사 RENSK_bygg bygg_BILDE

모두: 검사

$(완료표시): $(eldre_kilde_Filer)
	mkdir -p $(time_produksjon_katalog)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(time_produksjon_katalog) $(eldre_kilde_Filer)
	touch $(완료표시)

한글검사:
	@sh Verktøy/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(time_produksjon_katalog) Norge.JNorOS.시험.전체시험

vert: 검사
	$(자바실행기) -cp $(time_produksjon_katalog) Norge.JNorOS.vert.vert_oppstart

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 eldre_kilde/의 objekt_VERDI 기반 관리 kjerne_VERDI 전체를 AOT 변환하는 대상은 아니다.
bygg_BILDE:
	$(MAKE) -C os iso

RENSK_bygg:
	rm -rf KR
