// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Ocho archivos conservados durante la sesión. Si falla la edición o compilación, se preservan los archivos existentes. */
public final class SistemaArchivosMemoria {
    static final int tamañoMáximo = 16384;
    static int[] listaNombres = new int[8 * 64];
    static int[] listaTamaño = new int[8];
    static int[] abrirNúmeroElementos = new int[8], concesionesPermiso = new int[8];
    static int[] nombre = new int[64];
    static int[] valorEditar = new int[tamañoMáximo];
    static boolean esEdiciónEnCurso = false;
    static boolean valorDesbordamiento = false;
    static int tamañoEditar = 0;

    static boolean comprobarNombre(int[] valorCarácter, int longitud) {
        if (longitud < 1 || longitud > 63) return false;
        for (int númeroValor = 0; númeroValor < longitud; númeroValor++) {
            int valor = valorCarácter[númeroValor];
            if (!(valor >= 'a' && valor <= 'z') && !(valor >= 'A' && valor <= 'Z')
                && !(valor >= '0' && valor <= '9') && valor != '_' && valor != '-' && valor != '.') return false;
        }
        return valorCarácter[0] != '.';
    }

    static int encontrarEntradaElemento(int[] valorCarácter, int longitud) {
        if (!comprobarNombre(valorCarácter, longitud)) return -22;
        for (int númeroValor = 0; númeroValor < 8; númeroValor++) {
            boolean textoIgual = listaNombres[númeroValor * 64 + longitud] == 0;
            for (int entradaElementoRanura = 0; entradaElementoRanura < longitud; entradaElementoRanura++) if (listaNombres[númeroValor * 64 + entradaElementoRanura] != valorCarácter[entradaElementoRanura]) textoIgual = false;
            if (textoIgual) return númeroValor;
        }
        return -2;
    }

    static int valorAlmacenar(int[] valorCarácter, int longitud, int[] Datos, int tamaño) {
        if (!comprobarNombre(valorCarácter, longitud) || tamaño < 0 || tamaño > Datos.length) return -22;
        if (tamaño > tamañoMáximo) return -90;
        int número = encontrarEntradaElemento(valorCarácter, longitud);
        if (número == -2) {
            for (int númeroValor = 0; númeroValor < 8 && número < 0; númeroValor++) if (listaNombres[númeroValor * 64] == 0 && abrirNúmeroElementos[númeroValor] == 0) número = númeroValor;
            if (número >= 0) concesionesPermiso[número] = 438;
        }
        if (número < 0) return -28;
        int dirección = Dispositivo.memoriaArchivo() + número * tamañoMáximo;
        for (int númeroValor = 0; númeroValor < tamaño; númeroValor++) Dispositivo.escribirMemoria(dirección + númeroValor, Datos[númeroValor]);
        for (int númeroValor = 0; númeroValor < 64; númeroValor++) listaNombres[número * 64 + númeroValor] = númeroValor < longitud ? valorCarácter[númeroValor] : 0;
        listaTamaño[número] = tamaño;
        return tamaño;
    }

    static void listaEntradaElemento() {
        for (int númeroValor = 0; númeroValor < 8; númeroValor++) if (listaNombres[númeroValor * 64] != 0) {
            for (int entradaElementoRanura = 0; entradaElementoRanura < 64 && listaNombres[númeroValor * 64 + entradaElementoRanura] != 0; entradaElementoRanura++) TerminalTexto.Caracteres(listaNombres[númeroValor * 64 + entradaElementoRanura]);
            TerminalTexto.escribir("  "); TerminalTexto.escribirNúmero(listaTamaño[númeroValor]); TerminalTexto.escribir("valorByte\n");
        }
        TerminalTexto.escribir(ConexiónAlmacenamiento.esDisponible ? "Archivo 8칸, 파일당 16384바이트; sync로 valorAlmacenar 장치에 보존\n"
            : "valorTemporal Archivo 8칸, 파일당 16384바이트; valorReintentar 시작하면 사라짐\n");
    }

    static void comando(int[] valorEntrada, int ponerEnMarcha, int longitud, int acción) {
        while (ponerEnMarcha < longitud && valorEntrada[ponerEnMarcha] == ' ') ponerEnMarcha++;
        int terminación = longitud;
        while (terminación > ponerEnMarcha && valorEntrada[terminación - 1] == ' ') terminación--;
        int númeroValor = terminación - ponerEnMarcha;
        if (númeroValor < 1 || númeroValor > 63) { TerminalTexto.escribir("올바르지 않은 Archivo nombre\n"); return; }
        for (int entradaElementoRanura = 0; entradaElementoRanura < 64; entradaElementoRanura++) nombre[entradaElementoRanura] = entradaElementoRanura < númeroValor ? valorEntrada[ponerEnMarcha + entradaElementoRanura] : 0;
        int número = encontrarEntradaElemento(nombre, númeroValor);
        if (número == -22) { TerminalTexto.escribir("올바르지 않은 Archivo nombre\n"); return; }
        if (acción == 0) {
            esEdiciónEnCurso = true; tamañoEditar = 0; valorDesbordamiento = false;
            TerminalTexto.escribir("원문을 입력하세요. .save는 보존, .cancel은 취소합니다.\n");
        } else if (número < 0) TerminalTexto.escribir("파일을 찾을 númeroValor 없습니다\n");
        else if (acción == 1) {
            int dirección = Dispositivo.memoriaArchivo() + número * tamañoMáximo;
            for (int entradaElementoRanura = 0; entradaElementoRanura < listaTamaño[número]; entradaElementoRanura++) TerminalTexto.Caracteres(Dispositivo.leerMemoria(dirección + entradaElementoRanura));
            TerminalTexto.Caracteres(10);
        } else { listaNombres[número * 64] = 0; listaTamaño[número] = 0; TerminalTexto.escribir("파일을 지웠습니다\n"); }
    }

