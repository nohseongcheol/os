// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int dígit_VALOR(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int RESULTAT = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int VALOR = SMS.charAt(INDEX) - '0';
            if (VALOR < 0 || VALOR > 9 || RESULTAT > 6553) return -1;
            RESULTAT = RESULTAT * 10 + VALOR;
            if (RESULTAT > 65535) return -1;
        }
        return RESULTAT;
    }
    static int Adreça(String SMS) {
        if (SMS == null) return 0;
        int VALOR = 0, RESULTAT = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= SMS.length(); INDEX++) {
            int 문자 = INDEX == SMS.length() ? '.' : SMS.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                RESULTAT = (RESULTAT << 8) | VALOR; 부분++; VALOR = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALOR = VALOR * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALOR > 255) return 0;
            }
        }
        return 부분 == 4 ? RESULTAT : 0;
    }
    public static int Executa_2() {
        if (usuari.인수개수() != 3) { usuari.Escriptura("Usage: run udp IP PORT TEXT\n"); return 2; }
        int Adreça = Adreça(usuari.인수(0)), port_VALOR = dígit_VALOR(usuari.인수(1));
        String contingut_VALOR = usuari.인수(2);
        if (Adreça == 0 || port_VALOR < 1 || contingut_VALOR.length() > 1024) { usuari.Escriptura("Bad destination\n"); return 2; }
        int control_VALOR_f011887b = usuari.crear_xarxa(0);
        if (control_VALOR_f011887b < 0) { usuari.Escriptura("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] dades = new int[1024];
        for (int INDEX = 0; INDEX < contingut_VALOR.length(); INDEX++) dades[INDEX] = contingut_VALOR.charAt(INDEX);
        if (usuari.enviar_dades(control_VALOR_f011887b, Adreça, port_VALOR, dades, contingut_VALOR.length()) < 0) {
            usuari.Escriptura("UDP SEND FAILED\n"); usuari.Tanca_xarxa(control_VALOR_f011887b); return 4;
        }
        usuari.Escriptura("UDP SENT\n");
        int CANTIDAD_RECIBIDA_durada = usuari.rebre_dades(control_VALOR_f011887b, dades, 1500);
        boolean 같음 = CANTIDAD_RECIBIDA_durada == contingut_VALOR.length() && usuari.보낸주소(control_VALOR_f011887b) == Adreça && usuari.보낸창구(control_VALOR_f011887b) == port_VALOR;
        if (같음) for (int INDEX = 0; INDEX < CANTIDAD_RECIBIDA_durada; INDEX++) if (dades[INDEX] != contingut_VALOR.charAt(INDEX)) 같음 = false;
        usuari.Tanca_xarxa(control_VALOR_f011887b);
        if (CANTIDAD_RECIBIDA_durada < 0) { usuari.Escriptura("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        usuari.Escriptura(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
