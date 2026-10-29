자바컴파일러 ?= javac
자바실행기 ?= java
eldre_kjelde_Filer := $(shell find eldre_kjelde -type f -name '*.java' | sort)
클래스위치 := forretningsmål/time_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 vert 한글검사 CLEAN_bygg bygg_IMAGE

모두: 검사

$(완료표시): $(eldre_kjelde_Filer)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(eldre_kjelde_Filer)
	touch $(완료표시)

한글검사:
	@sh Verktøy/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Noreg.JNorOS.시험.전체시험

vert: 검사
	$(자바실행기) -cp $(클래스위치) Noreg.JNorOS.vert.vert_oppstart

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 eldre_kjelde/의 objekt_VALUE 기반 관리 kjerne_VALUE 전체를 AOT 변환하는 대상은 아니다.
bygg_IMAGE:
	$(MAKE) -C os iso

CLEAN_bygg:
	rm -rf forretningsmål
