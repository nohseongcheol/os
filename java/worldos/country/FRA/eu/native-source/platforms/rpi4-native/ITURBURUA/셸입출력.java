// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, sarrerako_fitxategi = -1, 출력파일 = -1;
    static boolean 파이프입력, 파이프출력;
    static int hutsegite_balio;
    static boolean Onartu_interaktibo = true;
    public static int informatika_interaktibo() { return Onartu_interaktibo && sarrerako_fitxategi < 3 && 출력파일 < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int Irteera(int kanal_balio, int balio) {
        if (kanal_balio != 1) return 0;
        if (출력파일 >= 3) { int 처리값 = Memoria_Fitxategiak.Idatzi(출력파일, balio); if (처리값 < 0) hutsegite_balio = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) hutsegite_balio = -28;
        else 출력자료[출력길이++] = balio;
        return 1;
    }
    public static int 입력() {
        if (sarrerako_fitxategi >= 3) { int 처리값 = Memoria_Fitxategiak.Irakurri(sarrerako_fitxategi); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Aurrera_balio
    }
    static void Exekutatu_2(boolean lerroarte_barra_bertikal, boolean 뒤파이프) {
        파이프입력 = lerroarte_barra_bertikal; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; sarrerako_fitxategi = -1; 출력파일 = -1; hutsegite_balio = 0;
    }
    static void 끝() {
        arbel.입출력전환(0);
        if (sarrerako_fitxategi >= 3) Memoria_Fitxategiak.Itxi(sarrerako_fitxategi);
        if (출력파일 >= 3) Memoria_Fitxategiak.Itxi(출력파일);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDIZE = 0; Loop_INDIZE < 출력길이; Loop_INDIZE++) 입력자료[Loop_INDIZE] = 출력자료[Loop_INDIZE]; }
        sarrerako_fitxategi = -1; 출력파일 = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
