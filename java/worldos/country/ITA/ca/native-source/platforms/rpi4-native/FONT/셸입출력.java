// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, fitxer_d_entrada = -1, 출력파일 = -1;
    static boolean 파이프입력, 파이프출력;
    static int error_VALOR;
    static boolean Permet_interactiu = true;
    public static int tecnologies_de_la_informació_interactiu() { return Permet_interactiu && fitxer_d_entrada < 3 && 출력파일 < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int Sortida(int Canal_VALOR, int VALOR) {
        if (Canal_VALOR != 1) return 0;
        if (출력파일 >= 3) { int 처리값 = Memòria_Fitxers.Escriptura(출력파일, VALOR); if (처리값 < 0) error_VALOR = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) error_VALOR = -28;
        else 출력자료[출력길이++] = VALOR;
        return 1;
    }
    public static int 입력() {
        if (fitxer_d_entrada >= 3) { int 처리값 = Memòria_Fitxers.Lectura(fitxer_d_entrada); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 desviar_VALOR
    }
    static void Executa_2(boolean 앞파이프, boolean 뒤파이프) {
        파이프입력 = 앞파이프; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; fitxer_d_entrada = -1; 출력파일 = -1; error_VALOR = 0;
    }
    static void 끝() {
        Tauler.입출력전환(0);
        if (fitxer_d_entrada >= 3) Memòria_Fitxers.Tanca(fitxer_d_entrada);
        if (출력파일 >= 3) Memòria_Fitxers.Tanca(출력파일);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        fitxer_d_entrada = -1; 출력파일 = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
