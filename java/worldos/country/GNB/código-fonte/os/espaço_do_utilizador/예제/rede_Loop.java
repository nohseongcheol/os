// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Tamanho/홀수 duração_VALOR 데이터그램으로 real_dados RTL8139 receber_VALOR Loop_VALOR 순환을 시험한다. */
public final class rede_Loop {
    public static int iniciar() {
        if (espaço_do_utilizador.인수개수() != 1) { espaço_do_utilizador.Escrita("Usage: run stress PORT\n"); return 2; }
        String texto = espaço_do_utilizador.argumentos(0);
        int porta_VALOR = 0;
        for (int ÍNDICE = 0; ÍNDICE < texto.length(); ÍNDICE++) {
            if (texto.charAt(ÍNDICE) < '0' || texto.charAt(ÍNDICE) > '9' || porta_VALOR > 6553) return 2;
            porta_VALOR = porta_VALOR * 10 + texto.charAt(ÍNDICE) - '0';
        }
        if (porta_VALOR < 1 || porta_VALOR > 65535) return 2;
        int alça_VALOR = espaço_do_utilizador.abrir_rede(0);
        if (alça_VALOR < 0) return 3;
        int[] dados = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int duração_VALOR = 1024 - (회차 & 1);
            for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) dados[ÍNDICE] = (ÍNDICE + 회차) & 255;
            if (espaço_do_utilizador.enviar_dados(alça_VALOR, 0x0a000202, porta_VALOR, dados, duração_VALOR) != duração_VALOR) return 4;
            if (espaço_do_utilizador.receber_dados(alça_VALOR, dados, 300) != duração_VALOR) return 5;
            for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) if (dados[ÍNDICE] != ((ÍNDICE + 회차) & 255)) return 6;
        }
        espaço_do_utilizador.Close_rede(alça_VALOR);
        espaço_do_utilizador.Escrita("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
