자바컴파일러 ?= javac
자바실행기 ?= java
pärand_lähe_Failid := $(shell find pärand_lähe -type f -name '*.java' | sort)
tund_toodang_kaust := TULEMUS/tund_VALUE
완료표시 := $(tund_toodang_kaust)/.완료

.PHONY: 모두 검사 host 한글검사 CLEAN_järk järk_pilt

모두: 검사

$(완료표시): $(pärand_lähe_Failid)
	mkdir -p $(tund_toodang_kaust)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(tund_toodang_kaust) $(pärand_lähe_Failid)
	touch $(완료표시)

한글검사:
	@sh Tööriistad/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(tund_toodang_kaust) Soome.JFinOS.시험.전체시험

host: 검사
	$(자바실행기) -cp $(tund_toodang_kaust) Soome.JFinOS.host.host_käivitus

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 pärand_lähe/의 objekt_VALUE 기반 관리 tuum_VALUE 전체를 AOT 변환하는 대상은 아니다.
järk_pilt:
	$(MAKE) -C os iso

CLEAN_järk:
	rm -rf TULEMUS
