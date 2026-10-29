// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, 출력파일 = -1;
    static boolean 파이프입력, 파이프출력;
    static int ella_njaru;
    static boolean Wellit_jokkondirtoo = true;
    public static int 대화가능() { return Wellit_jokkondirtoo && 입력파일 < 3 && 출력파일 < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int kanaal_njaru, int njaru) {
        if (kanaal_njaru != 1) return 0;
        if (출력파일 >= 3) { int 처리값 = 기억파일.winndude(출력파일, njaru); if (처리값 < 0) ella_njaru = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) ella_njaru = -28;
        else 출력자료[출력길이++] = njaru;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = 기억파일.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 yawtinde_njaru
    }
    static void huutoraade(boolean 앞파이프, boolean 뒤파이프) {
        파이프입력 = 앞파이프; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; 출력파일 = -1; ella_njaru = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) 기억파일.uddude(입력파일);
        if (출력파일 >= 3) 기억파일.uddude(출력파일);
        if (파이프출력) { 입력길이 = 출력길이; for (int kowal_joopirdu = 0; kowal_joopirdu < 출력길이; kowal_joopirdu++) 입력자료[kowal_joopirdu] = 출력자료[kowal_joopirdu]; }
        입력파일 = -1; 출력파일 = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
