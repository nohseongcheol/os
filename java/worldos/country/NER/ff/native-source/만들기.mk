자바컴파일러 ?= javac
자바실행기 ?= java
원천파일 := $(shell find donaa_sewnde -type f -name '*.java' | sort)
클래스위치 := 결과/fedde_njaru
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 njaatigi 한글검사 정리 tafde_natal

모두: 검사

$(완료표시): $(원천파일)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(원천파일)
	touch $(완료표시)

한글검사:
	@sh 도구/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Nijeer.JNerOS.시험.전체시험

njaatigi: 검사
	$(자바실행기) -cp $(클래스위치) Nijeer.JNerOS.njaatigi.njaatigi_kuɓɓagol

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 donaa_sewnde/의 huunde_njaru 기반 관리 aaluude_njaru 전체를 AOT 변환하는 대상은 아니다.
tafde_natal:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
