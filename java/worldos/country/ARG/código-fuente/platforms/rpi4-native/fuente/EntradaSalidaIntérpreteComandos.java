// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Las tuberías se ejecutan secuencialmente en bloques de 16 KiB. No simulan procesos ni tuberías concurrentes. */
public final class EntradaSalidaIntérpreteComandos {
    static int[] datosEntrada = new int[16384], datosSalida = new int[16384];
    static int longitudEntrada, posiciónEntrada, longitudSalida, archivoEntrada = -1, archivoSalida = -1;
    static boolean entradaTubería, salidaTubería;
    static int valorFallo;
    static boolean permitirInteractivo = true;
    public static int esInteractivo() { return permitirInteractivo && archivoEntrada < 3 && archivoSalida < 3 && !entradaTubería && !salidaTubería ? 1 : 0; }
    public static int Salida(int valorCanal, int valor) {
        if (valorCanal != 1) return 0;
        if (archivoSalida >= 3) { int valorProcesado = ArchivosMemoria.escribir(archivoSalida, valor); if (valorProcesado < 0) valorFallo = valorProcesado; return 1; }
        if (!salidaTubería) return 0;
        if (longitudSalida == datosSalida.length) valorFallo = -28;
        else datosSalida[longitudSalida++] = valor;
        return 1;
    }
    public static int valorEntrada() {
        if (archivoEntrada >= 3) { int valorProcesado = ArchivosMemoria.leer(archivoEntrada); return valorProcesado == 256 ? -2 : valorProcesado; }
        if (entradaTubería) return posiciónEntrada < longitudEntrada ? datosEntrada[posiciónEntrada++] : -2;
        return -3; // Transmitir a UART.
    }
    static void ponerEnMarcha(boolean tuberíaPrevio, boolean tuberíaPosiciónFinal) {
        entradaTubería = tuberíaPrevio; salidaTubería = tuberíaPosiciónFinal;
        posiciónEntrada = 0; longitudSalida = 0; archivoEntrada = -1; archivoSalida = -1; valorFallo = 0;
    }
    static void terminación() {
        Placa.entradaSalidaConmutar(0);
        if (archivoEntrada >= 3) ArchivosMemoria.cerrar(archivoEntrada);
        if (archivoSalida >= 3) ArchivosMemoria.cerrar(archivoSalida);
        if (salidaTubería) { longitudEntrada = longitudSalida; for (int índiceBucle = 0; índiceBucle < longitudSalida; índiceBucle++) datosEntrada[índiceBucle] = datosSalida[índiceBucle]; }
        archivoEntrada = -1; archivoSalida = -1; entradaTubería = false; salidaTubería = false;
    }
}
