// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, faili_towe = -1;
    static boolean 파이프입력, 파이프출력;
    static int kushindwa_thamani;
    static boolean Ruhusu_ingiliani = true;
    public static int teknolojia_ya_maelezo_ingiliani() { return Ruhusu_ingiliani && 입력파일 < 3 && faili_towe < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int mkondo_thamani, int thamani) {
        if (mkondo_thamani != 1) return 0;
        if (faili_towe >= 3) { int 처리값 = kumbukumbu_Faili.andika(faili_towe, thamani); if (처리값 < 0) kushindwa_thamani = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) kushindwa_thamani = -28;
        else 출력자료[출력길이++] = thamani;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = kumbukumbu_Faili.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 tuma_mbele_thamani
    }
    static void endesha(boolean inayoongoza_bomba, boolean 뒤파이프) {
        파이프입력 = inayoongoza_bomba; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; faili_towe = -1; kushindwa_thamani = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) kumbukumbu_Faili.funga(입력파일);
        if (faili_towe >= 3) kumbukumbu_Faili.funga(faili_towe);
        if (파이프출력) { 입력길이 = 출력길이; for (int kitanzi_kielezo = 0; kitanzi_kielezo < 출력길이; kitanzi_kielezo++) 입력자료[kitanzi_kielezo] = 출력자료[kitanzi_kielezo]; }
        입력파일 = -1; faili_towe = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
