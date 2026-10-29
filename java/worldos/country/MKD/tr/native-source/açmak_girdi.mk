자바컴파일러 ?= javac
자바실행기 ?= java
eski_kaynak_Dosyalar := $(shell find eski_kaynak -type f -name '*.java' | sort)
Sınıf_çıktı_dizin := sonuç/Sınıf_değer
완료표시 := $(Sınıf_çıktı_dizin)/.완료

.PHONY: 모두 검사 konak 한글검사 TEMİZ_BLD BLD_RESİM

모두: 검사

$(완료표시): $(eski_kaynak_Dosyalar)
	mkdir -p $(Sınıf_çıktı_dizin)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(Sınıf_çıktı_dizin) $(eski_kaynak_Dosyalar)
	touch $(완료표시)

한글검사:
	@sh araçlar/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(Sınıf_çıktı_dizin) Kuzey_Makedonya.JMkdOS.sınamalar.전체시험

konak: 검사
	$(자바실행기) -cp $(Sınıf_çıktı_dizin) Kuzey_Makedonya.JMkdOS.konak.konak_IPL

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 eski_kaynak/의 nesne_değer 기반 관리 çekirdek_değer 전체를 AOT 변환하는 대상은 아니다.
BLD_RESİM:
	$(MAKE) -C os iso

TEMİZ_BLD:
	rm -rf sonuç
