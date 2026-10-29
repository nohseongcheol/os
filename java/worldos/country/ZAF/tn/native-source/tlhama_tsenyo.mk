자바컴파일러 ?= javac
자바실행기 ?= java
maloba_Motswedi_Difaele := $(shell find maloba_Motswedi -type f -name '*.java' | sort)
클래스위치 := 결과/mofuta_Boleng
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 pinagare 한글검사 정리 aga_Setshwantsho

모두: 검사

$(완료표시): $(maloba_Motswedi_Difaele)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(maloba_Motswedi_Difaele)
	touch $(완료표시)

한글검사:
	@sh Thuluse/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Aforika_Borwa.JZafOS.시험.전체시험

pinagare: 검사
	$(자바실행기) -cp $(클래스위치) Aforika_Borwa.JZafOS.pinagare.pinagare_tshimologosešwa

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 maloba_Motswedi/의 selwana_Boleng 기반 관리 Khenele_Boleng 전체를 AOT 변환하는 대상은 아니다.
aga_Setshwantsho:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
