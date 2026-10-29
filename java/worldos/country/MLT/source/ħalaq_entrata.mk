자바컴파일러 ?= javac
자바실행기 ?= java
legacy_sors_Fajls := $(shell find legacy_sors -type f -name '*.java' | sort)
클래스위치 := miżura/klassi_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 host 한글검사 CLEAN_bena bena_IMAGE

모두: 검사

$(완료표시): $(legacy_sors_Fajls)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(legacy_sors_Fajls)
	touch $(완료표시)

한글검사:
	@sh Għodod/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Malta.JMltOS.시험.전체시험

host: 검사
	$(자바실행기) -cp $(클래스위치) Malta.JMltOS.host.host_ftuħ

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 legacy_sors/의 oġġett_VALUE 기반 관리 kernel_VALUE 전체를 AOT 변환하는 대상은 아니다.
bena_IMAGE:
	$(MAKE) -C os iso

CLEAN_bena:
	rm -rf miżura
