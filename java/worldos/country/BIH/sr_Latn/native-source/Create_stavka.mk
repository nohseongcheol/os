자바컴파일러 ?= javac
자바실행기 ?= java
zastareo_izvor_Datoteke := $(shell find zastareo_izvor -type f -name '*.java' | sort)
클래스위치 := KR/Razred_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 host 한글검사 CLEAN_verzija verzija_IMAGE

모두: 검사

$(완료표시): $(zastareo_izvor_Datoteke)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(zastareo_izvor_Datoteke)
	touch $(완료표시)

한글검사:
	@sh Alatke/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Bosna_i_Hercegovina.JBihOS.시험.전체시험

host: 검사
	$(자바실행기) -cp $(클래스위치) Bosna_i_Hercegovina.JBihOS.host.호스트시작

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 zastareo_izvor/의 objekat_VALUE 기반 관리 jezgro_VALUE 전체를 AOT 변환하는 대상은 아니다.
verzija_IMAGE:
	$(MAKE) -C os iso

CLEAN_verzija:
	rm -rf KR
