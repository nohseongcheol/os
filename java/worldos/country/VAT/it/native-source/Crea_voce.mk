자바컴파일러 ?= javac
자바실행기 ?= java
legacy_fonte_File := $(shell find legacy_fonte -type f -name '*.java' | sort)
Corso_output_elenco := risultato/Corso_VALORE
완료표시 := $(Corso_output_elenco)/.완료

.PHONY: 모두 검사 host 한글검사 LIBERA_BLD BLD_foto

모두: 검사

$(완료표시): $(legacy_fonte_File)
	mkdir -p $(Corso_output_elenco)
	$(자바컴파일러) -encoding UTF-8 -Xlint:all -Werror -d $(Corso_output_elenco) $(legacy_fonte_File)
	touch $(완료표시)

한글검사:
	@sh strumenti/한글이름검사.sh

검사: 한글검사 $(완료표시)
	$(자바실행기) -ea -cp $(Corso_output_elenco) Città_del_Vaticano.JVatOS.prove.전체시험

host: 검사
	$(자바실행기) -cp $(Corso_output_elenco) Città_del_Vaticano.JVatOS.host.host_avvio

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 legacy_fonte/의 oggetto_VALORE 기반 관리 kernel_VALORE 전체를 AOT 변환하는 대상은 아니다.
BLD_foto:
	$(MAKE) -C os iso

LIBERA_BLD:
	rm -rf risultato