    static boolean esExacto(int[] valorEntrada, int longitud, String valorExpresiónFrase) {
        if (longitud != valorExpresiónFrase.length()) return false;
        for (int entradaElementoRanura = 0; entradaElementoRanura < longitud; entradaElementoRanura++) if (valorEntrada[entradaElementoRanura] != valorExpresiónFrase.charAt(entradaElementoRanura)) return false;
        return true;
    }

    static void líneaEditado(int[] valorEntrada, int longitud, boolean desbordamientoLínea) {
        if (esExacto(valorEntrada, longitud, ".cancel")) {
            esEdiciónEnCurso = false; TerminalTexto.escribir("취소했습니다. 원래 파일은 그대로입니다\n");
        } else if (esExacto(valorEntrada, longitud, ".save")) {
            esEdiciónEnCurso = false;
            if (valorDesbordamiento) { TerminalTexto.escribir("입력이 너무 깁니다. 원래 파일은 그대로입니다\n"); return; }
            int númeroValor = 0;
            while (númeroValor < 64 && nombre[númeroValor] != 0) númeroValor++;
            int resultado = valorAlmacenar(nombre, númeroValor, valorEditar, tamañoEditar);
            TerminalTexto.escribir(resultado >= 0 ? "보존한 valorByte númeroValor: " : "보존 valorFallo: ");
            TerminalTexto.escribirNúmero(resultado); TerminalTexto.Caracteres(10);
        } else if (desbordamientoLínea || longitud + 1 > tamañoMáximo - tamañoEditar) valorDesbordamiento = true;
        else {
            for (int númeroValor = 0; númeroValor < longitud; númeroValor++) valorEditar[tamañoEditar++] = valorEntrada[númeroValor];
            valorEditar[tamañoEditar++] = 10;
        }
    }

    static void Ejemplos(String Archivo, String valorContenidoValor) {
        for (int númeroValor = 0; númeroValor < 64; númeroValor++) nombre[númeroValor] = númeroValor < Archivo.length() ? Archivo.charAt(númeroValor) : 0;
        for (int númeroValor = 0; númeroValor < valorContenidoValor.length(); númeroValor++) valorEditar[númeroValor] = valorContenidoValor.charAt(númeroValor);
        valorAlmacenar(nombre, Archivo.length(), valorEditar, valorContenidoValor.length());
    }

    static void preparar() {
        Ejemplos("Hello.java", "public class Hello {\n public static void main(String[] args) {\n  System.out.println(\"Hello from jkoros JVM!\");\n  int sum = 0;\n  for (int i = 1; i <= 10; i++) { sum = sum + i; }\n  System.out.println(sum);\n }\n}\n");
        int valorGrupo = Dispositivo.paqueteArchivoJava(), tamaño = Dispositivo.tamañoPaqueteArchivoJava();
        if (tamaño < 8 || GestiónEjecución.númeroValor(valorGrupo) != 0x464a4b4a) { TerminalTexto.escribir("올바르지 않은 Java Archivo valorGrupo\n"); return; }
        int númeroElementosElementoLista = GestiónEjecución.númeroValor(valorGrupo + 4);
        if (númeroElementosElementoLista < 0 || númeroElementosElementoLista > 8 || númeroElementosElementoLista > (tamaño - 8) / 72) { TerminalTexto.escribir("올바르지 않은 Java Archivo listaEntradaElemento\n"); return; }
        for (int númeroValor = 0; númeroValor < númeroElementosElementoLista; númeroValor++) {
            int valorEntradaElemento = valorGrupo + 8 + númeroValor * 72, longitud = 0;
            for (int entradaElementoRanura = 0; entradaElementoRanura < 64; entradaElementoRanura++) nombre[entradaElementoRanura] = Dispositivo.leerMemoria(valorEntradaElemento + entradaElementoRanura);
            while (longitud < 64 && nombre[longitud] != 0) longitud++;
            int posición = GestiónEjecución.númeroValor(valorEntradaElemento + 64), tamañoArchivo = GestiónEjecución.númeroValor(valorEntradaElemento + 68);
            if (!comprobarNombre(nombre, longitud) || tamañoArchivo < 0 || tamañoArchivo > tamañoMáximo || posición < 8 + númeroElementosElementoLista * 72 || posición > tamaño - tamañoArchivo) {
                TerminalTexto.escribir("올바르지 않은 Java Archivo valorEntradaElemento\n"); return;
            }
            for (int entradaElementoRanura = 0; entradaElementoRanura < tamañoArchivo; entradaElementoRanura++) valorEditar[entradaElementoRanura] = Dispositivo.leerMemoria(valorGrupo + posición + entradaElementoRanura);
            if (valorAlmacenar(nombre, longitud, valorEditar, tamañoArchivo) < 0) { TerminalTexto.escribir("Java 파일을 가져오지 못했습니다\n"); return; }
        }
    }
}
