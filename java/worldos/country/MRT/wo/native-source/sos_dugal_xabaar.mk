자바컴파일러 ?= javac
자바실행기 ?= java
ndono_Cosaan_Fisiye_yi := $(shell find ndono_Cosaan -type f -name '*.java' | sort)
클래스위치 := 결과/maas_xëyma
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 dalal 한글검사 정리 tabax_nataal

모두: 검사

$(완료표시): $(ndono_Cosaan_Fisiye_yi)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(ndono_Cosaan_Fisiye_yi)
	touch $(완료표시)

한글검사:
	@sh Jumtukaay_yi/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Mooritani.JMrtOS.시험.전체시험

dalal: 검사
	$(자바실행기) -cp $(클래스위치) Mooritani.JMrtOS.dalal.dalal_buuraat

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 ndono_Cosaan/의 yëf_xëyma 기반 관리 xoox_xëyma 전체를 AOT 변환하는 대상은 아니다.
tabax_nataal:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
