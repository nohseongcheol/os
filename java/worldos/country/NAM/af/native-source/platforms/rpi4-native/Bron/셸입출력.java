// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, afvoerlêer = -1;
    static boolean 파이프입력, 파이프출력;
    static int faling_VALUE;
    static boolean toelaat_interaktief = true;
    public static int 대화가능() { return toelaat_interaktief && 입력파일 < 3 && afvoerlêer < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int Afvoer(int kanaal_VALUE, int VALUE) {
        if (kanaal_VALUE != 1) return 0;
        if (afvoerlêer >= 3) { int 처리값 = Geheue_Lêers.Skryf(afvoerlêer, VALUE); if (처리값 < 0) faling_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) faling_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Geheue_Lêers.Lees(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 aanstuur_VALUE_24592b8a
    }
    static void Loop(boolean reëlspasiëring_vertikale_strepie, boolean 뒤파이프) {
        파이프입력 = reëlspasiëring_vertikale_strepie; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; afvoerlêer = -1; faling_VALUE = 0;
    }
    static void 끝() {
        bord.입출력전환(0);
        if (입력파일 >= 3) Geheue_Lêers.Sluit(입력파일);
        if (afvoerlêer >= 3) Geheue_Lêers.Sluit(afvoerlêer);
        if (파이프출력) { 입력길이 = 출력길이; for (int lus_INDEX = 0; lus_INDEX < 출력길이; lus_INDEX++) 입력자료[lus_INDEX] = 출력자료[lus_INDEX]; }
        입력파일 = -1; afvoerlêer = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
