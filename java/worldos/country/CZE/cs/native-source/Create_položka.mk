자바컴파일러 ?= javac
자바실행기 ?= java
starší_verze_zdroj_Files := $(shell find starší_verze_zdroj -type f -name '*.java' | sort)
Třída_výstup_Adresář := VÝSLEDEK/Třída_HODNOTA
완료표시 := $(Třída_výstup_Adresář)/.완료

.PHONY: 모두 검사 hostit 한글검사 Čisté_BLD BLD_image

모두: 검사

$(완료표시): $(starší_verze_zdroj_Files)
	mkdir -p $(Třída_výstup_Adresář)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(Třída_výstup_Adresář) $(starší_verze_zdroj_Files)
	touch $(완료표시)

한글검사:
	@sh nástroje/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(Třída_výstup_Adresář) Česko.JCzeOS.zkoušky.전체시험

hostit: 검사
	$(자바실행기) -cp $(Třída_výstup_Adresář) Česko.JCzeOS.hostit.hostit_spuštění

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 starší_verze_zdroj/의 objekt_HODNOTA 기반 관리 jádro_HODNOTA 전체를 AOT 변환하는 대상은 아니다.
BLD_image:
	$(MAKE) -C os iso

Čisté_BLD:
	rm -rf VÝSLEDEK
