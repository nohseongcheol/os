// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, vhodna_datoteka = -1, izhodna_datoteka = -1;
    static boolean 파이프입력, 파이프출력;
    static int napaka_VALUE;
    static boolean Dovoli_interaktiven = true;
    public static int informacijska_tehnologija_interaktiven() { return Dovoli_interaktiven && vhodna_datoteka < 3 && izhodna_datoteka < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int Izpis(int Kanal_VALUE, int VALUE) {
        if (Kanal_VALUE != 1) return 0;
        if (izhodna_datoteka >= 3) { int 처리값 = pomnilnik_Datoteke.Pisanje(izhodna_datoteka, VALUE); if (처리값 < 0) napaka_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) napaka_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (vhodna_datoteka >= 3) { int 처리값 = pomnilnik_Datoteke.Branje(vhodna_datoteka); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Naprej_VALUE
    }
    static void Zaženi(boolean razmik_vrstic_navpičnica, boolean 뒤파이프) {
        파이프입력 = razmik_vrstic_navpičnica; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; vhodna_datoteka = -1; izhodna_datoteka = -1; napaka_VALUE = 0;
    }
    static void 끝() {
        Tabla.입출력전환(0);
        if (vhodna_datoteka >= 3) pomnilnik_Datoteke.Zapri(vhodna_datoteka);
        if (izhodna_datoteka >= 3) pomnilnik_Datoteke.Zapri(izhodna_datoteka);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        vhodna_datoteka = -1; izhodna_datoteka = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
