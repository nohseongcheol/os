// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Sectores lógicos de 512 bytes del primer dispositivo IDE. Esta capa no formatea ni borra dispositivos arbitrarios. */
public final class ConexiónAlmacenamiento {
    static boolean esDisponible = false;
    static int[] datosSección = new int[512];
    static void esperarBrevemente() {
        for (int número = 0; número < 4; número++) Dispositivo.leerByteEntradaSalida(0x3f6);
    }
    static int esperarListoHasta(boolean requeridoDatos) {
        int ponerEnMarcha = Dispositivo.milisegundos();
        while (Dispositivo.milisegundos() - ponerEnMarcha < 500) {
            int valorEstadoValor = Dispositivo.leerByteEntradaSalida(0x1f7);
            if (valorEstadoValor == 0 || valorEstadoValor == 255) return -19;
            if ((valorEstadoValor & 128) == 0) {
                if ((valorEstadoValor & 33) != 0) return -5;
                if (!requeridoDatos || (valorEstadoValor & 8) != 0) return 0;
            }
            Dispositivo.cederBrevemente();
        }
        return -110;
    }
    static int petición(int valorSección, int comando) {
        if (valorSección < 0 || valorSección >= 2048) return -22;
        Dispositivo.escribirByteEntradaSalida(0x3f6, 2); // Sondeo; no se usa la IRQ IDE.
        Dispositivo.escribirByteEntradaSalida(0x1f6, 0xe0); esperarBrevemente();
        int resultado = esperarListoHasta(false);
        if (resultado < 0) return resultado;
        Dispositivo.escribirByteEntradaSalida(0x1f2, 1);
        Dispositivo.escribirByteEntradaSalida(0x1f3, valorSección & 255);
        Dispositivo.escribirByteEntradaSalida(0x1f4, (valorSección >>> 8) & 255);
        Dispositivo.escribirByteEntradaSalida(0x1f5, 0);
        Dispositivo.escribirByteEntradaSalida(0x1f7, comando); esperarBrevemente();
        return esperarListoHasta(true);
    }
    static int leer(int valorSección) {
        int resultado = petición(valorSección, 0x20);
        if (resultado < 0) return resultado;
        for (int número = 0; número < 256; número++) {
            int valor = Dispositivo.leerCortoEntradaSalida(0x1f0);
            datosSección[número * 2] = valor & 255; datosSección[número * 2 + 1] = valor >>> 8;
        }
        esperarBrevemente(); return esperarListoHasta(false);
    }
    static int escribir(int valorSección) {
        if (!esDisponible || valorSección < 1 || valorSección > 518) return -19;
        int resultado = petición(valorSección, 0x30);
        if (resultado < 0) return resultado;
        for (int número = 0; número < 256; número++)
            Dispositivo.escribirCortoEntradaSalida(0x1f0, datosSección[número * 2] | datosSección[número * 2 + 1] << 8);
        esperarBrevemente(); return esperarListoHasta(false);
    }
    static int salidaVaciarBúfer() {
        if (!esDisponible) return -19;
        Dispositivo.escribirByteEntradaSalida(0x1f7, 0xe7); esperarBrevemente();
        return esperarListoHasta(false);
    }
    static int analizarEnteroValor(int posición) {
        return datosSección[posición] | datosSección[posición + 1] << 8 | datosSección[posición + 2] << 16 | datosSección[posición + 3] << 24;
    }
    static void escribirValorEnteroValor(int posición, int valor) {
        for (int número = 0; número < 4; número++) datosSección[posición + número] = (valor >>> (número * 8)) & 255;
    }
}
