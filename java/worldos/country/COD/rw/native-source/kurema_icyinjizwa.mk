자바컴파일러 ?= javac
자바실행기 ?= java
umurage_inkomoko_Dosiye := $(shell find umurage_inkomoko -type f -name '*.java' | sort)
클래스위치 := 결과/icyiciro_agaciro_55654bf1
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 gucumbikira 한글검사 정리 gusohora_ishusho

모두: 검사

$(완료표시): $(umurage_inkomoko_Dosiye)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(umurage_inkomoko_Dosiye)
	touch $(완료표시)

한글검사:
	@sh Ibikoresho/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) COD.JCodOS.시험.전체시험

gucumbikira: 검사
	$(자바실행기) -cp $(클래스위치) COD.JCodOS.gucumbikira.gucumbikira_iyatsa

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 umurage_inkomoko/의 ikintu_agaciro_2ed200e9 기반 관리 intima_agaciro 전체를 AOT 변환하는 대상은 아니다.
gusohora_ishusho:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
