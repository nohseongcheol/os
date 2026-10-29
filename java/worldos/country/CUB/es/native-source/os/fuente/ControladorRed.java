// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), un búfer de envío y un anillo de recepción de 8 KiB. Usa sondeo en lugar de interrupciones. */
public final class ControladorRed {
    static int direcciónBaseEntradaSalida = 0;
    static int recibirPosición = 0, ranuraTransmitir = 0;
    static int[] direcciónDispositivo = new int[6];
    static int númeroElementosTransmitir = 0, recibirNúmeroElementos = 0, númeroElementosError = 0;

    static int leerAjustes(int númeroDispositivo, int posición) {
        Dispositivo.escribirEnteroValorEntradaSalida(0xcf8, 0x80000000 | (númeroDispositivo << 11) | posición);
        return Dispositivo.leerEnteroValorEntradaSalida(0xcfc);
    }

    static boolean preparar() {
        int númeroDispositivo = -1;
        for (int número = 0; número < 32; número++) {
            if (leerAjustes(número, 0) == 0x813910ec) { númeroDispositivo = número; break; }
        }
        if (númeroDispositivo < 0) return false;
        int valorPredeterminado = leerAjustes(númeroDispositivo, 0x10);
        if ((valorPredeterminado & 1) == 0 || (valorPredeterminado & 0xfffffffc) < 0x100 || (valorPredeterminado & 0xfffffffc) > 65535) return false;
        direcciónBaseEntradaSalida = valorPredeterminado & 0xfffc;
        int comando = leerAjustes(númeroDispositivo, 4);
        Dispositivo.escribirEnteroValorEntradaSalida(0xcf8, 0x80000004 | (númeroDispositivo << 11));
        Dispositivo.escribirCortoEntradaSalida(0xcfc, comando | 5); // Activar I/O y el dominio del bus; no modificar los bits de estado PCI.
        Dispositivo.escribirByteEntradaSalida(direcciónBaseEntradaSalida + 0x52, 0);
        if (!reiniciarValor()) { direcciónBaseEntradaSalida = 0; return false; }
        for (int número = 0; número < 6; número++) direcciónDispositivo[número] = Dispositivo.leerByteEntradaSalida(direcciónBaseEntradaSalida + número);
        return true;
    }

    static boolean reiniciarValor() {
        Dispositivo.escribirByteEntradaSalida(direcciónBaseEntradaSalida + 0x37, 0x10);
        int ponerEnMarcha = Dispositivo.milisegundos();
        while ((Dispositivo.leerByteEntradaSalida(direcciónBaseEntradaSalida + 0x37) & 0x10) != 0)
            if (Dispositivo.milisegundos() - ponerEnMarcha > 100) return false;
        recibirPosición = 0; ranuraTransmitir = 0;
        Dispositivo.escribirEnteroValorEntradaSalida(direcciónBaseEntradaSalida + 0x30, Dispositivo.memoriaRed());
        for (int número = 0; número < 4; número++) Dispositivo.escribirEnteroValorEntradaSalida(direcciónBaseEntradaSalida + 0x20 + número * 4, Dispositivo.memoriaRed() + 12288);
        Dispositivo.escribirCortoEntradaSalida(direcciónBaseEntradaSalida + 0x3c, 0);
        Dispositivo.escribirCortoEntradaSalida(direcciónBaseEntradaSalida + 0x3e, 0xffff);
        Dispositivo.escribirByteEntradaSalida(direcciónBaseEntradaSalida + 0x37, 0x0c);
        Dispositivo.escribirEnteroValorEntradaSalida(direcciónBaseEntradaSalida + 0x44, 0x0000e78a); // Aceptar dirección propia y difusión; almacenamiento contiguo al volver al inicio, 8 KiB.
        Dispositivo.escribirEnteroValorEntradaSalida(direcciónBaseEntradaSalida + 0x40, 0x03000600);
        return true;
    }

    static int enviar(int[] Datos, int longitud) {
        if (direcciónBaseEntradaSalida == 0) return -19;
        if (longitud < 14 || longitud > 1514) return -90;
        int puertoEstado = direcciónBaseEntradaSalida + 0x10 + ranuraTransmitir * 4;
        int ponerEnMarcha = Dispositivo.milisegundos();
        while ((Dispositivo.leerEnteroValorEntradaSalida(puertoEstado) & 0x2000) == 0)
            if (Dispositivo.milisegundos() - ponerEnMarcha > 100) return -110;
        int tamaño = longitud < 60 ? 60 : longitud;
        for (int número = 0; número < tamaño; número++)
            Dispositivo.escribirMemoria(Dispositivo.memoriaRed() + 12288 + número, número < longitud ? Datos[número] : 0);
        Dispositivo.escribirEnteroValorEntradaSalida(puertoEstado, tamaño | 0x00080000);
        ponerEnMarcha = Dispositivo.milisegundos();
        while ((Dispositivo.leerEnteroValorEntradaSalida(puertoEstado) & 0xe0008000) == 0)
            if (Dispositivo.milisegundos() - ponerEnMarcha > 100) return -110;
        if ((Dispositivo.leerEnteroValorEntradaSalida(puertoEstado) & 0x8000) == 0) { númeroElementosError++; return -5; }
        ranuraTransmitir = (ranuraTransmitir + 1) & 3;
        númeroElementosTransmitir++;
        return longitud;
    }

    static int recibir(int[] Datos) {
        if (direcciónBaseEntradaSalida == 0) return 0;
        if ((Dispositivo.leerByteEntradaSalida(direcciónBaseEntradaSalida + 0x3e) & 0x50) != 0) {
            númeroElementosError++;
            if (!reiniciarValor()) direcciónBaseEntradaSalida = 0;
            return 0;
        }
        if ((Dispositivo.leerByteEntradaSalida(direcciónBaseEntradaSalida + 0x37) & 1) != 0) return 0;
        int valorCabecera = Dispositivo.memoriaRed() + recibirPosición;
        int valorEstadoValor = GestiónEjecución.valorCorto(valorCabecera), tamaño = GestiónEjecución.valorCorto(valorCabecera + 2);
        if (tamaño == 0xfff0) return 0; // DMA en curso.
        if (tamaño < 4 || tamaño > 1518) {
            númeroElementosError++;
            if (!reiniciarValor()) direcciónBaseEntradaSalida = 0;
            return 0;
        }
        int longitud = tamaño - 4;
        if ((valorEstadoValor & 1) != 0) {
            for (int número = 0; número < longitud; número++) Datos[número] = Dispositivo.leerMemoria(valorCabecera + 4 + número);
            recibirNúmeroElementos++;
        } else { longitud = 0; númeroElementosError++; }
        recibirPosición = (recibirPosición + tamaño + 4 + 3) & ~3;
        recibirPosición &= 8191;
        Dispositivo.escribirCortoEntradaSalida(direcciónBaseEntradaSalida + 0x38, (recibirPosición - 16) & 65535);
        Dispositivo.escribirCortoEntradaSalida(direcciónBaseEntradaSalida + 0x3e, 0x000f);
        return longitud;
    }
}
