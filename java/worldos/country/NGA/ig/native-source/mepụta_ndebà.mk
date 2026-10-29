자바컴파일러 ?= javac
자바실행기 ?= java
ekpe_ebensìbịa_Ndi_ọbọakwụkwọ := $(shell find ekpe_ebensìbịa -type f -name '*.java' | sort)
클래스위치 := 결과/klaàsị_valuu
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 usu 한글검사 정리 wue_foto

모두: 검사

$(완료표시): $(ekpe_ebensìbịa_Ndi_ọbọakwụkwọ)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(ekpe_ebensìbịa_Ndi_ọbọakwụkwọ)
	touch $(완료표시)

한글검사:
	@sh Ngwaọrụ/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Naịjịrịa.JNgaOS.시험.전체시험

usu: 검사
	$(자바실행기) -cp $(클래스위치) Naịjịrịa.JNgaOS.usu.usu_mbido

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 ekpe_ebensìbịa/의 ihe_valuu 기반 관리 mkpụrụobī_kọmpùta_valuu 전체를 AOT 변환하는 대상은 아니다.
wue_foto:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
