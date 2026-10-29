// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.util.Arrays;

/** Invoca el gestor real del protocolo Java en una JVM para comprobar rápidamente los límites y las entradas dañadas. */
public final class PruebaPaqueteDatos {
    static int númeroElementosRepetición = 0;
    static void verificar(boolean valor) { if (!valor) throw new AssertionError("case " + númeroElementosRepetición); númeroElementosRepetición++; }
    static int sumaComprobación(int[] valor, int ponerEnMarcha, int longitud, int estadoValorInicialValor) {
        int valorTotalSuma = estadoValorInicialValor;
        for (int número = 0; número < longitud; número++) valorTotalSuma += valor[ponerEnMarcha + número] << ((número & 1) == 0 ? 8 : 0);
        valorTotalSuma = (valorTotalSuma & 65535) + (valorTotalSuma >>> 16);
        valorTotalSuma = (valorTotalSuma & 65535) + (valorTotalSuma >>> 16);
        return ~valorTotalSuma & 65535;
    }
    static void preparar(int longitud) {
        PilaRed.procesoLimpiar();
        verificar(PilaRed.abrir(5000) == 3);
        int[] índiceMarco = PilaRed.marcoEntrada;
        Arrays.fill(índiceMarco, 0);
        for (int número = 0; número < 6; número++) índiceMarco[número] = ControladorRed.direcciónDispositivo[número];
        PilaRed.poner16Bits(índiceMarco, 12, 0x0800);
        índiceMarco[14] = 0x45; índiceMarco[22] = 64; índiceMarco[23] = 17;
        PilaRed.poner16Bits(índiceMarco, 16, 28 + longitud);
        PilaRed.poner32Bits(índiceMarco, 26, 0x0a000202); PilaRed.poner32Bits(índiceMarco, 30, PilaRed.direcciónPropio);
        PilaRed.poner16Bits(índiceMarco, 34, 4321); PilaRed.poner16Bits(índiceMarco, 36, 5000); PilaRed.poner16Bits(índiceMarco, 38, longitud + 8);
        for (int número = 0; número < longitud; número++) índiceMarco[42 + número] = número & 255;
        establecerSumaComprobación(longitud);
    }
    static void establecerSumaComprobación(int longitud) {
        int[] índiceMarco = PilaRed.marcoEntrada;
        PilaRed.poner16Bits(índiceMarco, 24, 0); PilaRed.poner16Bits(índiceMarco, 40, 0);
        PilaRed.poner16Bits(índiceMarco, 24, sumaComprobación(índiceMarco, 14, 20, 0));
        int estadoValorInicialValor = PilaRed.sumaComprobaciónEncabezadoSeudo(PilaRed.entero32(índiceMarco, 26), PilaRed.direcciónPropio, longitud + 8);
        int valorTotalSuma = sumaComprobación(índiceMarco, 34, longitud + 8, estadoValorInicialValor);
        PilaRed.poner16Bits(índiceMarco, 40, valorTotalSuma == 0 ? 65535 : valorTotalSuma);
    }
    static void rechazarValor(int longitud) { PilaRed.marcoProceso(longitud); verificar(PilaRed.longitudRecibido[0] == -1); }
    public static void main(String[] argumentos) {
        for (int longitud : new int[]{0, 1, 2, 7, 1023, 1024}) {
            preparar(longitud); PilaRed.marcoProceso(longitud + 42);
            verificar(PilaRed.longitudRecibido[0] == longitud);
            verificar(PilaRed.direcciónRecibido[0] == 0x0a000202 && PilaRed.númeroPuertoRecibido[0] == 4321);
            for (int número = 0; número < longitud; número++) verificar(PilaRed.datosRecibido[número] == (número & 255));
        }
        for (int longitud = 0; longitud < 42; longitud++) { preparar(0); rechazarValor(longitud); }
        preparar(1025); rechazarValor(1067);
        preparar(2); PilaRed.marcoEntrada[24] ^= 1; rechazarValor(44);
        preparar(2); PilaRed.marcoEntrada[42] ^= 1; rechazarValor(44);
        preparar(2); PilaRed.poner16Bits(PilaRed.marcoEntrada, 38, 7); rechazarValor(44);
        preparar(2); PilaRed.poner16Bits(PilaRed.marcoEntrada, 38, 65535); rechazarValor(44);
        preparar(2); PilaRed.marcoEntrada[14] = 0x4f; rechazarValor(44);
        preparar(2); PilaRed.marcoEntrada[14] = 0x44; rechazarValor(44);
        preparar(2); PilaRed.marcoEntrada[20] = 0x20; establecerSumaComprobación(2); rechazarValor(44);
        preparar(2); PilaRed.marcoEntrada[21] = 1; establecerSumaComprobación(2); rechazarValor(44);
        preparar(2); PilaRed.marcoEntrada[33] = 99; establecerSumaComprobación(2); rechazarValor(44);
        preparar(2); PilaRed.marcoEntrada[0] ^= 1; rechazarValor(44);
        preparar(2); PilaRed.marcoEntrada[23] = 6; establecerSumaComprobación(2); rechazarValor(44);
        preparar(2); PilaRed.poner16Bits(PilaRed.marcoEntrada, 40, 0); PilaRed.marcoProceso(44); verificar(PilaRed.longitudRecibido[0] == 2);
        int[] resultado = new int[4];
        verificar(PilaRed.recibir(3, resultado, 1, 0) == -90);
        verificar(PilaRed.recibir(3, resultado, 4, 0) == -11);
        preparar(2); PilaRed.marcoProceso(44); int descartarValor = PilaRed.númeroElementosDescartado;
        PilaRed.marcoProceso(44); verificar(PilaRed.númeroElementosDescartado == descartarValor + 1);
        PilaRed.procesoLimpiar(); verificar(PilaRed.abrir(5000) == 3);
        verificar(PilaRed.abrir(5000) == -98); verificar(PilaRed.abrir(0) == 4);
        verificar(PilaRed.abrir(0) == 5); verificar(PilaRed.abrir(0) == 6); verificar(PilaRed.abrir(0) == -24);
        verificar(PilaRed.cerrar(4) == 0); verificar(PilaRed.cerrar(4) == -9);
        PilaRed.direcciónEncontrado = PilaRed.valorPasarela;
        verificar(PilaRed.enviar(3, PilaRed.valorPasarela, 4321, new int[]{1, 2, 3}, 3) == 3);
        int[] tieneEnviado = ControladorRed.valorReciente;
        verificar(sumaComprobación(tieneEnviado, 14, 20, 0) == 0);
        verificar(sumaComprobación(tieneEnviado, 34, 11, PilaRed.sumaComprobaciónEncabezadoSeudo(PilaRed.direcciónPropio, PilaRed.valorPasarela, 11)) == 0);
        verificar(tieneEnviado[42] == 1 && tieneEnviado[44] == 3);
        System.out.println("PACKET TEST PASS: " + númeroElementosRepetición + " assertions");
    }
}
