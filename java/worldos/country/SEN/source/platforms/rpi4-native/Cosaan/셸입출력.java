// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, takkub_génn = -1;
    static boolean 파이프입력, 파이프출력;
    static int foo_xëyma;
    static boolean Maye_duglante = true;
    public static int 대화가능() { return Maye_duglante && 입력파일 < 3 && takkub_génn < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int Yoon_xëyma, int xëyma) {
        if (Yoon_xëyma != 1) return 0;
        if (takkub_génn >= 3) { int 처리값 = fatlekookaay_Fisiye_yi.biir(takkub_génn, xëyma); if (처리값 < 0) foo_xëyma = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) foo_xëyma = -28;
        else 출력자료[출력길이++] = xëyma;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = fatlekookaay_Fisiye_yi.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 jëmal_kanam_xëyma
    }
    static void daw(boolean rëddu_xàjji_yat_wu_taxaw, boolean 뒤파이프) {
        파이프입력 = rëddu_xàjji_yat_wu_taxaw; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; takkub_génn = -1; foo_xëyma = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) fatlekookaay_Fisiye_yi.Tej(입력파일);
        if (takkub_génn >= 3) fatlekookaay_Fisiye_yi.Tej(takkub_génn);
        if (파이프출력) { 입력길이 = 출력길이; for (int wërngël_àlluwa_tur = 0; wërngël_àlluwa_tur < 출력길이; wërngël_àlluwa_tur++) 입력자료[wërngël_àlluwa_tur] = 출력자료[wërngël_àlluwa_tur]; }
        입력파일 = -1; takkub_génn = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
