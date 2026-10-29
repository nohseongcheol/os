// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, chiqish_fayli = -1;
    static boolean 파이프입력, 파이프출력;
    static int to_xtab_qolish_VALUE;
    static boolean Ruxsatnoma_o_zaro_faol = true;
    public static int 대화가능() { return Ruxsatnoma_o_zaro_faol && 입력파일 < 3 && chiqish_fayli < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int kanal_VALUE, int VALUE) {
        if (kanal_VALUE != 1) return 0;
        if (chiqish_fayli >= 3) { int 처리값 = Xotira_Fayllar.Yozish(chiqish_fayli, VALUE); if (처리값 < 0) to_xtab_qolish_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) to_xtab_qolish_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = Xotira_Fayllar.Oʻqish(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Oldinga_VALUE
    }
    static void Bajarish(boolean yetakchi_belgisi, boolean 뒤파이프) {
        파이프입력 = yetakchi_belgisi; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; chiqish_fayli = -1; to_xtab_qolish_VALUE = 0;
    }
    static void 끝() {
        yozuv_taxtasi.입출력전환(0);
        if (입력파일 >= 3) Xotira_Fayllar.Yopish(입력파일);
        if (chiqish_fayli >= 3) Xotira_Fayllar.Yopish(chiqish_fayli);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        입력파일 = -1; chiqish_fayli = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
