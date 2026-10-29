// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, çykyş_faýly_9ceb7bd4 = -1;
    static boolean 파이프입력, 파이프출력;
    static int näsazlyk_baha;
    static boolean Rugsat_ber_interaktiw = true;
    public static int 대화가능() { return Rugsat_ber_interaktiw && 입력파일 < 3 && çykyş_faýly_9ceb7bd4 < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int kanal_baha, int baha) {
        if (kanal_baha != 1) return 0;
        if (çykyş_faýly_9ceb7bd4 >= 3) { int 처리값 = ýat_Faýllar.Ýaz(çykyş_faýly_9ceb7bd4, baha); if (처리값 < 0) näsazlyk_baha = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) näsazlyk_baha = -28;
        else 출력자료[출력길이++] = baha;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = ýat_Faýllar.Oka(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 ugrukdyr_baha
    }
    static void Bitir(boolean setirara_nyşany, boolean 뒤파이프) {
        파이프입력 = setirara_nyşany; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; çykyş_faýly_9ceb7bd4 = -1; näsazlyk_baha = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) ýat_Faýllar.Ýap(입력파일);
        if (çykyş_faýly_9ceb7bd4 >= 3) ýat_Faýllar.Ýap(çykyş_faýly_9ceb7bd4);
        if (파이프출력) { 입력길이 = 출력길이; for (int sikl_indeks = 0; sikl_indeks < 출력길이; sikl_indeks++) 입력자료[sikl_indeks] = 출력자료[sikl_indeks]; }
        입력파일 = -1; çykyş_faýly_9ceb7bd4 = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
