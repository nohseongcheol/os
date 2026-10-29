// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** API exclusiva para ELF de usuario de jkoros; no es JNI para Linux/JVM ni la API java.net. */
public final class Usuario {
    public static native int abrirDescriptorArchivo(int[] nombreEntradaElementoArchivo, int abrirAjustes);
    public static native int leerByteArchivoUno(int descriptorArchivo);
    public static native int escribirByteArchivoUno(int descriptorArchivo, int valorByte);
    public static native int cerrarDescriptorArchivo(int descriptorArchivo);
    public static native int almacenamientoArchivoConfirmar(int descriptorArchivo);
    public static native int leerArchivo(int[] nombre, int[] Datos);
    public static native int escribirValorCarácter(int Caracteres);
    public static native int escribirArchivo(int[] nombre, int[] Datos, int longitud);
    public static native int escribir(String valorContenidoValor);
    public static native int númeroElementosArgumentos();
    public static native String argumentos(int número);
    public static native int permisoEjecución();
    public static native int abrirRed(int puertoLocal);
    public static native int enviarDatos(int valorManejador, int dirección, int puertoDestino, int[] Datos, int longitud);
    public static native int recibirDatos(int valorManejador, int[] Datos, int milisegundosLímite);
    public static native int cerrarRed(int valorManejador);
    public static native int direcciónPropio();
    public static native int direcciónEnviado(int valorManejador);
    public static native int puertoEnviado(int valorManejador);
}
