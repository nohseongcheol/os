자바컴파일러 ?= javac
자바실행기 ?= java
oighreachd_tùs_faidhlichean := $(shell find oighreachd_tùs -type f -name '*.java' | sort)
클래스위치 := tomhas/clas_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 òstair 한글검사 CLEAN_tog tog_IMAGE

모두: 검사

$(완료표시): $(oighreachd_tùs_faidhlichean)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(oighreachd_tùs_faidhlichean)
	touch $(완료표시)

한글검사:
	@sh innealan/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) An_Rìoghachd_Aonaichte.JGbrOS.시험.전체시험

òstair: 검사
	$(자바실행기) -cp $(클래스위치) An_Rìoghachd_Aonaichte.JGbrOS.òstair.òstair_tòiseachadh

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 oighreachd_tùs/의 nì_VALUE 기반 관리 eitean_VALUE 전체를 AOT 변환하는 대상은 아니다.
tog_IMAGE:
	$(MAKE) -C os iso

CLEAN_tog:
	rm -rf tomhas
