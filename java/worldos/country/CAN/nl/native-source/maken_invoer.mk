자바컴파일러 ?= javac
자바실행기 ?= java
verouderd_bron_Files := $(shell find verouderd_bron -type f -name '*.java' | sort)
les_uitvoer_map := resultaat/les_WAARDE
완료표시 := $(les_uitvoer_map)/.완료

.PHONY: 모두 검사 host 한글검사 Verscherpt_build build_kopie

모두: 검사

$(완료표시): $(verouderd_bron_Files)
	mkdir -p $(les_uitvoer_map)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(les_uitvoer_map) $(verouderd_bron_Files)
	touch $(완료표시)

한글검사:
	@sh hulpmiddelen/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(les_uitvoer_map) Canada.JCanOS.tests.전체시험

host: 검사
	$(자바실행기) -cp $(les_uitvoer_map) Canada.JCanOS.host.host_bootstrap

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 verouderd_bron/의 object_WAARDE 기반 관리 kernel_WAARDE 전체를 AOT 변환하는 대상은 아니다.
build_kopie:
	$(MAKE) -C os iso

Verscherpt_build:
	rm -rf resultaat
