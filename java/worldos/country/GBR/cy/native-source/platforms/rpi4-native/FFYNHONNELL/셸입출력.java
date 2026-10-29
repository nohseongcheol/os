// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, ffeil_allbwn = -1;
    static boolean 파이프입력, 파이프출력;
    static int methiant_VALUE;
    static boolean Caniatáu_rhyngweithiol = true;
    public static int technoleg_gwybodaeth_rhyngweithiol() { return Caniatáu_rhyngweithiol && 입력파일 < 3 && ffeil_allbwn < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int Allbwn(int sianel_VALUE, int VALUE) {
        if (sianel_VALUE != 1) return 0;
        if (ffeil_allbwn >= 3) { int 처리값 = Cof_Ffeil.Ysgrifennu(ffeil_allbwn, VALUE); if (처리값 < 0) methiant_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) methiant_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Cof_Ffeil.Darllen(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Ymlaen_VALUE
    }
    static void Gweithredu_2(boolean rhynglinellu_pibell, boolean 뒤파이프) {
        파이프입력 = rhynglinellu_pibell; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; ffeil_allbwn = -1; methiant_VALUE = 0;
    }
    static void 끝() {
        bwrdd.입출력전환(0);
        if (입력파일 >= 3) Cof_Ffeil.Cau(입력파일);
        if (ffeil_allbwn >= 3) Cof_Ffeil.Cau(ffeil_allbwn);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        입력파일 = -1; ffeil_allbwn = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
