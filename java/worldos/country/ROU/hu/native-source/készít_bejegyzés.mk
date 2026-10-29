자바컴파일러 ?= javac
자바실행기 ?= java
örökség_forrás_Files := $(shell find örökség_forrás -type f -name '*.java' | sort)
tanóra_kimenet_címtár := KR/tanóra_ÉRTÉK
완료표시 := $(tanóra_kimenet_címtár)/.완료

.PHONY: 모두 검사 gazda 한글검사 TISZTÍT_épít épít_KÉP

모두: 검사

$(완료표시): $(örökség_forrás_Files)
	mkdir -p $(tanóra_kimenet_címtár)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(tanóra_kimenet_címtár) $(örökség_forrás_Files)
	touch $(완료표시)

한글검사:
	@sh Eszközök/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(tanóra_kimenet_címtár) Románia.JRouOS.시험.전체시험

gazda: 검사
	$(자바실행기) -cp $(tanóra_kimenet_címtár) Románia.JRouOS.gazda.gazda_rendszerindítás

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 örökség_forrás/의 objektum_ÉRTÉK 기반 관리 kernel_ÉRTÉK 전체를 AOT 변환하는 대상은 아니다.
épít_KÉP:
	$(MAKE) -C os iso

TISZTÍT_épít:
	rm -rf KR
