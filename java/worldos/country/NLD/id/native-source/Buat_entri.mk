자바컴파일러 ?= javac
자바실행기 ?= java
lama_sumber_File := $(shell find lama_sumber -type f -name '*.java' | sort)
클래스위치 := hasil/Kelas_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 host 한글검사 CLEAN_build build_foto

모두: 검사

$(완료표시): $(lama_sumber_File)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(lama_sumber_File)
	touch $(완료표시)

한글검사:
	@sh alat/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Belanda.JNldOS.pengujian.전체시험

host: 검사
	$(자바실행기) -cp $(클래스위치) Belanda.JNldOS.host.host_mulai

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 lama_sumber/의 objek_VALUE 기반 관리 kernel_VALUE 전체를 AOT 변환하는 대상은 아니다.
build_foto:
	$(MAKE) -C os iso

CLEAN_build:
	rm -rf hasil
