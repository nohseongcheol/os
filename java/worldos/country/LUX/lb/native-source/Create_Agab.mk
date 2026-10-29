자바컴파일러 ?= javac
자바실행기 ?= java
al_Quell_Fichieren := $(shell find al_Quell -type f -name '*.java' | sort)
클래스위치 := Mooss/Klass_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 Host 한글검사 CLEAN_Build Build_Bild

모두: 검사

$(완료표시): $(al_Quell_Fichieren)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(al_Quell_Fichieren)
	touch $(완료표시)

한글검사:
	@sh Tools/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Lëtzebuerg.JLuxOS.시험.전체시험

Host: 검사
	$(자바실행기) -cp $(클래스위치) Lëtzebuerg.JLuxOS.Host.Host_Start

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 al_Quell/의 Objet_VALUE 기반 관리 Kernel_VALUE 전체를 AOT 변환하는 대상은 아니다.
Build_Bild:
	$(MAKE) -C os iso

CLEAN_Build:
	rm -rf Mooss
