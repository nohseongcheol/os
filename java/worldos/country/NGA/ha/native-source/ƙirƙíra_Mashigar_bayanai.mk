자바컴파일러 ?= javac
자바실행기 ?= java
Tsohon_Bayani_tushe_Fayiloli := $(shell find Tsohon_Bayani_tushe -type f -name '*.java' | sort)
클래스위치 := 결과/Aji_Daraja
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 sauka 한글검사 정리 Gina_Hoto

모두: 검사

$(완료표시): $(Tsohon_Bayani_tushe_Fayiloli)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(Tsohon_Bayani_tushe_Fayiloli)
	touch $(완료표시)

한글검사:
	@sh Kaya/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) Nijeriya.JNgaOS.시험.전체시험

sauka: 검사
	$(자바실행기) -cp $(클래스위치) Nijeriya.JNgaOS.sauka.sauka_Matakan_kunna_kwamfuta

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 Tsohon_Bayani_tushe/의 abu_Daraja 기반 관리 Kwara_Daraja 전체를 AOT 변환하는 대상은 아니다.
Gina_Hoto:
	$(MAKE) -C os iso

정리:
	rm -rf 결과
