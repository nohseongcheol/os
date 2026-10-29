CompiladorJava ?= javac
lanzadorJava ?= java
archivosFuenteSistemaAntiguo := $(shell find FuentesFundamentales -type f -name '*.java' | sort)
directorioSalidaClase := resultado/valorClase
marcadorFinalización := $(directorioSalidaClase)/.esTerminado

.PHONY: construirTodos Comprobaciones Anfitrión comprobarHangul construirLimpiar construirImagen

construirTodos: Comprobaciones

$(marcadorFinalización): $(archivosFuenteSistemaAntiguo)
	mkdir -p $(directorioSalidaClase)
	$(CompiladorJava) -encoding UTF-8 -Xlint:all -Werror -d $(directorioSalidaClase) $(archivosFuenteSistemaAntiguo)
	touch $(marcadorFinalización)

comprobarHangul:
	@sh Herramientas/ComprobaciónIdentificadores.sh

Comprobaciones: comprobarHangul $(marcadorFinalización)
	$(lanzadorJava) -ea -cp $(directorioSalidaClase) Andorra.JAndOS.Pruebas.pruebaTodos

Anfitrión: Comprobaciones
	$(lanzadorJava) -cp $(directorioSalidaClase) Andorra.JAndOS.Anfitrión.inicioSistemaAnfitrión

# 별도 os/의 제한형 Java 네이티브 커널을 빌드한다.
# 기존 FuentesFundamentales/의 valorObjeto fundamento 관리 valorNúcleo 전체를 AOT 변환하는 대상은 아니다.
construirImagen:
	$(MAKE) -C os iso

construirLimpiar:
	rm -rf resultado
