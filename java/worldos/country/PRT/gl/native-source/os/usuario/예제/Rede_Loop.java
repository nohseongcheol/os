// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Tamaño/홀수 duración_VALOR 데이터그램으로 real_datos RTL8139 수신 Loop_VALOR 순환을 시험한다. */
public final class Rede_Loop {
    public static int Executar_2() {
        if (usuario.인수개수() != 1) { usuario.Escritura("Usage: run stress PORT\n"); return 2; }
        String Texto = usuario.Argumentos(0);
        int porto_VALOR = 0;
        for (int ÍNDICE = 0; ÍNDICE < Texto.length(); ÍNDICE++) {
            if (Texto.charAt(ÍNDICE) < '0' || Texto.charAt(ÍNDICE) > '9' || porto_VALOR > 6553) return 2;
            porto_VALOR = porto_VALOR * 10 + Texto.charAt(ÍNDICE) - '0';
        }
        if (porto_VALOR < 1 || porto_VALOR > 65535) return 2;
        int agarradoira_VALOR = usuario.abrir_Rede(0);
        if (agarradoira_VALOR < 0) return 3;
        int[] datos = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int duración_VALOR = 1024 - (회차 & 1);
            for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) datos[ÍNDICE] = (ÍNDICE + 회차) & 255;
            if (usuario.enviar_datos(agarradoira_VALOR, 0x0a000202, porto_VALOR, datos, duración_VALOR) != duración_VALOR) return 4;
            if (usuario.자료받기(agarradoira_VALOR, datos, 300) != duración_VALOR) return 5;
            for (int ÍNDICE = 0; ÍNDICE < duración_VALOR; ÍNDICE++) if (datos[ÍNDICE] != ((ÍNDICE + 회차) & 255)) return 6;
        }
        usuario.peche_Rede(agarradoira_VALOR);
        usuario.Escritura("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
