// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, Faele_ya_Tiro_e_e_Dirilweng = -1;
    static boolean 파이프입력, 파이프출력;
    static int palelo_Boleng;
    static boolean letla_Tirisano = true;
    public static int 대화가능() { return letla_Tirisano && 입력파일 < 3 && Faele_ya_Tiro_e_e_Dirilweng < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int mosele_Boleng, int Boleng) {
        if (mosele_Boleng != 1) return 0;
        if (Faele_ya_Tiro_e_e_Dirilweng >= 3) { int 처리값 = memori_Difaele.kwala(Faele_ya_Tiro_e_e_Dirilweng, Boleng); if (처리값 < 0) palelo_Boleng = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) palelo_Boleng = -28;
        else 출력자료[출력길이++] = Boleng;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = memori_Difaele.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 fetisa_Boleng_24592b8a
    }
    static void dirisa(boolean kgaoganyomela_baratlhamalalo, boolean 뒤파이프) {
        파이프입력 = kgaoganyomela_baratlhamalalo; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; Faele_ya_Tiro_e_e_Dirilweng = -1; palelo_Boleng = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) memori_Difaele.tswala(입력파일);
        if (Faele_ya_Tiro_e_e_Dirilweng >= 3) memori_Difaele.tswala(Faele_ya_Tiro_e_e_Dirilweng);
        if (파이프출력) { 입력길이 = 출력길이; for (int lupu_tshupane = 0; lupu_tshupane < 출력길이; lupu_tshupane++) 입력자료[lupu_tshupane] = 출력자료[lupu_tshupane]; }
        입력파일 = -1; Faele_ya_Tiro_e_e_Dirilweng = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
