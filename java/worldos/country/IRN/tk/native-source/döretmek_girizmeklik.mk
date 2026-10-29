자바컴파일러 ?= javac
자바실행기 ?= java
geçen_gor_Faýllar := $(shell find geçen_gor -type f -name '*.java' | sort)
클래스위치 := 결과/klas_baha
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 esasy 한글검사 Päkize_düz düz_surat

모두: 검사

$(완료표시): $(geçen_gor_Faýllar)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(geçen_gor_Faýllar)
	touch $(완료표시)

한글검사:
	@sh Gurallar/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Eýran.JIrnOS.시험.전체시험

esasy: 검사
	$(자바실행기) -cp $(클래스위치) Eýran.JIrnOS.esasy.esasy_başlangyç

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 geçen_gor/의 obýekt_baha 기반 관리 ýadro_baha 전체를 AOT 변환하는 대상은 아니다.
düz_surat:
	$(MAKE) -C os iso

Päkize_düz:
	rm -rf 결과
