자바컴파일러 ?= javac
자바실행기 ?= java
eyayikhe_yenzeka_umthombo_Iifayile := $(shell find eyayikhe_yenzeka_umthombo -type f -name '*.java' | sort)
클래스위치 := 결과/iklasi_ixabiso
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 umsingathi 한글검사 정리 yakha_umfanekiso

모두: 검사

$(완료표시): $(eyayikhe_yenzeka_umthombo_Iifayile)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(eyayikhe_yenzeka_umthombo_Iifayile)
	touch $(완료표시)

한글검사:
	@sh Izixhobo/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) EMzantsi_Afrika.JZafOS.시험.전체시험

umsingathi: 검사
	$(자바실행기) -cp $(클래스위치) EMzantsi_Afrika.JZafOS.umsingathi.umsingathi_ukuvula

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 eyayikhe_yenzeka_umthombo/의 into_ixabiso 기반 관리 ikheneli_ixabiso 전체를 AOT 변환하는 대상은 아니다.
yakha_umfanekiso:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
