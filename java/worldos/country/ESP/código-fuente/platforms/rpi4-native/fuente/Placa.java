// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Frontera de máquina ARM64. Nunca truncar un puntero a un int de Java. */
public final class Placa {
    public static native int leerPíxelPresentar(int posiciónHorizontal, int posiciónVertical);
    public static native void escribirPíxelPresentar(int posiciónHorizontal, int posiciónVertical, int valorColor);
    public static native int controlRemoto(int valorClaseTipo, int acción);
    public static native void comandoRemotoFin(int valorEstadoValor);
    public static native void esperarRemoto(int valorEstadoValor);
    public static native void escribirSerie(int valor);
    public static native int leerSerie();
    public static native int milisegundos();
    public static native int nivelPrivilegioCPU();
    public static native int prepararPantalla();
    public static native int anchuraPantalla();
    public static native int alturaPantalla();
    public static native void ponerPíxelPantalla(int posiciónHorizontal, int posiciónVertical, int valorColor);
    public static native void cederProcesador();
    public static native int crearTarea(int número);
    public static native int estadoValorTarea(int número);
    public static native void detener(int valorEstadoValor);
    public static native int pruebaCpp();
    public static native int ponerEnMarchaProgramaUsuario(int número);
    public static native int comprobarProgramaUsuario();
    public static native int prepararArgumentos(int númeroElementosElementoLista);
    public static native int ejecutarArchivoUsuario();
    public static native int ejecutarArchivoLinux();
    public static native int byteArgumento(int número, int posición, int valor);
    public static native int terminal(int acción);
    public static native int programaUsuarioControl(int acción);
    public static native void entradaSalidaConmutar(int acción);
    public static native int servicioTransferenciaArchivo(int acción);
    public static native int estadoRed(int valorEntradaElemento, int número);
    public static native int ajustesRed(int acción, int dirección, int valorMáscara, int valorPasarela);
    public static native int enviarRespuestaRetorno(int dirección, int valorOrden);
    public static native int leerRespuestaRetorno(int valorEntradaElemento);
    public static native int sistemaConsultar(int valorEntradaElemento, int número);
    public static native void desactivadoAlimentación();
}
