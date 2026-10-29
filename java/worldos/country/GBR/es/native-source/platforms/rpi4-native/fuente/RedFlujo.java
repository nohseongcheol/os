// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Flujos de bytes con conexión dentro del núcleo: capa socket en bucle local, no pila de paquetes Ethernet/TCP. */
public final class RedFlujo {
    static int[] valorEstadoValor = new int[16], valorPuerto = new int[16], valorEmparejado = new int[16], puertoParRed = new int[16], esperarValor = new int[16], esAsociado = new int[16];
    static int[] valorLadoDelantero = new int[16], númeroValor = new int[16], Datos = new int[16 * 1024];
    static int elementoListaSiguiente = 50000;
    static int verificar(int númeroArchivoAbierto) { return númeroArchivoAbierto >= 40 && númeroArchivoAbierto < 56 && valorEstadoValor[númeroArchivoAbierto - 40] != 0 ? númeroArchivoAbierto - 40 : -1; }
    static boolean esUsarEntrante(int númeroPuerto) { for (int índiceBucle = 0; índiceBucle < 16; índiceBucle++) if (valorEstadoValor[índiceBucle] != 0 && esAsociado[índiceBucle] != 0 && valorPuerto[índiceBucle] == númeroPuerto) return true; return false; }
    public static int crearEntradaElemento() {
        for (int índiceBucle = 0; índiceBucle < 16; índiceBucle++) if (valorEstadoValor[índiceBucle] == 0) { valorEstadoValor[índiceBucle] = 1; puertoParRed[índiceBucle] = valorPuerto[índiceBucle] = valorLadoDelantero[índiceBucle] = númeroValor[índiceBucle] = esperarValor[índiceBucle] = esAsociado[índiceBucle] = 0; valorEmparejado[índiceBucle] = -1; return índiceBucle + 40; }
        return -24;
    }
    public static int EmpaquetarEjecutables(int númeroArchivoAbierto, int DirecciónConectorRed, int númeroPuerto) {
        int índiceBucle = verificar(númeroArchivoAbierto); if (índiceBucle < 0) return -9;
        if (DirecciónConectorRed != 0 && DirecciónConectorRed != 0x7f000001) return -99;
        if (valorEstadoValor[índiceBucle] != 1 || númeroPuerto < 0 || númeroPuerto > 65535) return -22;
        if (númeroPuerto == 0) { do { númeroPuerto = elementoListaSiguiente++; if (elementoListaSiguiente > 65535) elementoListaSiguiente = 50000; } while (esUsarEntrante(númeroPuerto)); }
        if (esUsarEntrante(númeroPuerto)) return -98; valorPuerto[índiceBucle] = númeroPuerto; esAsociado[índiceBucle] = 1; valorEstadoValor[índiceBucle] = 2; return 0;
    }
    public static int escucharExtremo(int númeroArchivoAbierto, int esperaConexiones) { int índiceBucle = verificar(númeroArchivoAbierto); if (índiceBucle < 0) return -9; if (valorEstadoValor[índiceBucle] != 2 || esperaConexiones < 1) return -22; valorEstadoValor[índiceBucle] = 3; return 0; }
    public static int conectar(int númeroArchivoAbierto, int DirecciónConectorRed, int númeroPuerto) {
        int índiceBucle = verificar(númeroArchivoAbierto); if (índiceBucle < 0) return -9; if (DirecciónConectorRed != 0x7f000001) return -101;
        if (númeroPuerto < 1 || númeroPuerto > 65535 || valorEstadoValor[índiceBucle] > 2) return -22;
        int recibirPágina = -1; for (int posiciónInterior = 0; posiciónInterior < 16; posiciónInterior++) if (valorEstadoValor[posiciónInterior] == 3 && valorPuerto[posiciónInterior] == númeroPuerto) recibirPágina = posiciónInterior;
        if (recibirPágina < 0) return -111;
        int esEncolado = 0; for (int posiciónInterior = 0; posiciónInterior < 16; posiciónInterior++) if (esperarValor[posiciónInterior] == recibirPágina + 1) esEncolado++;
        if (esEncolado >= 4) return -11;
        if (valorEstadoValor[índiceBucle] == 1) { int valorProcesado = EmpaquetarEjecutables(númeroArchivoAbierto, 0x7f000001, 0); if (valorProcesado < 0) return valorProcesado; }
        int otro = crearEntradaElemento(); if (otro < 0) return otro; otro -= 40;
        valorEstadoValor[índiceBucle] = valorEstadoValor[otro] = 4; valorEmparejado[índiceBucle] = otro; valorEmparejado[otro] = índiceBucle; valorPuerto[otro] = númeroPuerto; puertoParRed[índiceBucle] = númeroPuerto; puertoParRed[otro] = valorPuerto[índiceBucle]; esperarValor[otro] = recibirPágina + 1; return 0;
    }
    public static int aceptarConexión(int númeroArchivoAbierto) { int índiceBucle = verificar(númeroArchivoAbierto); if (índiceBucle < 0) return -9; if (valorEstadoValor[índiceBucle] != 3) return -22; for (int posiciónInterior = 0; posiciónInterior < 16; posiciónInterior++) if (valorEstadoValor[posiciónInterior] != 0 && esperarValor[posiciónInterior] == índiceBucle + 1) { esperarValor[posiciónInterior] = 0; return posiciónInterior + 40; } return -11; }
    public static int escribir(int númeroArchivoAbierto, int númeroElementosEntradaElemento) {
        int índiceBucle = verificar(númeroArchivoAbierto); if (índiceBucle < 0) return -9; if (valorEstadoValor[índiceBucle] != 4) return -107;
        if (númeroElementosEntradaElemento < 0 || númeroElementosEntradaElemento > 512) return -22; if (númeroElementosEntradaElemento == 0) return 0;
        int posiciónInterior = valorEmparejado[índiceBucle]; if (posiciónInterior < 0) return -32; int númeroElementosTotal = 1024 - númeroValor[posiciónInterior]; if (númeroElementosTotal == 0) return -11; if (númeroElementosTotal > númeroElementosEntradaElemento) númeroElementosTotal = númeroElementosEntradaElemento;
        for (int posiciónComparación = 0; posiciónComparación < númeroElementosTotal; posiciónComparación++) Datos[posiciónInterior * 1024 + (valorLadoDelantero[posiciónInterior] + númeroValor[posiciónInterior] + posiciónComparación) % 1024] = RedBucleRetorno.valorAdelante[posiciónComparación]; númeroValor[posiciónInterior] += númeroElementosTotal; return númeroElementosTotal;
    }
    public static int leer(int númeroArchivoAbierto, int númeroElementosEntradaElemento) {
        int índiceBucle = verificar(númeroArchivoAbierto); if (índiceBucle < 0) return -9; if (valorEstadoValor[índiceBucle] != 4) return -107; if (númeroElementosEntradaElemento < 0 || númeroElementosEntradaElemento > 512) return -22;
        if (númeroElementosEntradaElemento == 0) return 0; if (númeroValor[índiceBucle] == 0) return valorEmparejado[índiceBucle] < 0 ? 0 : -11; if (númeroElementosEntradaElemento > númeroValor[índiceBucle]) númeroElementosEntradaElemento = númeroValor[índiceBucle];
        for (int posiciónComparación = 0; posiciónComparación < númeroElementosEntradaElemento; posiciónComparación++) RedBucleRetorno.valorAdelante[posiciónComparación] = Datos[índiceBucle * 1024 + (valorLadoDelantero[índiceBucle] + posiciónComparación) % 1024]; valorLadoDelantero[índiceBucle] = (valorLadoDelantero[índiceBucle] + númeroElementosEntradaElemento) % 1024; númeroValor[índiceBucle] -= númeroElementosEntradaElemento; return númeroElementosEntradaElemento;
    }
    public static int leerPuertoExtremo(int númeroArchivoAbierto) { int índiceBucle = verificar(númeroArchivoAbierto); return índiceBucle < 0 ? -9 : valorPuerto[índiceBucle]; }
    public static int leerPuertoParRed(int númeroArchivoAbierto) { int índiceBucle = verificar(númeroArchivoAbierto); return índiceBucle < 0 ? -9 : puertoParRed[índiceBucle]; }
    public static int cerrar(int númeroArchivoAbierto) {
        int índiceBucle = verificar(númeroArchivoAbierto); if (índiceBucle < 0) return -9;
        if (valorEstadoValor[índiceBucle] == 3) for (int posiciónInterior = 0; posiciónInterior < 16; posiciónInterior++) if (esperarValor[posiciónInterior] == índiceBucle + 1) { if (valorEmparejado[posiciónInterior] >= 0) valorEmparejado[valorEmparejado[posiciónInterior]] = -1; valorEstadoValor[posiciónInterior] = esperarValor[posiciónInterior] = esAsociado[posiciónInterior] = 0; }
        if (valorEmparejado[índiceBucle] >= 0) valorEmparejado[valorEmparejado[índiceBucle]] = -1; valorEstadoValor[índiceBucle] = esAsociado[índiceBucle] = númeroValor[índiceBucle] = esperarValor[índiceBucle] = 0; return 0;
    }
}
