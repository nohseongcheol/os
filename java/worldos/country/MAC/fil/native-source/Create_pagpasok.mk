자바컴파일러 ?= javac
자바실행기 ?= java
pamana_pinagmulan_Mga_File := $(shell find pamana_pinagmulan -type f -name '*.java' | sort)
클래스위치 := sukat/kategorya_VALUE_55654bf1
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 host 한글검사 CLEAN_build build_IMAGE

모두: 검사

$(완료표시): $(pamana_pinagmulan_Mga_File)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(pamana_pinagmulan_Mga_File)
	touch $(완료표시)

한글검사:
	@sh Mga_Tool/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Macau_SAR_China.JMacOS.시험.전체시험

host: 검사
	$(자바실행기) -cp $(클래스위치) Macau_SAR_China.JMacOS.host.host_magbukas

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 pamana_pinagmulan/의 bagay_VALUE 기반 관리 kernel_VALUE 전체를 AOT 변환하는 대상은 아니다.
build_IMAGE:
	$(MAKE) -C os iso

CLEAN_build:
	rm -rf sukat
