자바컴파일러 ?= javac
자바실행기 ?= java
kirithi_chanzo_Faili := $(shell find kirithi_chanzo -type f -name '*.java' | sort)
클래스위치 := 결과/tabaka_thamani_55654bf1
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 mwenyeji 한글검사 Safi_jenga jenga_picha

모두: 검사

$(완료표시): $(kirithi_chanzo_Faili)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(kirithi_chanzo_Faili)
	touch $(완료표시)

한글검사:
	@sh Zana/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Mayotte.JMytOS.시험.전체시험

mwenyeji: 검사
	$(자바실행기) -cp $(클래스위치) Mayotte.JMytOS.mwenyeji.mwenyeji_uwashaji

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 kirithi_chanzo/의 kipengee_thamani 기반 관리 kiini_thamani_0611a8a8 전체를 AOT 변환하는 대상은 아니다.
jenga_picha:
	$(MAKE) -C os iso

Safi_jenga:
	rm -rf 결과
