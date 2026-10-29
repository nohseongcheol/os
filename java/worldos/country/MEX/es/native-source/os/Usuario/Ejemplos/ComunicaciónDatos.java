// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class ComunicaciónDatos {
    static int valorDígito(String texto) {
        if (texto == null || texto.length() == 0) return -1;
        int resultado = 0;
        for (int número = 0; número < texto.length(); número++) {
            int valor = texto.charAt(número) - '0';
            if (valor < 0 || valor > 9 || resultado > 6553) return -1;
            resultado = resultado * 10 + valor;
            if (resultado > 65535) return -1;
        }
        return resultado;
    }
    static int dirección(String texto) {
        if (texto == null) return 0;
        int valor = 0, resultado = 0, valorSubparte = 0, dígitos = 0;
        for (int número = 0; número <= texto.length(); número++) {
            int Caracteres = número == texto.length() ? '.' : texto.charAt(número);
            if (Caracteres == '.') {
                if (dígitos == 0 || valorSubparte == 4) return 0;
                resultado = (resultado << 8) | valor; valorSubparte++; valor = 0; dígitos = 0;
            } else {
                if (Caracteres < '0' || Caracteres > '9') return 0;
                valor = valor * 10 + Caracteres - '0';
                if (++dígitos > 3 || valor > 255) return 0;
            }
        }
        return valorSubparte == 4 ? resultado : 0;
    }
    public static int ponerEnMarcha() {
        if (Usuario.númeroElementosArgumentos() != 3) { Usuario.escribir("Usage: run udp IP PORT TEXT\n"); return 2; }
        int dirección = dirección(Usuario.argumentos(0)), valorPuerto = valorDígito(Usuario.argumentos(1));
        String valorContenidoValor = Usuario.argumentos(2);
        if (dirección == 0 || valorPuerto < 1 || valorContenidoValor.length() > 1024) { Usuario.escribir("Bad destination\n"); return 2; }
        int valorManejador = Usuario.abrirRed(0);
        if (valorManejador < 0) { Usuario.escribir("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] Datos = new int[1024];
        for (int número = 0; número < valorContenidoValor.length(); número++) Datos[número] = valorContenidoValor.charAt(número);
        if (Usuario.enviarDatos(valorManejador, dirección, valorPuerto, Datos, valorContenidoValor.length()) < 0) {
            Usuario.escribir("UDP SEND FAILED\n"); Usuario.cerrarRed(valorManejador); return 4;
        }
        Usuario.escribir("UDP SENT\n");
        int longitudRecibido = Usuario.recibirDatos(valorManejador, Datos, 1500);
        boolean textoIgual = longitudRecibido == valorContenidoValor.length() && Usuario.direcciónEnviado(valorManejador) == dirección && Usuario.puertoEnviado(valorManejador) == valorPuerto;
        if (textoIgual) for (int número = 0; número < longitudRecibido; número++) if (Datos[número] != valorContenidoValor.charAt(número)) textoIgual = false;
        Usuario.cerrarRed(valorManejador);
        if (longitudRecibido < 0) { Usuario.escribir("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        Usuario.escribir(textoIgual ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return textoIgual ? 0 : 6;
    }
}
