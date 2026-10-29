// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, ifayela_yokukhipha = -1;
    static boolean 파이프입력, 파이프출력;
    static int ukwehluleka_inani;
    static boolean vumela_ingxoxo_nekhompiyutha = true;
    public static int 대화가능() { return vumela_ingxoxo_nekhompiyutha && 입력파일 < 3 && ifayela_yokukhipha < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int umgudu_inani, int inani) {
        if (umgudu_inani != 1) return 0;
        if (ifayela_yokukhipha >= 3) { int 처리값 = inkumbulo_Amafayela.Bhala(ifayela_yokukhipha, inani); if (처리값 < 0) ukwehluleka_inani = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) ukwehluleka_inani = -28;
        else 출력자료[출력길이++] = inani;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = inkumbulo_Amafayela.Funda(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 dlulisela_phambili_inani
    }
    static void Sebenzisa(boolean izikhala_iphayiphi, boolean 뒤파이프) {
        파이프입력 = izikhala_iphayiphi; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; ifayela_yokukhipha = -1; ukwehluleka_inani = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) inkumbulo_Amafayela.Vala(입력파일);
        if (ifayela_yokukhipha >= 3) inkumbulo_Amafayela.Vala(ifayela_yokukhipha);
        if (파이프출력) { 입력길이 = 출력길이; for (int iluphu_thola_inkomba = 0; iluphu_thola_inkomba < 출력길이; iluphu_thola_inkomba++) 입력자료[iluphu_thola_inkomba] = 출력자료[iluphu_thola_inkomba]; }
        입력파일 = -1; ifayela_yokukhipha = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
