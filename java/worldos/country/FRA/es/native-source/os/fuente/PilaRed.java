// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** IPv4/ARP/UDP estáticos. Conserva hasta cuatro puertos de comunicación, con un datagrama por puerto. */
public final class PilaRed {
    static final int direcciónPropio = 0xc0a80064; /* ip.conf:IP */
    static final int máscaraRed = 0xffffff00; /* ip.conf:NETMASK */
    static final int valorPasarela = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] marcoEntrada = new int[1536], marcoSalida = new int[1536];
    static int[] puertos = new int[4], longitudRecibido = new int[4], direcciónRecibido = new int[4], númeroPuertoRecibido = new int[4];
    static int[] datosRecibido = new int[4096], dispositivoEncontrado = new int[6];
    static int encontrarHaciaDirección = 0, direcciónEncontrado = 0, valorIdentificador = 0, númeroElementosDescartado = 0;

    static int entero16(int[] índiceMarco, int posición) { return (índiceMarco[posición] << 8) | índiceMarco[posición + 1]; }
    static int entero32(int[] índiceMarco, int posición) { return (entero16(índiceMarco, posición) << 16) | entero16(índiceMarco, posición + 2); }
    static void poner16Bits(int[] índiceMarco, int posición, int valor) { índiceMarco[posición] = (valor >>> 8) & 255; índiceMarco[posición + 1] = valor & 255; }
    static void poner32Bits(int[] índiceMarco, int posición, int valor) { poner16Bits(índiceMarco, posición, valor >>> 16); poner16Bits(índiceMarco, posición + 2, valor); }
    static int valorTotalSuma(int[] índiceMarco, int ponerEnMarcha, int longitud, int valor) {
        for (int número = 0; número < longitud; número += 2)
            valor += (índiceMarco[ponerEnMarcha + número] << 8) | (número + 1 < longitud ? índiceMarco[ponerEnMarcha + número + 1] : 0);
        while ((valor >>> 16) != 0) valor = (valor & 65535) + (valor >>> 16);
        return valor;
    }
    static int sumaComprobaciónEncabezadoSeudo(int valorPartida, int valorLlegada, int longitud) {
        return (valorPartida >>> 16) + (valorPartida & 65535) + (valorLlegada >>> 16) + (valorLlegada & 65535) + 17 + longitud;
    }

    static void procesoLimpiar() {
        for (int número = 0; número < 4; número++) {
            puertos[número] = 0; longitudRecibido[número] = -1; direcciónRecibido[número] = 0; númeroPuertoRecibido[número] = 0;
        }
        for (int número = 0; número < 64; número++) if (ControladorRed.recibir(marcoEntrada) == 0) break;
    }
    static int número(int valorManejador) { return valorManejador >= 3 && valorManejador < 7 && puertos[valorManejador - 3] != 0 ? valorManejador - 3 : -1; }
    static int abrir(int númeroPuerto) {
        if (ControladorRed.direcciónBaseEntradaSalida == 0) return -19;
        if (númeroPuerto < 0 || númeroPuerto > 65535) return -22;
        if (númeroPuerto != 0) for (int número = 0; número < 4; número++) if (puertos[número] == númeroPuerto) return -98;
        for (int número = 0; número < 4; número++) if (puertos[número] == 0) {
            if (númeroPuerto == 0) {
                númeroPuerto = 49152;
                boolean solapamientos = true;
                while (solapamientos) {
                    solapamientos = false;
                    for (int valorLadoDelantero = 0; valorLadoDelantero < 4; valorLadoDelantero++) if (puertos[valorLadoDelantero] == númeroPuerto) solapamientos = true;
                    if (solapamientos) númeroPuerto++;
                }
            }
            puertos[número] = númeroPuerto; longitudRecibido[número] = -1;
            return número + 3;
        }
        return -24;
    }
    static int cerrar(int valorManejador) {
        int entradaElementoRanura = número(valorManejador);
        if (entradaElementoRanura < 0) return -9;
        puertos[entradaElementoRanura] = 0; longitudRecibido[entradaElementoRanura] = -1;
        return 0;
    }
    static int direcciónParRed(int valorManejador) { int entradaElementoRanura = número(valorManejador); return entradaElementoRanura < 0 ? -9 : direcciónRecibido[entradaElementoRanura]; }
    static int númeroPuertoParRed(int valorManejador) { int entradaElementoRanura = número(valorManejador); return entradaElementoRanura < 0 ? -9 : númeroPuertoRecibido[entradaElementoRanura]; }

    static void encabezadoExterior(int valorClaseTipo, boolean valorDifusiónGeneral) {
        for (int número = 0; número < 6; número++) {
            marcoSalida[número] = valorDifusiónGeneral ? 255 : dispositivoEncontrado[número];
            marcoSalida[6 + número] = ControladorRed.direcciónDispositivo[número];
        }
        poner16Bits(marcoSalida, 12, valorClaseTipo);
    }
    static void direcciónPetición(int valorDestino) {
        encabezadoExterior(0x0806, true);
        poner16Bits(marcoSalida, 14, 1); poner16Bits(marcoSalida, 16, 0x0800);
        marcoSalida[18] = 6; marcoSalida[19] = 4; poner16Bits(marcoSalida, 20, 1);
        for (int número = 0; número < 6; número++) {
            marcoSalida[22 + número] = ControladorRed.direcciónDispositivo[número]; marcoSalida[32 + número] = 0;
        }
        poner32Bits(marcoSalida, 28, direcciónPropio); poner32Bits(marcoSalida, 38, valorDestino);
        ControladorRed.enviar(marcoSalida, 42);
    }
    static void direcciónProceso(int longitud) {
        if (longitud < 42 || entero16(marcoEntrada, 14) != 1 || entero16(marcoEntrada, 16) != 0x0800
            || marcoEntrada[18] != 6 || marcoEntrada[19] != 4 || entero32(marcoEntrada, 38) != direcciónPropio) { númeroElementosDescartado++; return; }
        int valorClaseTipo = entero16(marcoEntrada, 20), valorParRed = entero32(marcoEntrada, 28);
        if (valorClaseTipo == 2 && valorParRed == encontrarHaciaDirección) {
            for (int número = 0; número < 6; número++) {
                if (marcoEntrada[6 + número] != marcoEntrada[22 + número] || marcoEntrada[32 + número] != ControladorRed.direcciónDispositivo[número]) return;
            }
            for (int número = 0; número < 6; número++) dispositivoEncontrado[número] = marcoEntrada[22 + número];
            direcciónEncontrado = valorParRed;
        } else if (valorClaseTipo == 1) {
            encabezadoExterior(0x0806, false);
            poner16Bits(marcoSalida, 14, 1); poner16Bits(marcoSalida, 16, 0x0800);
            marcoSalida[18] = 6; marcoSalida[19] = 4; poner16Bits(marcoSalida, 20, 2);
            for (int número = 0; número < 6; número++) {
                marcoSalida[número] = marcoEntrada[22 + número]; marcoSalida[32 + número] = marcoEntrada[22 + número];
                marcoSalida[22 + número] = ControladorRed.direcciónDispositivo[número];
            }
            poner32Bits(marcoSalida, 28, direcciónPropio); poner32Bits(marcoSalida, 38, valorParRed);
            ControladorRed.enviar(marcoSalida, 42);
        }
    }

    static void marcoProceso(int longitud) {
        if (longitud < 14 || longitud > marcoEntrada.length) { númeroElementosDescartado++; return; }
        boolean referenciaPropio = true, valorDifusiónGeneral = true;
        for (int número = 0; número < 6; número++) {
            if (marcoEntrada[número] != ControladorRed.direcciónDispositivo[número]) referenciaPropio = false;
            if (marcoEntrada[número] != 255) valorDifusiónGeneral = false;
        }
        if (!referenciaPropio && !valorDifusiónGeneral) return;
        if (entero16(marcoEntrada, 12) == 0x0806) { direcciónProceso(longitud); return; }
        if (entero16(marcoEntrada, 12) != 0x0800) return;
        if (longitud < 34 || (marcoEntrada[14] >>> 4) != 4) { númeroElementosDescartado++; return; }
        int longitudEncabezado = (marcoEntrada[14] & 15) * 4, longitudTotal = entero16(marcoEntrada, 16);
        if (longitudEncabezado < 20 || longitudEncabezado > 60 || longitudTotal < longitudEncabezado + 8 || longitudTotal > longitud - 14
            || (entero16(marcoEntrada, 20) & 0x3fff) != 0 || marcoEntrada[23] != 17
            || entero32(marcoEntrada, 30) != direcciónPropio || valorTotalSuma(marcoEntrada, 14, longitudEncabezado, 0) != 65535) { númeroElementosDescartado++; return; }
        int ponerEnMarcha = 14 + longitudEncabezado, longitudDatos = entero16(marcoEntrada, ponerEnMarcha + 4);
        if (longitudDatos < 8 || longitudDatos != longitudTotal - longitudEncabezado || longitudDatos > 1032) { númeroElementosDescartado++; return; }
        int valorPartida = entero32(marcoEntrada, 26);
        if (entero16(marcoEntrada, ponerEnMarcha + 6) != 0 && valorTotalSuma(marcoEntrada, ponerEnMarcha, longitudDatos, sumaComprobaciónEncabezadoSeudo(valorPartida, direcciónPropio, longitudDatos)) != 65535) {
            númeroElementosDescartado++; return;
        }
        int valorDestino = entero16(marcoEntrada, ponerEnMarcha + 2);
        for (int entradaElementoRanura = 0; entradaElementoRanura < 4; entradaElementoRanura++) if (puertos[entradaElementoRanura] != 0 && puertos[entradaElementoRanura] == valorDestino) {
            if (longitudRecibido[entradaElementoRanura] >= 0) { númeroElementosDescartado++; return; }
            longitudRecibido[entradaElementoRanura] = longitudDatos - 8; direcciónRecibido[entradaElementoRanura] = valorPartida; númeroPuertoRecibido[entradaElementoRanura] = entero16(marcoEntrada, ponerEnMarcha);
            for (int número = 0; número < longitudDatos - 8; número++) datosRecibido[entradaElementoRanura * 1024 + número] = marcoEntrada[ponerEnMarcha + 8 + número];
            return;
        }
    }

    static void verificar() {
        for (int número = 0; número < 16; número++) {
            int longitud = ControladorRed.recibir(marcoEntrada);
            if (longitud == 0) return;
            marcoProceso(longitud);
        }
    }
    static int encontrarDirección(int dirección) {
        if (dirección == 0 || dirección == -1 || (dirección >>> 28) >= 14 || (dirección >>> 24) == 127 || dirección == direcciónPropio) return -101;
        int elementoListaSiguiente = (dirección & máscaraRed) == (direcciónPropio & máscaraRed) ? dirección : valorPasarela;
        if (elementoListaSiguiente == direcciónEncontrado) return 0;
        encontrarHaciaDirección = elementoListaSiguiente;
        int ponerEnMarcha = Dispositivo.milisegundos(), peticiónSiguiente = ponerEnMarcha;
        while (Dispositivo.milisegundos() - ponerEnMarcha < 1000) {
            if (Dispositivo.milisegundos() - peticiónSiguiente >= 0) { direcciónPetición(elementoListaSiguiente); peticiónSiguiente += 300; }
            verificar();
            if (direcciónEncontrado == elementoListaSiguiente) return 0;
            Dispositivo.cederBrevemente();
        }
        return -110;
    }
    static int enviar(int valorManejador, int dirección, int númeroPuerto, int[] Datos, int longitud) {
        int entradaElementoRanura = número(valorManejador);
        if (entradaElementoRanura < 0) return -9;
        if (ControladorRed.direcciónBaseEntradaSalida == 0) return -19;
        if (númeroPuerto < 1 || númeroPuerto > 65535 || longitud < 0 || longitud > 1024) return -22;
        int resultado = encontrarDirección(dirección);
        if (resultado < 0) return resultado;
        encabezadoExterior(0x0800, false);
        marcoSalida[14] = 0x45; marcoSalida[15] = 0; poner16Bits(marcoSalida, 16, 28 + longitud);
        poner16Bits(marcoSalida, 18, valorIdentificador++); poner16Bits(marcoSalida, 20, 0x4000);
        marcoSalida[22] = 64; marcoSalida[23] = 17; poner16Bits(marcoSalida, 24, 0);
        poner32Bits(marcoSalida, 26, direcciónPropio); poner32Bits(marcoSalida, 30, dirección);
        poner16Bits(marcoSalida, 24, ~valorTotalSuma(marcoSalida, 14, 20, 0));
        poner16Bits(marcoSalida, 34, puertos[entradaElementoRanura]); poner16Bits(marcoSalida, 36, númeroPuerto);
        poner16Bits(marcoSalida, 38, longitud + 8); poner16Bits(marcoSalida, 40, 0);
        for (int número = 0; número < longitud; número++) marcoSalida[42 + número] = Datos[número] & 255;
        int sumaComprobación = (~valorTotalSuma(marcoSalida, 34, longitud + 8, sumaComprobaciónEncabezadoSeudo(direcciónPropio, dirección, longitud + 8))) & 65535;
        poner16Bits(marcoSalida, 40, sumaComprobación == 0 ? 65535 : sumaComprobación);
        resultado = ControladorRed.enviar(marcoSalida, longitud + 42);
        return resultado < 0 ? resultado : longitud;
    }
    static int recibir(int valorManejador, int[] Datos, int valorCapacidad, int valorLímite) {
        int entradaElementoRanura = número(valorManejador);
        if (entradaElementoRanura < 0) return -9;
        int ponerEnMarcha = Dispositivo.milisegundos();
        while (true) {
            verificar();
            int longitud = longitudRecibido[entradaElementoRanura];
            if (longitud >= 0) {
                longitudRecibido[entradaElementoRanura] = -1;
                if (longitud > valorCapacidad) return -90;
                for (int número = 0; número < longitud; número++) Datos[número] = datosRecibido[entradaElementoRanura * 1024 + número];
                return longitud;
            }
            if (valorLímite == 0) return -11;
            if (Dispositivo.milisegundos() - ponerEnMarcha >= valorLímite) return -110;
            Dispositivo.cederBrevemente();
        }
    }
    static void valorEstadoValor() {
        TerminalTexto.escribir(ControladorRed.direcciónBaseEntradaSalida == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        TerminalTexto.escribir("TX: "); TerminalTexto.escribirNúmero(ControladorRed.númeroElementosTransmitir);
        TerminalTexto.escribir(" RX: "); TerminalTexto.escribirNúmero(ControladorRed.recibirNúmeroElementos);
        TerminalTexto.escribir(" DROP: "); TerminalTexto.escribirNúmero(númeroElementosDescartado);
        TerminalTexto.escribir("\n");
    }
}
