자바컴파일러 ?= javac
자바실행기 ?= java
senstelėjusi_įranga_šaltinis_Failai := $(shell find senstelėjusi_įranga_šaltinis -type f -name '*.java' | sort)
klasė_išeiga_Katalogas := REZULTATAS/klasė_VALUE
완료표시 := $(klasė_išeiga_Katalogas)/.완료

.PHONY: 모두 검사 organizuoti 한글검사 CLEAN_kompiliuoti kompiliuoti_IMAGE

모두: 검사

$(완료표시): $(senstelėjusi_įranga_šaltinis_Failai)
	mkdir -p $(klasė_išeiga_Katalogas)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(klasė_išeiga_Katalogas) $(senstelėjusi_įranga_šaltinis_Failai)
	touch $(완료표시)

한글검사:
	@sh Įrankiai/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(klasė_išeiga_Katalogas) Lietuva.JLtuOS.시험.전체시험

organizuoti: 검사
	$(자바실행기) -cp $(klasė_išeiga_Katalogas) Lietuva.JLtuOS.organizuoti.organizuoti_perkrovimas

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 senstelėjusi_įranga_šaltinis/의 objektas_VALUE 기반 관리 branduolys_VALUE 전체를 AOT 변환하는 대상은 아니다.
kompiliuoti_IMAGE:
	$(MAKE) -C os iso

CLEAN_kompiliuoti:
	rm -rf REZULTATAS
