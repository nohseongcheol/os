// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, dosiye_yasohotse = -1;
    static boolean 파이프입력, 파이프출력;
    static int kudakora_agaciro;
    static boolean Kwemerera_interfacebikorana = true;
    public static int 대화가능() { return Kwemerera_interfacebikorana && 입력파일 < 3 && dosiye_yasohotse < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int umurongo_agaciro, int agaciro) {
        if (umurongo_agaciro != 1) return 0;
        if (dosiye_yasohotse >= 3) { int 처리값 = ububiko_Dosiye.kwandika(dosiye_yasohotse, agaciro); if (처리값 < 0) kudakora_agaciro = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) kudakora_agaciro = -28;
        else 출력자료[출력길이++] = agaciro;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = ububiko_Dosiye.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 koherereza_agaciro
    }
    static void ihuriro(boolean itandukanyamurongo_akarongo_gahagaze, boolean 뒤파이프) {
        파이프입력 = itandukanyamurongo_akarongo_gahagaze; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; dosiye_yasohotse = -1; kudakora_agaciro = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) ububiko_Dosiye.Gufunga(입력파일);
        if (dosiye_yasohotse >= 3) ububiko_Dosiye.Gufunga(dosiye_yasohotse);
        if (파이프출력) { 입력길이 = 출력길이; for (int gukora_mu_matsinda_umugerekashakiro = 0; gukora_mu_matsinda_umugerekashakiro < 출력길이; gukora_mu_matsinda_umugerekashakiro++) 입력자료[gukora_mu_matsinda_umugerekashakiro] = 출력자료[gukora_mu_matsinda_umugerekashakiro]; }
        입력파일 = -1; dosiye_yasohotse = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
