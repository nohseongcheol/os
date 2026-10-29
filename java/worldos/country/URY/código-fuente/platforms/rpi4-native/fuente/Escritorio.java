// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Pequeño lanzador sobre el búfer de imagen, controlado mediante TAB/ENTER/Q por UART. Interfaz limitada con una fuente latina propia de 5x7, sin Swing, USB HID ni método de entrada completo. */
public final class Escritorio {
    static String valoresCarácter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.:";
    // Siete filas por glifo, cada una expresada mediante dos dígitos hexadecimales. Fuente de 5x7 definida por el proyecto.
    static String listaFormas =
        "0E11111F111111" + "1E11111E11111E" + "0F10101010100F" + "1E11111111111E" +
        "1F10101E10101F" + "1F10101E101010" + "0F10101711110F" + "1111111F111111" +
        "0E04040404040E" + "0702020212120C" + "11121418141211" + "1010101010101F" +
        "111B1515111111" + "11191915131311" + "0E11111111110E" + "1E11111E101010" +
        "0E11111115120D" + "1E11111E141211" + "0F10100E01011E" + "1F040404040404" +
        "1111111111110E" + "11111111110A04" + "11111115151B11" + "11110A040A1111" +
        "11110A04040404" + "1F01020408101F" + "0E11131519110E" + "040C040404040E" +
        "0E11010204081F" + "1E01010601011E" + "02060A121F0202" + "1F10101E01011E" +
        "0E10101E11110E" + "1F010204080808" + "0E11110E11110E" + "0E11110F01010E" +
        "0004041F040400" + "0000001F000000" + "00000000000C0C" + "000C0C000C0C00";
    static int valorDígito(int valorCarácter) { return valorCarácter <= '9' ? valorCarácter - '0' : valorCarácter - 'A' + 10; }
    static void texto(int posiciónHorizontal, int posiciónVertical, String valorContenidoValor, int valorColor) {
        for (int valorCarácter = 0; valorCarácter < valorContenidoValor.length(); valorCarácter++) {
            int valorEncontrado = -1;
            for (int candidato = 0; candidato < valoresCarácter.length(); candidato++) if (valoresCarácter.charAt(candidato) == valorContenidoValor.charAt(valorCarácter)) valorEncontrado = candidato;
            if (valorEncontrado < 0) continue;
            for (int valorFila = 0; valorFila < 7; valorFila++) {
                int posición = valorEncontrado * 14 + valorFila * 2;
                int valorBit = valorDígito(listaFormas.charAt(posición)) * 16 + valorDígito(listaFormas.charAt(posición + 1));
                for (int valorColumna = 0; valorColumna < 5; valorColumna++) if ((valorBit & (16 >> valorColumna)) != 0)
                    Núcleo.rectángulo(posiciónHorizontal + valorCarácter * 12 + valorColumna * 2, posiciónVertical + valorFila * 2, 2, 2, valorColor);
            }
        }
    }
    static void pantallaPintar(int valorSelección, String valorEstadoValor) {
        Núcleo.rectángulo(0, 0, Placa.anchuraPantalla(), Placa.alturaPantalla(), 0x302018);
        Núcleo.rectángulo(32, 24, 576, 432, 0xefe8e2);
        Núcleo.rectángulo(32, 24, 576, 48, 0x905020);
        texto(52, 40, "JKOROS PROGRAMS", 0xffffff);
        for (int número = 0; número < 5; número++) {
            Núcleo.rectángulo(64, 112 + número * 52, 512, 40, número == valorSelección ? 0xd0a040 : 0xd8d0c8);
            texto(84, 128 + número * 52, número == 0 ? "RUN C++ FILE PROGRAM" : número == 1 ? "RUN UDP LOOPBACK" : número == 2 ? "COMPILE AND RUN JAVA" : número == 3 ? "RUN MICROPYTHON" : "OPEN TERMINAL", 0x201810);
        }
        texto(68, 384, valorEstadoValor, 0x205020);
        texto(52, 420, "TAB SELECT  ENTER RUN  Q EXIT", 0x302018);
    }
    public static void ejecutarComando() {
        if (Placa.prepararPantalla() == 0) { EntradaSalidaTerminal.escribir("GUI unavailable\n"); return; }
        int valorSelección = 0;
        String valorEstadoValor = "READY";
        boolean líneaElementoPrevio = IntérpreteComandos.líneaElementoPrevio;
        pantallaPintar(valorSelección, valorEstadoValor);
        EntradaSalidaTerminal.escribir("GUI READY: UART TAB selects, ENTER runs, Q exits\n");
        while (true) {
            int valorEntrada = Placa.leerSerie();
            if (valorEntrada < 0) { Placa.cederProcesador(); continue; }
            if (valorEntrada == 10 && líneaElementoPrevio) { líneaElementoPrevio = false; continue; }
            líneaElementoPrevio = valorEntrada == 13;
            if (valorEntrada >= '1' && valorEntrada <= '5') { valorSelección = valorEntrada - '1'; valorEntrada = 13; }
            if (valorEntrada == 't' || valorEntrada == 'T') { IntérpreteComandos.terminal(false); return; }
            if (valorEntrada == 'q' || valorEntrada == 'Q' || valorEntrada == 27) break;
            if (valorEntrada == 9 || valorEntrada == 'j') {
                valorSelección = (valorSelección + 1) % 5; pantallaPintar(valorSelección, valorEstadoValor); EntradaSalidaTerminal.escribir("GUI FOCUS "); EntradaSalidaTerminal.númeroValor(valorSelección); EntradaSalidaTerminal.Caracteres(10);
            } else if (valorEntrada == 13 || valorEntrada == 10) {
                if (valorSelección == 4) { IntérpreteComandos.terminal(false); return; }
                int resultado;
                if (valorSelección < 2) resultado = Placa.ponerEnMarchaProgramaUsuario(valorSelección == 0 ? 0 : 9);
                else if (valorSelección == 2) {
                    resultado = IntérpreteComandos.ponerEnMarchaEjemplo(10, "Hello.java");
                    if (resultado == 0) resultado = IntérpreteComandos.ponerEnMarchaEjemplo(11, "Hello");
                } else resultado = IntérpreteComandos.ponerEnMarchaEjemplo(12, "hello.py");
                valorEstadoValor = resultado != 0 ? "PROGRAM FAILED" : valorSelección == 0 ? "C++ FILE OK" : valorSelección == 1 ? "UDP LOOPBACK OK" : valorSelección == 2 ? "JAVA OK" : "MICROPYTHON OK";
                pantallaPintar(valorSelección, valorEstadoValor);
                EntradaSalidaTerminal.escribir("GUI ACTION "); EntradaSalidaTerminal.númeroValor(valorSelección); EntradaSalidaTerminal.escribir(" RESULT "); EntradaSalidaTerminal.númeroValor(resultado); EntradaSalidaTerminal.Caracteres(10);
            }
        }
        Núcleo.Pantalla();
        EntradaSalidaTerminal.escribir("GUI EXIT\n");
    }
}
