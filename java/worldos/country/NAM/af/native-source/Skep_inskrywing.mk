자바컴파일러 ?= javac
자바실행기 ?= java
reedsbestaande_bron_Lêers := $(shell find reedsbestaande_bron -type f -name '*.java' | sort)
클래스위치 := maatreël/Klas_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 hou 한글검사 CLEAN_bou bou_foto

모두: 검사

$(완료표시): $(reedsbestaande_bron_Lêers)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(reedsbestaande_bron_Lêers)
	touch $(완료표시)

한글검사:
	@sh Nutsmiddels/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Namibië.JNamOS.시험.전체시험

hou: 검사
	$(자바실행기) -cp $(클래스위치) Namibië.JNamOS.hou.hou_selflaai

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 reedsbestaande_bron/의 objek_VALUE 기반 관리 kern_VALUE 전체를 AOT 변환하는 대상은 아니다.
bou_foto:
	$(MAKE) -C os iso

CLEAN_bou:
	rm -rf maatreël
