// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, comhad_aschuir = -1;
    static boolean 파이프입력, 파이프출력;
    static int teip_VALUE;
    static boolean Ceadaigh_idirghníomhach = true;
    public static int teicneolaíocht_faisnéise_idirghníomhach() { return Ceadaigh_idirghníomhach && 입력파일 < 3 && comhad_aschuir < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int Aschur(int cainéal_VALUE, int VALUE) {
        if (cainéal_VALUE != 1) return 0;
        if (comhad_aschuir >= 3) { int 처리값 = Cuimhne_Comhaid.Scríobh(comhad_aschuir, VALUE); if (처리값 < 0) teip_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) teip_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Cuimhne_Comhaid.Léigh(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Ar_aghaidh_VALUE
    }
    static void Rith_2(boolean spásáil_línte_píopa, boolean 뒤파이프) {
        파이프입력 = spásáil_línte_píopa; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; comhad_aschuir = -1; teip_VALUE = 0;
    }
    static void 끝() {
        clár.입출력전환(0);
        if (입력파일 >= 3) Cuimhne_Comhaid.Dún(입력파일);
        if (comhad_aschuir >= 3) Cuimhne_Comhaid.Dún(comhad_aschuir);
        if (파이프출력) { 입력길이 = 출력길이; for (int lúb_INDEX = 0; lúb_INDEX < 출력길이; lúb_INDEX++) 입력자료[lúb_INDEX] = 출력자료[lúb_INDEX]; }
        입력파일 = -1; comhad_aschuir = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
