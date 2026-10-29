// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Prueba el retorno circular real del anillo de recepción RTL8139 con datagramas de longitud máxima e impar. */
public final class bucleRed {
    public static int ponerEnMarcha() {
        if (Usuario.númeroElementosArgumentos() != 1) { Usuario.escribir("Usage: run stress PORT\n"); return 2; }
        String texto = Usuario.argumentos(0);
        int valorPuerto = 0;
        for (int número = 0; número < texto.length(); número++) {
            if (texto.charAt(número) < '0' || texto.charAt(número) > '9' || valorPuerto > 6553) return 2;
            valorPuerto = valorPuerto * 10 + texto.charAt(número) - '0';
        }
        if (valorPuerto < 1 || valorPuerto > 65535) return 2;
        int valorManejador = Usuario.abrirRed(0);
        if (valorManejador < 0) return 3;
        int[] Datos = new int[1024];
        for (int ordinalIteración = 0; ordinalIteración < 24; ordinalIteración++) {
            int longitud = 1024 - (ordinalIteración & 1);
            for (int número = 0; número < longitud; número++) Datos[número] = (número + ordinalIteración) & 255;
            if (Usuario.enviarDatos(valorManejador, 0x0a000202, valorPuerto, Datos, longitud) != longitud) return 4;
            if (Usuario.recibirDatos(valorManejador, Datos, 300) != longitud) return 5;
            for (int número = 0; número < longitud; número++) if (Datos[número] != ((número + ordinalIteración) & 255)) return 6;
        }
        Usuario.cerrarRed(valorManejador);
        Usuario.escribir("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
