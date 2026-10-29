자바컴파일러 ?= javac
자바실행기 ?= java
tawhito_pūtake_Ngā_Kōnae := $(shell find tawhito_pūtake -type f -name '*.java' | sort)
클래스위치 := mēhua/tauaha_uara
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 taurima 한글검사 CLEAN_hanga hanga_IMAGE

모두: 검사

$(완료표시): $(tawhito_pūtake_Ngā_Kōnae)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(tawhito_pūtake_Ngā_Kōnae)
	touch $(완료표시)

한글검사:
	@sh Ngā_Utauta/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Aotearoa.JNzlOS.시험.전체시험

taurima: 검사
	$(자바실행기) -cp $(클래스위치) Aotearoa.JNzlOS.taurima.taurima_whakaara

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 tawhito_pūtake/의 ahanoa_uara 기반 관리 kākano_uara_0611a8a8 전체를 AOT 변환하는 대상은 아니다.
hanga_IMAGE:
	$(MAKE) -C os iso

CLEAN_hanga:
	rm -rf mēhua
