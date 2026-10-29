// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Enlace SVC exclusivo para herramientas Java de ARM64 EL0. Se construye junto con las fuentes existentes de herramientas x86. */
public final class Usuario {
    public static native int abrirDescriptorArchivo(int[] nombre, int ajustes);
    public static native int leerByteArchivoUno(int entradaElementoDescriptor);
    public static native int escribirByteArchivoUno(int entradaElementoDescriptor, int valor);
    public static native int cerrarDescriptorArchivo(int entradaElementoDescriptor);
    public static native int leerArchivo(int[] nombre, int[] Datos);
    public static native int escribirArchivo(int[] nombre, int[] Datos, int longitud);
    public static native int escribir(String texto);
    public static native int escribirValorCarácter(int valor);
    public static native int númeroElementosArgumentos();
    public static native String argumentos(int número);
    public static native int númeroHerramienta();
    public static native int conexiónPantalla(int acción, int número, int operandoPrimero, int operandoSegundo, int operandoTercero, int operandoCuarto);
    public static native int textoPantalla(int número, int[] texto, int longitud);
    public static native int anchuraPantalla();
    public static native int alturaPantalla();
    public static native int controlFlujo(int acción, int entradaElementoDescriptor, int valor);
    public static native int conectarFlujo(int entradaElementoDescriptor, int dirección, int valorPuerto);
    public static native int abrirRed(int valorPuerto);
    public static native int enviarRed(int entradaElementoDescriptor, int dirección, int valorPuerto, int[] Datos, int longitud);
    public static native int recibirRed(int entradaElementoDescriptor, int[] Datos, int longitud);
    public static native int puertoRed(int entradaElementoDescriptor);
    public static native int milisegundos();
    public static native int esperarImagenPara();
    public static native int rectángulo(int posiciónHorizontal, int posiciónVertical, int extensiónRangoAnchura, int valorAltura, int valorColor);
}
