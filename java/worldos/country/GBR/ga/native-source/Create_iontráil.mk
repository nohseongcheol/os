자바컴파일러 ?= javac
자바실행기 ?= java
oidhreacht_foinse_Comhaid := $(shell find oidhreacht_foinse -type f -name '*.java' | sort)
클래스위치 := tomhas/aicme_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 óstach 한글검사 CLEAN_tóg tóg_IMAGE

모두: 검사

$(완료표시): $(oidhreacht_foinse_Comhaid)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(oidhreacht_foinse_Comhaid)
	touch $(완료표시)

한글검사:
	@sh Uirlisí/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) an_Ríocht_Aontaithe.JGbrOS.시험.전체시험

óstach: 검사
	$(자바실행기) -cp $(클래스위치) an_Ríocht_Aontaithe.JGbrOS.óstach.óstach_tosú

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 oidhreacht_foinse/의 oibiacht_VALUE 기반 관리 eithne_VALUE 전체를 AOT 변환하는 대상은 아니다.
tóg_IMAGE:
	$(MAKE) -C os iso

CLEAN_tóg:
	rm -rf tomhas
