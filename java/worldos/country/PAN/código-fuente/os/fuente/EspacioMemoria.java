// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Consulta información de arranque y asigna/libera regiones de tarea fijas de 4 KiB; no es un gestor general de páginas físicas. */
public final class EspacioMemoria {
    static int[] valorSección = new int[8192];
    static int[] valorUsar = new int[8];

    static int analizarEnteroValor(int dirección) {
        return Dispositivo.leerMemoria(dirección) | (Dispositivo.leerMemoria(dirección + 1) << 8)
            | (Dispositivo.leerMemoria(dirección + 2) << 16) | (Dispositivo.leerMemoria(dirección + 3) << 24);
    }

    static int tamañoMemoriaSuperior() {
        int informaciónSistema = Dispositivo.informaciónArranque();
        if (Dispositivo.marcadorArranque() != 0x2badb002 || informaciónSistema == 0 || (analizarEnteroValor(informaciónSistema) & 1) == 0) return -1;
        return analizarEnteroValor(informaciónSistema + 8);
    }

    static int asignarMemoriaAlmacenamiento() {
        for (int número = 0; número < valorUsar.length; número++) {
            if (valorUsar[número] == 0) {
                valorUsar[número] = 1;
                for (int entradaElementoRanura = 0; entradaElementoRanura < 1024; entradaElementoRanura++) valorSección[número * 1024 + entradaElementoRanura] = 0;
                return número;
            }
        }
        return -1;
    }

    static boolean resultadoRetornar(int número) {
        if (número < 0 || número >= valorUsar.length || valorUsar[número] == 0) return false;
        valorUsar[número] = 0;
        return true;
    }

    static int númeroElementosEntradaElementoUsado() {
        int númeroElementosElementoLista = 0;
        for (int número = 0; número < valorUsar.length; número++) númeroElementosElementoLista += valorUsar[número];
        return númeroElementosElementoLista;
    }
}
