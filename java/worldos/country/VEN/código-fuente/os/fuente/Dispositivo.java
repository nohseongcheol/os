// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Frontera native restringida del compilador, solo para instrucciones x86 y acceso a direcciones físicas. */
public final class Dispositivo {
    public static native int memoriaArchivo();
    public static native int paqueteArchivoJava();
    public static native int tamañoPaqueteArchivoJava();
    public static native int leerByteEntradaSalida(int número);
    public static native void escribirByteEntradaSalida(int número, int valor);
    public static native int leerMemoria(int dirección);
    public static native void escribirMemoria(int dirección, int valor);
    public static native int marcadorArranque();
    public static native int informaciónArranque();
    public static native int usoArreglo();
    public static native void cederBrevemente();
    public static native void ejecuciónDetenerMáquina();
    public static native void terminarPrueba(int valor);
    public static native int leerEnteroValorEntradaSalida(int número);
    public static native void escribirEnteroValorEntradaSalida(int número, int valor);
    public static native void escribirCortoEntradaSalida(int número, int valor);
    public static native int leerCortoEntradaSalida(int número);
    public static native void prepararProgramaUsuario();
    public static native void contenidoBorrarContenidoUsuario();
    public static native int ponerEnMarchaProgramaUsuario(int direcciónEntradaElemento, int direcciónPilaOperando);
    public static native int milisegundos();
    public static native int milisegundosRestanteUsuario();
    public static native int PaqueteCódigoEjecutable();
    public static native int tamañoPaqueteCódigoEjecutable();
    public static native int memoriaRed();
}
