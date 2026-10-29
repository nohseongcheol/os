// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, faele_ya_tšweletšo = -1;
    static boolean 파이프입력, 파이프출력;
    static int go_palelwa_boleng;
    static boolean Dumelela_ya_kgokagano = true;
    public static int 대화가능() { return Dumelela_ya_kgokagano && 입력파일 < 3 && faele_ya_tšweletšo < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int mokero_boleng, int boleng) {
        if (mokero_boleng != 1) return 0;
        if (faele_ya_tšweletšo >= 3) { int 처리값 = memori_Difaele.Ngwala(faele_ya_tšweletšo, boleng); if (처리값 < 0) go_palelwa_boleng = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) go_palelwa_boleng = -28;
        else 출력자료[출력길이++] = boleng;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = memori_Difaele.Bala(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 romela_pele_boleng
    }
    static void Diriša(boolean sekgoba_sa_methalo_phaepe, boolean 뒤파이프) {
        파이프입력 = sekgoba_sa_methalo_phaepe; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; faele_ya_tšweletšo = -1; go_palelwa_boleng = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) memori_Difaele.Tswalela(입력파일);
        if (faele_ya_tšweletšo >= 3) memori_Difaele.Tswalela(faele_ya_tšweletšo);
        if (파이프출력) { 입력길이 = 출력길이; for (int ditaelopoeletšwa_lokela = 0; ditaelopoeletšwa_lokela < 출력길이; ditaelopoeletšwa_lokela++) 입력자료[ditaelopoeletšwa_lokela] = 출력자료[ditaelopoeletšwa_lokela]; }
        입력파일 = -1; faele_ya_tšweletšo = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
