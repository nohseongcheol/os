// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, skedari_përfundimtar = -1;
    static boolean 파이프입력, 파이프출력;
    static int dështim_VALUE;
    static boolean Lejoj_ndërvepruese = true;
    public static int teknologjia_e_informacionit_ndërvepruese() { return Lejoj_ndërvepruese && 입력파일 < 3 && skedari_përfundimtar < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int kanal_VALUE, int VALUE) {
        if (kanal_VALUE != 1) return 0;
        if (skedari_përfundimtar >= 3) { int 처리값 = Memorie_Skedarët.Shkrimi(skedari_përfundimtar, VALUE); if (처리값 < 0) dështim_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) dështim_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Memorie_Skedarët.Leximi(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 paso_VALUE
    }
    static void Ekzekuto(boolean hapësira_midis_rreshtave_vijë_vertikale, boolean 뒤파이프) {
        파이프입력 = hapësira_midis_rreshtave_vijë_vertikale; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; skedari_përfundimtar = -1; dështim_VALUE = 0;
    }
    static void 끝() {
        panel.입출력전환(0);
        if (입력파일 >= 3) Memorie_Skedarët.Mbyll(입력파일);
        if (skedari_përfundimtar >= 3) Memorie_Skedarët.Mbyll(skedari_përfundimtar);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        입력파일 = -1; skedari_përfundimtar = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
