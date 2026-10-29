자바컴파일러 ?= javac
자바실행기 ?= java
mantots_avots_Faili := $(shell find mantots_avots -type f -name '*.java' | sort)
klase_ražojums_Direktorijs := mērs/klase_VALUE
완료표시 := $(klase_ražojums_Direktorijs)/.완료

.PHONY: 모두 검사 viesot 한글검사 CLEAN_būvējums būvējums_IMAGE

모두: 검사

$(완료표시): $(mantots_avots_Faili)
	mkdir -p $(klase_ražojums_Direktorijs)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(klase_ražojums_Direktorijs) $(mantots_avots_Faili)
	touch $(완료표시)

한글검사:
	@sh Rīki/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(klase_ražojums_Direktorijs) Latvija.JLvaOS.시험.전체시험

viesot: 검사
	$(자바실행기) -cp $(klase_ražojums_Direktorijs) Latvija.JLvaOS.viesot.viesot_palaišana

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 mantots_avots/의 objekts_VALUE 기반 관리 kodols_VALUE 전체를 AOT 변환하는 대상은 아니다.
būvējums_IMAGE:
	$(MAKE) -C os iso

CLEAN_būvējums:
	rm -rf mērs
