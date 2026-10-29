// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Entrada Java invocada tras el arranque real, independiente de una JVM y del sistema anfitrión. */
public final class Núcleo {
    static int valorTotal(int terminación) {
        int valorTotalSuma = 0;
        for (int número = 1; número <= terminación; número++) valorTotalSuma += número;
        return valorTotalSuma;
    }

    static boolean Pruebas() {
        int[] valores = new int[4];
        valores[2] = valorTotal(10);
        int valorNegativo = -7;
        int valorMínimo = 0x80000000;
        int resultadoDivisión = -1;
        int número = EspacioMemoria.asignarMemoriaAlmacenamiento();
        boolean valorPaso = valores[0] == 0 && valores[2] == 55 && valores.length == 4
            && valorNegativo / 3 == -2 && valorNegativo % 3 == -1 && valorMínimo / resultadoDivisión == valorMínimo
            && valorMínimo % resultadoDivisión == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && número >= 0 && EspacioMemoria.resultadoRetornar(número) && !EspacioMemoria.resultadoRetornar(número);
        TerminalTexto.escribir(valorPaso ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return valorPaso;
    }

    public static void ponerEnMarcha() {
        TerminalTexto.preparar();
        TerminalTexto.escribir("JKOROS NATIVE JAVA\n");
        TerminalTexto.escribir("Java 기계어 valorNúcleo ponerEnMarcha\n");
        if (Dispositivo.marcadorArranque() != 0x2badb002) {
            TerminalTexto.escribir("BAD MULTIBOOT MAGIC\n");
            Dispositivo.ejecuciónDetenerMáquina();
        }
        if (!Pruebas()) Dispositivo.ejecuciónDetenerMáquina();
        if (EspacioMemoria.tamañoMemoriaSuperior() < 15360) {
            TerminalTexto.escribir("At least 16 MiB RAM required\n");
            Dispositivo.ejecuciónDetenerMáquina();
        }
        Dispositivo.prepararProgramaUsuario();
        TerminalTexto.escribir("USER ELF: ring 3 / paging / int 0x80\n");
        ControladorRed.preparar();
        PilaRed.procesoLimpiar();
        SistemaArchivosMemoria.preparar();
        PersistenciaArchivos.preparar();
        IntérpreteComandos.ponerEnMarcha();
    }
}
