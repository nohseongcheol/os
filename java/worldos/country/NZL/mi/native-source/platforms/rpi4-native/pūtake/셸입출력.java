// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, kōnae_huaputa = -1;
    static boolean 파이프입력, 파이프출력;
    static int rahunga_uara;
    static boolean Tuku_pāhekoheko = true;
    public static int 대화가능() { return Tuku_pāhekoheko && 입력파일 < 3 && kōnae_huaputa < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int hongere_uara, int uara) {
        if (hongere_uara != 1) return 0;
        if (kōnae_huaputa >= 3) { int 처리값 = Pūmahara_Ngā_Kōnae.Tuhia(kōnae_huaputa, uara); if (처리값 < 0) rahunga_uara = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) rahunga_uara = -28;
        else 출력자료[출력길이++] = uara;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Pūmahara_Ngā_Kōnae.Pānuitia(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Whakamua_uara
    }
    static void whakahaere(boolean mokowā_raina_pae_poutū, boolean 뒤파이프) {
        파이프입력 = mokowā_raina_pae_poutū; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; kōnae_huaputa = -1; rahunga_uara = 0;
    }
    static void 끝() {
        papa.입출력전환(0);
        if (입력파일 >= 3) Pūmahara_Ngā_Kōnae.Kati(입력파일);
        if (kōnae_huaputa >= 3) Pūmahara_Ngā_Kōnae.Kati(kōnae_huaputa);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        입력파일 = -1; kōnae_huaputa = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
