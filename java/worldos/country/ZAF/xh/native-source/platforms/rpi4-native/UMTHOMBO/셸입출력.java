// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, ifayile_yemveliso = -1;
    static boolean 파이프입력, 파이프출력;
    static int ukungaphumeleli_ixabiso;
    static boolean vumela_esebenzisana_nomsebenzi = true;
    public static int 대화가능() { return vumela_esebenzisana_nomsebenzi && 입력파일 < 3 && ifayile_yemveliso < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int ijelo_ixabiso, int ixabiso) {
        if (ijelo_ixabiso != 1) return 0;
        if (ifayile_yemveliso >= 3) { int 처리값 = imemori_Iifayile.Bhala(ifayile_yemveliso, ixabiso); if (처리값 < 0) ukungaphumeleli_ixabiso = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) ukungaphumeleli_ixabiso = -28;
        else 출력자료[출력길이++] = ixabiso;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = imemori_Iifayile.Funda(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 dlulisa_ixabiso
    }
    static void Phumeza(boolean isikhokeli_ibha, boolean 뒤파이프) {
        파이프입력 = isikhokeli_ibha; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; ifayile_yemveliso = -1; ukungaphumeleli_ixabiso = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) imemori_Iifayile.Vala(입력파일);
        if (ifayile_yemveliso >= 3) imemori_Iifayile.Vala(ifayile_yemveliso);
        if (파이프출력) { 입력길이 = 출력길이; for (int iluphu_indeksa = 0; iluphu_indeksa < 출력길이; iluphu_indeksa++) 입력자료[iluphu_indeksa] = 출력자료[iluphu_indeksa]; }
        입력파일 = -1; ifayile_yemveliso = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
