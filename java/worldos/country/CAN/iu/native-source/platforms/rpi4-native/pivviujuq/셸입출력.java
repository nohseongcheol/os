// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, 입력파일 = -1, 출력파일 = -1;
    static boolean 파이프입력, 파이프출력;
    static int itigaqtuq_atuutilik;
    static boolean Pijunnaqtilli_ilaliujjarvilik = true;
    public static int 대화가능() { return Pijunnaqtilli_ilaliujjarvilik && 입력파일 < 3 && 출력파일 < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int 출력(int saana_atuutilik, int atuutilik) {
        if (saana_atuutilik != 1) return 0;
        if (출력파일 >= 3) { int 처리값 = 기억파일.titiraq(출력파일, atuutilik); if (처리값 < 0) itigaqtuq_atuutilik = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) itigaqtuq_atuutilik = -28;
        else 출력자료[출력길이++] = atuutilik;
        return 1;
    }
    public static int 입력() {
        if (입력파일 >= 3) { int 처리값 = 기억파일.읽기(입력파일); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 sivummualli_atuutilik
    }
    static void 시작(boolean titikutaat_akunningit_sullulik, boolean 뒤파이프) {
        파이프입력 = titikutaat_akunningit_sullulik; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; 입력파일 = -1; 출력파일 = -1; itigaqtuq_atuutilik = 0;
    }
    static void 끝() {
        보드.입출력전환(0);
        if (입력파일 >= 3) 기억파일.matuli(입력파일);
        if (출력파일 >= 3) 기억파일.matuli(출력파일);
        if (파이프출력) { 입력길이 = 출력길이; for (int piliqqittaajuq_nalunaiqsimavik = 0; piliqqittaajuq_nalunaiqsimavik < 출력길이; piliqqittaajuq_nalunaiqsimavik++) 입력자료[piliqqittaajuq_nalunaiqsimavik] = 출력자료[piliqqittaajuq_nalunaiqsimavik]; }
        입력파일 = -1; 출력파일 = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
