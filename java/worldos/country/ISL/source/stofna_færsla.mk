자바컴파일러 ?= javac
자바실행기 ?= java
eldra_uppruni_Skrár := $(shell find eldra_uppruni -type f -name '*.java' | sort)
klasi_úttak_skráasafn := NIÐURSTAÐA/klasi_VALUE
완료표시 := $(klasi_úttak_skráasafn)/.완료

.PHONY: 모두 검사 hýsa 한글검사 CLEAN_smíð smíð_mynd

모두: 검사

$(완료표시): $(eldra_uppruni_Skrár)
	mkdir -p $(klasi_úttak_skráasafn)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(klasi_úttak_skráasafn) $(eldra_uppruni_Skrár)
	touch $(완료표시)

한글검사:
	@sh Verkfæri/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(klasi_úttak_skráasafn) Ísland.JIslOS.시험.전체시험

hýsa: 검사
	$(자바실행기) -cp $(klasi_úttak_skráasafn) Ísland.JIslOS.hýsa.hýsa_ræsa

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 eldra_uppruni/의 hlutur_VALUE 기반 관리 kjarni_VALUE 전체를 AOT 변환하는 대상은 아니다.
smíð_mynd:
	$(MAKE) -C os iso

CLEAN_smíð:
	rm -rf NIÐURSTAÐA
