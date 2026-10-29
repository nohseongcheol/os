자바컴파일러 ?= javac
자바실행기 ?= java
nedarvet_kilde_Filer := $(shell find nedarvet_kilde -type f -name '*.java' | sort)
Hold_produktoutput_mappe := KR/Hold_VÆRDI
완료표시 := $(Hold_produktoutput_mappe)/.완료

.PHONY: 모두 검사 vært 한글검사 Ren_build build_Image

모두: 검사

$(완료표시): $(nedarvet_kilde_Filer)
	mkdir -p $(Hold_produktoutput_mappe)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(Hold_produktoutput_mappe) $(nedarvet_kilde_Filer)
	touch $(완료표시)

한글검사:
	@sh Værktøjer/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(Hold_produktoutput_mappe) Danmark.JDnkOS.시험.전체시험

vært: 검사
	$(자바실행기) -cp $(Hold_produktoutput_mappe) Danmark.JDnkOS.vært.vært_IPL

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 nedarvet_kilde/의 objekt_VÆRDI 기반 관리 kerne_VÆRDI 전체를 AOT 변환하는 대상은 아니다.
build_Image:
	$(MAKE) -C os iso

Ren_build:
	rm -rf KR
