자바컴파일러 ?= javac
자바실행기 ?= java
tàtijọ́_orísun_Àwọn_fáìlì := $(shell find tàtijọ́_orísun -type f -name '*.java' | sort)
클래스위치 := 결과/ọ̀wọ́_iye
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 olùpèsè 한글검사 정리 àtòpọ̀_àwòrán

모두: 검사

$(완료표시): $(tàtijọ́_orísun_Àwọn_fáìlì)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(tàtijọ́_orísun_Àwọn_fáìlì)
	touch $(완료표시)

한글검사:
	@sh Àwọn_irinṣẹ́/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Bẹ̀nẹ̀.JBenOS.시험.전체시험

olùpèsè: 검사
	$(자바실행기) -cp $(클래스위치) Bẹ̀nẹ̀.JBenOS.olùpèsè.olùpèsè_ìbẹ̀rẹ̀

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 tàtijọ́_orísun/의 nǹkan_iye 기반 관리 kánẹ́ẹ̀lì_iye 전체를 AOT 변환하는 대상은 아니다.
àtòpọ̀_àwòrán:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
