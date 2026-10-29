자바컴파일러 ?= javac
자바실행기 ?= java
trashëgim_burim_Skedarët := $(shell find trashëgim_burim -type f -name '*.java' | sort)
클래스위치 := llogaritje/klasë_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 pritës 한글검사 CLEAN_ndërtoj ndërtoj_IMAGE

모두: 검사

$(완료표시): $(trashëgim_burim_Skedarët)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(trashëgim_burim_Skedarët)
	touch $(완료표시)

한글검사:
	@sh Mjete/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Turqi.JTurOS.시험.전체시험

pritës: 검사
	$(자바실행기) -cp $(클래스위치) Turqi.JTurOS.pritës.pritës_nisje

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 trashëgim_burim/의 objekt_VALUE 기반 관리 bërthamë_VALUE 전체를 AOT 변환하는 대상은 아니다.
ndërtoj_IMAGE:
	$(MAKE) -C os iso

CLEAN_ndërtoj:
	rm -rf llogaritje
