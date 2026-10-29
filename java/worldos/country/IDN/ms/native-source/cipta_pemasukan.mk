자바컴파일러 ?= javac
자바실행기 ?= java
legasi_sumber_Fail := $(shell find legasi_sumber -type f -name '*.java' | sort)
클래스위치 := ukuran/Kelas_VALUE
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 hos 한글검사 CLEAN_bina bina_imej

모두: 검사

$(완료표시): $(legasi_sumber_Fail)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(legasi_sumber_Fail)
	touch $(완료표시)

한글검사:
	@sh alat/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Indonesia.JIdnOS.ujian.전체시험

hos: 검사
	$(자바실행기) -cp $(클래스위치) Indonesia.JIdnOS.hos.hos_butstrap

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 legasi_sumber/의 objek_VALUE 기반 관리 kernel_VALUE 전체를 AOT 변환하는 대상은 아니다.
bina_imej:
	$(MAKE) -C os iso

CLEAN_bina:
	rm -rf ukuran
