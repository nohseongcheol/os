자바컴파일러 ?= javac
자바실행기 ?= java
okumisiwe_umthombo_Amafayela := $(shell find okumisiwe_umthombo -type f -name '*.java' | sort)
클래스위치 := 결과/uhlobo_inani
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 singatha 한글검사 정리 akha_isithombe

모두: 검사

$(완료표시): $(okumisiwe_umthombo_Amafayela)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(okumisiwe_umthombo_Amafayela)
	touch $(완료표시)

한글검사:
	@sh Amathuluzi/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) iMalawi.JMwiOS.시험.전체시험

singatha: 검사
	$(자바실행기) -cp $(클래스위치) iMalawi.JMwiOS.singatha.singatha_ukuvula

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 okumisiwe_umthombo/의 into_inani 기반 관리 ikhenela_inani 전체를 AOT 변환하는 대상은 아니다.
akha_isithombe:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
