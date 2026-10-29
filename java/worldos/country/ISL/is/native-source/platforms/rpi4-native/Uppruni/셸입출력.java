// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], úttak_gögn = new int[16384];
    static int 입력길이, 입력위치, úttak_lengd, 입력파일 = -1, úttaksskrá = -1;
    static boolean 파이프입력, lóðrétt_strik_úttak;
    static int bilun_VALUE;
    static boolean leyfa_gagnvirkur = true;
    public static int upplýsingatækni_gagnvirkur() { return leyfa_gagnvirkur && 입력파일 < 3 && úttaksskrá < 3 && !파이프입력 && !lóðrétt_strik_úttak ? 1 : 0; }
    public static int úttak(int rás_VALUE, int VALUE) {
        if (rás_VALUE != 1) return 0;
        if (úttaksskrá >= 3) { int 처리값 = Minni_Skrár.Skrift(úttaksskrá, VALUE); if (처리값 < 0) bilun_VALUE = 처리값; return 1; }
        if (!lóðrétt_strik_úttak) return 0;
        if (úttak_lengd == úttak_gögn.length) bilun_VALUE = -28;
        else úttak_gögn[úttak_lengd++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Minni_Skrár.Lestur(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Áfram_VALUE
    }
    static void Keyra_2(boolean línubil_lóðrétt_strik, boolean 뒤파이프) {
        파이프입력 = línubil_lóðrétt_strik; lóðrétt_strik_úttak = 뒤파이프;
        입력위치 = 0; úttak_lengd = 0; 입력파일 = -1; úttaksskrá = -1; bilun_VALUE = 0;
    }
    static void 끝() {
        bretti.입출력전환(0);
        if (입력파일 >= 3) Minni_Skrár.Loka(입력파일);
        if (úttaksskrá >= 3) Minni_Skrár.Loka(úttaksskrá);
        if (lóðrétt_strik_úttak) { 입력길이 = úttak_lengd; for (int Loop_INDEX = 0; Loop_INDEX < úttak_lengd; Loop_INDEX++) 입력자료[Loop_INDEX] = úttak_gögn[Loop_INDEX]; }
        입력파일 = -1; úttaksskrá = -1; 파이프입력 = false; lóðrétt_strik_úttak = false;
    }
}
