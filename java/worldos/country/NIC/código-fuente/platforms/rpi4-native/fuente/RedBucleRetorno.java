// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Primera capa de red: transmisión IPv4/UDP en bucle local dentro de un núcleo. Las IP externas devuelven ENETUNREACH; no sustituye un controlador de paquetes Ethernet/IP. Ocho extremos, cuatro datagramas por extremo y 512 bytes por datagrama. Todas las llamadas son no bloqueantes. */
public final class RedBucleRetorno {
    static int[] valorUsar = new int[8];
    static int[] valorPuerto = new int[8];
    static int[] dirección = new int[8];
    static int[] valorLadoDelantero = new int[8];
    static int[] númeroElementosElementoLista = new int[8];
    static int[] puertoRecibido = new int[8];
    static int[] longitud = new int[32];
    static int[] puertoEnviado = new int[32];
    static int[] Datos = new int[32 * 512];
    static int[] valorAdelante = new int[512];
    static int extremoSiguiente = 49152;
    static int verificar(int número) { return número >= 32 && número < 40 && valorUsar[número - 32] != 0 ? número - 32 : -1; }
    static boolean solapamientos(int número) {
        for (int entradaElementoRanura = 0; entradaElementoRanura < 8; entradaElementoRanura++) if (valorUsar[entradaElementoRanura] != 0 && valorPuerto[entradaElementoRanura] == número) return true;
        return false;
    }
    static int puertoTemporal() {
        for (int valorIntento = 0; valorIntento < 16; valorIntento++) {
            int candidato = extremoSiguiente++;
            if (extremoSiguiente > 65535) extremoSiguiente = 49152;
            if (!solapamientos(candidato)) return candidato;
        }
        return -98;
    }
    public static int crearEntradaElemento(int valorRegión, int valorClaseTipo, int valorContrato) {
        if (valorRegión != 2) return -97;
        if (valorClaseTipo != 2 || (valorContrato != 0 && valorContrato != 17)) return -93;
        for (int entradaElementoRanura = 0; entradaElementoRanura < 8; entradaElementoRanura++) if (valorUsar[entradaElementoRanura] == 0) {
            valorUsar[entradaElementoRanura] = 1; valorPuerto[entradaElementoRanura] = 0; dirección[entradaElementoRanura] = 0; valorLadoDelantero[entradaElementoRanura] = 0; númeroElementosElementoLista[entradaElementoRanura] = 0; puertoRecibido[entradaElementoRanura] = 0;
            return entradaElementoRanura + 32;
        }
        return -24;
    }
    public static int EmpaquetarEjecutables(int número, int direcciónRed, int númeroPuertoExtremo) {
        int entradaElementoRanura = verificar(número);
        if (entradaElementoRanura < 0) return -9;
        if (direcciónRed != 0 && direcciónRed != 0x7f000001) return -99;
        if (valorPuerto[entradaElementoRanura] != 0 || númeroPuertoExtremo < 0 || númeroPuertoExtremo > 65535) return -22;
        if (númeroPuertoExtremo == 0) númeroPuertoExtremo = puertoTemporal();
        if (númeroPuertoExtremo < 0) return númeroPuertoExtremo;
        if (solapamientos(númeroPuertoExtremo)) return -98;
        valorPuerto[entradaElementoRanura] = númeroPuertoExtremo; dirección[entradaElementoRanura] = direcciónRed; return 0;
    }
    public static int ponerDatos(int número, int valor) {
        if (número < 0 || número >= 512) return -22;
        valorAdelante[número] = valor & 255; return 0;
    }
    public static int leerDatos(int número) { return número >= 0 && número < 512 ? valorAdelante[número] : -22; }
    public static int enviar(int número, int direcciónRed, int númeroPuertoExtremo, int tamaño) {
        int entradaElementoRanura = verificar(número);
        if (entradaElementoRanura < 0) return -9;
        if (direcciónRed != 0x7f000001) return -101;
        if (númeroPuertoExtremo < 1 || númeroPuertoExtremo > 65535) return -22;
        if (tamaño < 0 || tamaño > 512) return -90;
        if (valorPuerto[entradaElementoRanura] == 0) {
            int resultado = EmpaquetarEjecutables(número, 0x7f000001, 0);
            if (resultado < 0) return resultado;
        }
        int valorDestino = -1;
        for (int candidato = 0; candidato < 8; candidato++) if (valorUsar[candidato] != 0 && valorPuerto[candidato] == númeroPuertoExtremo) valorDestino = candidato;
        if (valorDestino < 0) return -111;
        if (númeroElementosElementoLista[valorDestino] == 4) return -11;
        int índicePosición = valorDestino * 4 + (valorLadoDelantero[valorDestino] + númeroElementosElementoLista[valorDestino]) % 4;
        for (int valorByte = 0; valorByte < tamaño; valorByte++) Datos[índicePosición * 512 + valorByte] = valorAdelante[valorByte];
        longitud[índicePosición] = tamaño; puertoEnviado[índicePosición] = valorPuerto[entradaElementoRanura]; númeroElementosElementoLista[valorDestino]++;
        return tamaño;
    }
    public static int recibir(int número, int valorCapacidad) {
        int entradaElementoRanura = verificar(número);
        if (entradaElementoRanura < 0) return -9;
        if (valorCapacidad < 0 || valorCapacidad > 512) return -22;
        if (númeroElementosElementoLista[entradaElementoRanura] == 0) return -11;
        int índicePosición = entradaElementoRanura * 4 + valorLadoDelantero[entradaElementoRanura];
        int tamaño = longitud[índicePosición] < valorCapacidad ? longitud[índicePosición] : valorCapacidad;
        for (int valorByte = 0; valorByte < tamaño; valorByte++) valorAdelante[valorByte] = Datos[índicePosición * 512 + valorByte];
        puertoRecibido[entradaElementoRanura] = puertoEnviado[índicePosición]; valorLadoDelantero[entradaElementoRanura] = (valorLadoDelantero[entradaElementoRanura] + 1) % 4; númeroElementosElementoLista[entradaElementoRanura]--;
        return tamaño;
    }
    public static int leerPuertoExtremo(int número) { int entradaElementoRanura = verificar(número); return entradaElementoRanura < 0 ? -9 : valorPuerto[entradaElementoRanura]; }
    public static int leerDirección(int número) { int entradaElementoRanura = verificar(número); return entradaElementoRanura < 0 ? -9 : dirección[entradaElementoRanura]; }
    public static int extremoEmisor(int número) { int entradaElementoRanura = verificar(número); return entradaElementoRanura < 0 ? -9 : puertoRecibido[entradaElementoRanura]; }
    public static int cerrar(int número) {
        int entradaElementoRanura = verificar(número); if (entradaElementoRanura < 0) return -9;
        valorUsar[entradaElementoRanura] = 0; númeroElementosElementoLista[entradaElementoRanura] = 0; valorPuerto[entradaElementoRanura] = 0; return 0;
    }
}
