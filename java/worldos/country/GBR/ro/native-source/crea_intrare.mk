자바컴파일러 ?= javac
자바실행기 ?= java
moștenit_sursă_Fișiere := $(shell find moștenit_sursă -type f -name '*.java' | sort)
클래스위치 := KR/Clasă_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 gazdă 한글검사 CLEAN_generare generare_IMAGE

모두: 검사

$(완료표시): $(moștenit_sursă_Fișiere)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(moștenit_sursă_Fișiere)
	touch $(완료표시)

한글검사:
	@sh Instrumente/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Regatul_Unit.JGbrOS.시험.전체시험

gazdă: 검사
	$(자바실행기) -cp $(클래스위치) Regatul_Unit.JGbrOS.gazdă.gazdă_boot

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 moștenit_sursă/의 obiect_VALUE 기반 관리 nucleu_VALUE 전체를 AOT 변환하는 대상은 아니다.
generare_IMAGE:
	$(MAKE) -C os iso

CLEAN_generare:
	rm -rf KR
