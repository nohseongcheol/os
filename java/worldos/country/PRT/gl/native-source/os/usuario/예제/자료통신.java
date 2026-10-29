// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int díxito_VALOR(String Texto) {
        if (Texto == null || Texto.length() == 0) return -1;
        int RESULTANTE = 0;
        for (int ÍNDICE = 0; ÍNDICE < Texto.length(); ÍNDICE++) {
            int VALOR = Texto.charAt(ÍNDICE) - '0';
            if (VALOR < 0 || VALOR > 9 || RESULTANTE > 6553) return -1;
            RESULTANTE = RESULTANTE * 10 + VALOR;
            if (RESULTANTE > 65535) return -1;
        }
        return RESULTANTE;
    }
    static int ENDEREZO(String Texto) {
        if (Texto == null) return 0;
        int VALOR = 0, RESULTANTE = 0, 부분 = 0, 자릿수 = 0;
        for (int ÍNDICE = 0; ÍNDICE <= Texto.length(); ÍNDICE++) {
            int 문자 = ÍNDICE == Texto.length() ? '.' : Texto.charAt(ÍNDICE);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                RESULTANTE = (RESULTANTE << 8) | VALOR; 부분++; VALOR = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALOR = VALOR * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALOR > 255) return 0;
            }
        }
        return 부분 == 4 ? RESULTANTE : 0;
    }
    public static int Executar_2() {
        if (usuario.인수개수() != 3) { usuario.Escritura("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ENDEREZO = ENDEREZO(usuario.Argumentos(0)), porto_VALOR = díxito_VALOR(usuario.Argumentos(1));
        String Contido_VALOR = usuario.Argumentos(2);
        if (ENDEREZO == 0 || porto_VALOR < 1 || Contido_VALOR.length() > 1024) { usuario.Escritura("Bad destination\n"); return 2; }
        int agarradoira_VALOR = usuario.abrir_Rede(0);
        if (agarradoira_VALOR < 0) { usuario.Escritura("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] datos = new int[1024];
        for (int ÍNDICE = 0; ÍNDICE < Contido_VALOR.length(); ÍNDICE++) datos[ÍNDICE] = Contido_VALOR.charAt(ÍNDICE);
        if (usuario.enviar_datos(agarradoira_VALOR, ENDEREZO, porto_VALOR, datos, Contido_VALOR.length()) < 0) {
            usuario.Escritura("UDP SEND FAILED\n"); usuario.peche_Rede(agarradoira_VALOR); return 4;
        }
        usuario.Escritura("UDP SENT\n");
        int RECIBIDO_duración = usuario.자료받기(agarradoira_VALOR, datos, 1500);
        boolean 같음 = RECIBIDO_duración == Contido_VALOR.length() && usuario.보낸주소(agarradoira_VALOR) == ENDEREZO && usuario.보낸창구(agarradoira_VALOR) == porto_VALOR;
        if (같음) for (int ÍNDICE = 0; ÍNDICE < RECIBIDO_duración; ÍNDICE++) if (datos[ÍNDICE] != Contido_VALOR.charAt(ÍNDICE)) 같음 = false;
        usuario.peche_Rede(agarradoira_VALOR);
        if (RECIBIDO_duración < 0) { usuario.Escritura("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        usuario.Escritura(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
