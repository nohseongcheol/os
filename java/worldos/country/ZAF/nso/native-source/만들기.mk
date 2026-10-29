자바컴파일러 ?= javac
자바실행기 ?= java
ya_kgale_mohlodi_Difaele := $(shell find ya_kgale_mohlodi -type f -name '*.java' | sort)
클래스위치 := 결과/legoro_boleng_55654bf1
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 go_nea_ditirelo 한글검사 정리 aga_seswantšho

모두: 검사

$(완료표시): $(ya_kgale_mohlodi_Difaele)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(ya_kgale_mohlodi_Difaele)
	touch $(완료표시)

한글검사:
	@sh Ditholosi/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Afrika_Borwa.JZafOS.시험.전체시험

go_nea_ditirelo: 검사
	$(자바실행기) -cp $(클래스위치) Afrika_Borwa.JZafOS.go_nea_ditirelo.go_nea_ditirelo_bula

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 ya_kgale_mohlodi/의 selo_boleng 기반 관리 khenele_boleng 전체를 AOT 변환하는 대상은 아니다.
aga_seswantšho:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
