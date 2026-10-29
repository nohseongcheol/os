자바컴파일러 ?= javac
자바실행기 ?= java
herdado_fonte_Ficheiros := $(shell find herdado_fonte -type f -name '*.java' | sort)
클래스위치 := RESULTANTE/Clase_VALOR
완료표시 := $(클래스위치)/.완료

.PHONY: 모두 검사 hospedar 한글검사 Limpo_compilar compilar_IMAXE

모두: 검사

$(완료표시): $(herdado_fonte_Ficheiros)
	mkdir -p $(클래스위치)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(클래스위치) $(herdado_fonte_Ficheiros)
	touch $(완료표시)

한글검사:
	@sh Ferramentas/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(클래스위치) España.JEspOS.시험.전체시험

hospedar: 검사
	$(자바실행기) -cp $(클래스위치) España.JEspOS.hospedar.hospedar_inicio

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 herdado_fonte/의 obxecto_VALOR 기반 관리 kernel_VALOR 전체를 AOT 변환하는 대상은 아니다.
compilar_IMAXE:
	$(MAKE) -C os iso

Limpo_compilar:
	rm -rf RESULTANTE
