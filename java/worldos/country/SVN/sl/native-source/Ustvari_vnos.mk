자바컴파일러 ?= javac
자바실행기 ?= java
starejši_vir_Datoteke := $(shell find starejši_vir -type f -name '*.java' | sort)
클래스위치 := REZULTAT/Razred_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 gostiti 한글검사 CLEAN_graditev graditev_IMAGE

모두: 검사

$(완료표시): $(starejši_vir_Datoteke)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(starejši_vir_Datoteke)
	touch $(완료표시)

한글검사:
	@sh Orodja/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Slovenija.JSvnOS.시험.전체시험

gostiti: 검사
	$(자바실행기) -cp $(클래스위치) Slovenija.JSvnOS.gostiti.gostiti_zagnati

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 starejši_vir/의 predmet_VALUE 기반 관리 jedro_VALUE 전체를 AOT 변환하는 대상은 아니다.
graditev_IMAGE:
	$(MAKE) -C os iso

CLEAN_graditev:
	rm -rf REZULTAT
