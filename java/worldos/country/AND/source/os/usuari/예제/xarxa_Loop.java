// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Mida/홀수 durada_VALOR 데이터그램으로 real_dades RTL8139 rebre_VALOR Loop_VALOR 순환을 시험한다. */
public final class xarxa_Loop {
    public static int Executa_2() {
        if (usuari.인수개수() != 1) { usuari.Escriptura("Usage: run stress PORT\n"); return 2; }
        String SMS = usuari.인수(0);
        int port_VALOR = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            if (SMS.charAt(INDEX) < '0' || SMS.charAt(INDEX) > '9' || port_VALOR > 6553) return 2;
            port_VALOR = port_VALOR * 10 + SMS.charAt(INDEX) - '0';
        }
        if (port_VALOR < 1 || port_VALOR > 65535) return 2;
        int control_VALOR_f011887b = usuari.crear_xarxa(0);
        if (control_VALOR_f011887b < 0) return 3;
        int[] dades = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int durada_VALOR = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) dades[INDEX] = (INDEX + 회차) & 255;
            if (usuari.enviar_dades(control_VALOR_f011887b, 0x0a000202, port_VALOR, dades, durada_VALOR) != durada_VALOR) return 4;
            if (usuari.rebre_dades(control_VALOR_f011887b, dades, 300) != durada_VALOR) return 5;
            for (int INDEX = 0; INDEX < durada_VALOR; INDEX++) if (dades[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        usuari.Tanca_xarxa(control_VALOR_f011887b);
        usuari.Escriptura("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
