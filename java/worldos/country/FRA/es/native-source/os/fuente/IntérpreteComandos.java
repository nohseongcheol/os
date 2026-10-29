// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Pequeño intérprete de órdenes serie/PS2 que no escribe en disco. */
public final class IntérpreteComandos {
    static int[] valorEntrada = new int[128];
    static int longitud = 0;
    static boolean líneaElementoPrevioHaciaRetornar = false;
    static boolean desbordamientoLínea = false;

    static boolean comando(String nombre) {
        if (longitud < nombre.length()) return false;
        for (int número = 0; número < nombre.length(); número++)
            if (valorEntrada[número] != nombre.charAt(número)) return false;
        return longitud == nombre.length() || valorEntrada[nombre.length()] == ' ';
    }

    static void mostrarAyuda() {
        TerminalTexto.escribir("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        TerminalTexto.escribir("apps | run NAME [ARGS] | net\n");
        TerminalTexto.escribir("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        TerminalTexto.escribir("sync (연결된 JKSTORE1 valorAlmacenar 장치에 Archivo 보존)\n");
    }

    static void entradaElementoValorProceso() {
        if (longitud == 0) return;
        if (comando("help")) mostrarAyuda();
        else if (comando("sync")) {
            int resultado = PersistenciaArchivos.sincronizar();
            TerminalTexto.escribir("Sync: "); TerminalTexto.escribirNúmero(resultado); TerminalTexto.Caracteres(10);
        }
        else if (comando("ls")) SistemaArchivosMemoria.listaEntradaElemento();
        else if (comando("edit")) SistemaArchivosMemoria.comando(valorEntrada, 4, longitud, 0);
        else if (comando("cat")) SistemaArchivosMemoria.comando(valorEntrada, 3, longitud, 1);
        else if (comando("rm")) SistemaArchivosMemoria.comando(valorEntrada, 2, longitud, 2);
        else if (comando("java") || comando("javac")) {
            int resultado = GestiónEjecución.ejecutarComando(valorEntrada, 0, longitud);
            TerminalTexto.escribir("Exit: "); TerminalTexto.escribirNúmero(resultado); TerminalTexto.Caracteres(10);
        }
        else if (comando("apps")) GestiónEjecución.listaEntradaElemento();
        else if (comando("net")) PilaRed.valorEstadoValor();
        else if (comando("run")) {
            int resultado = GestiónEjecución.ejecutarComando(valorEntrada, 3, longitud);
            TerminalTexto.escribir("Exit: "); TerminalTexto.escribirNúmero(resultado); TerminalTexto.escribir("\n");
        } else if (comando("info")) {
            TerminalTexto.escribir("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (comando("mem")) {
            TerminalTexto.escribir("ladoSuperior Memoria regiónDirección(KiB): "); TerminalTexto.escribirNúmero(EspacioMemoria.tamañoMemoriaSuperior());
            TerminalTexto.escribir("\n배열 동적 Memoria regiónDirección(valorByte): "); TerminalTexto.escribirNúmero(Dispositivo.usoArreglo());
            TerminalTexto.escribir(" / 262144\n작업 regiónDirección valorSección: "); TerminalTexto.escribirNúmero(EspacioMemoria.númeroElementosEntradaElementoUsado());
            TerminalTexto.escribir(" / 8 (각 4096바이트)\n");
        } else if (comando("alloc")) {
            int número = EspacioMemoria.asignarMemoriaAlmacenamiento();
            TerminalTexto.escribir("valorSección número: "); TerminalTexto.escribirNúmero(número); TerminalTexto.escribir("\n");
        } else if (comando("free")) {
            if (longitud == 6 && valorEntrada[4] == ' ' && valorEntrada[5] >= '0' && valorEntrada[5] <= '7') {
                TerminalTexto.escribir(EspacioMemoria.resultadoRetornar(valorEntrada[5] - '0') ? "반환됨\n" : "할당되지 않은 valorSección\n");
            } else TerminalTexto.escribir("사용법: free 0..7\n");
        } else if (comando("echo")) {
            for (int número = 5; número < longitud; número++) TerminalTexto.Caracteres(valorEntrada[número]);
            TerminalTexto.Caracteres(10);
        } else if (comando("clear")) TerminalTexto.borrarEntradaElemento();
        else if (comando("test")) Núcleo.Pruebas();
        else if (comando("halt")) {
            TerminalTexto.escribir("HALTED\n");
            Dispositivo.ejecuciónDetenerMáquina();
        } else TerminalTexto.escribir("알 númeroValor 없는 명령입니다. help를 입력하세요.\n");
    }

    static void aceptarEscribirY(int valor) {
        if (valor == 10 && líneaElementoPrevioHaciaRetornar) { líneaElementoPrevioHaciaRetornar = false; return; }
        líneaElementoPrevioHaciaRetornar = valor == 13;
        if (valor == 10 || valor == 13) {
            TerminalTexto.Caracteres(10);
            if (SistemaArchivosMemoria.esEdiciónEnCurso) SistemaArchivosMemoria.líneaEditado(valorEntrada, longitud, desbordamientoLínea);
            else entradaElementoValorProceso();
            longitud = 0;
            desbordamientoLínea = false;
            TerminalTexto.escribir(SistemaArchivosMemoria.esEdiciónEnCurso ? "...> " : "jkoros> ");
        } else if (valor == 8 || valor == 127) {
            if (longitud > 0) {
                longitud--;
                TerminalTexto.byteSerie(8); TerminalTexto.byteSerie(32); TerminalTexto.byteSerie(8);
                TerminalTexto.carácterPantalla(8);
            }
        } else if (valor >= 32 && valor < 127 && longitud < valorEntrada.length) {
            valorEntrada[longitud++] = valor;
            TerminalTexto.Caracteres(valor);
        } else if (valor >= 32 && valor < 127) desbordamientoLínea = true;
    }

    static void ponerEnMarcha() {
        mostrarAyuda();
        TerminalTexto.escribir("READY\njkoros> ");
        while (true) {
            int valor = TerminalTexto.leerSerie();
            if (valor < 0) valor = Teclado.leer();
            if (valor >= 0) aceptarEscribirY(valor);
            else { PilaRed.verificar(); Dispositivo.cederBrevemente(); }
        }
    }
}
