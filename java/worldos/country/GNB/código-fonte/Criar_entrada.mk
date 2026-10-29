자바컴파일러 ?= javac
자바실행기 ?= java
herdado_fonte_Arquivos := $(shell find herdado_fonte -type f -name '*.java' | sort)
aula_saída_Diretório := resultado/aula_VALOR
완료표시 := $(aula_saída_Diretório)/.완료

.PHONY: 모두 검사 host 한글검사 TIRAR_BLD BLD_foto

모두: 검사

$(완료표시): $(herdado_fonte_Arquivos)
	mkdir -p $(aula_saída_Diretório)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(aula_saída_Diretório) $(herdado_fonte_Arquivos)
	touch $(완료표시)

한글검사:
	@sh ferramentas/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(aula_saída_Diretório) Guiné_Bissau.JGnbOS.testes.전체시험

host: 검사
	$(자바실행기) -cp $(aula_saída_Diretório) Guiné_Bissau.JGnbOS.host.host_inicialização

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 herdado_fonte/의 objeto_VALOR 기반 관리 kernel_VALOR 전체를 AOT 변환하는 대상은 아니다.
BLD_foto:
	$(MAKE) -C os iso

TIRAR_BLD:
	rm -rf resultado
