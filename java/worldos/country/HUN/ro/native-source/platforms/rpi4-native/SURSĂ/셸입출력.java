// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] 입력자료 = new int[16384], 출력자료 = new int[16384];
    static int 입력길이, 입력위치, 출력길이, fișier_de_intrare = -1, fișier_de_ieșire = -1;
    static boolean 파이프입력, 파이프출력;
    static int eroare_VALUE;
    static boolean 대화허용 = true;
    public static int 대화가능() { return 대화허용 && fișier_de_intrare < 3 && fișier_de_ieșire < 3 && !파이프입력 && !파이프출력 ? 1 : 0; }
    public static int Rezultat(int Canal_VALUE, int VALUE) {
        if (Canal_VALUE != 1) return 0;
        if (fișier_de_ieșire >= 3) { int 처리값 = Memorie_Fișiere.Scriere(fișier_de_ieșire, VALUE); if (처리값 < 0) eroare_VALUE = 처리값; return 1; }
        if (!파이프출력) return 0;
        if (출력길이 == 출력자료.length) eroare_VALUE = -28;
        else 출력자료[출력길이++] = VALUE;
        return 1;
    }
    public static int 입력() {
        if (fișier_de_intrare >= 3) { int 처리값 = Memorie_Fișiere.Citire(fișier_de_intrare); return 처리값 == 256 ? -2 : 처리값; }
        if (파이프입력) return 입력위치 < 입력길이 ? 입력자료[입력위치++] : -2;
        return -3; // UART로 Înainte_VALUE
    }
    static void Pornește(boolean spațiere_canal, boolean 뒤파이프) {
        파이프입력 = spațiere_canal; 파이프출력 = 뒤파이프;
        입력위치 = 0; 출력길이 = 0; fișier_de_intrare = -1; fișier_de_ieșire = -1; eroare_VALUE = 0;
    }
    static void 끝() {
        Avizier.입출력전환(0);
        if (fișier_de_intrare >= 3) Memorie_Fișiere.Închide(fișier_de_intrare);
        if (fișier_de_ieșire >= 3) Memorie_Fișiere.Închide(fișier_de_ieșire);
        if (파이프출력) { 입력길이 = 출력길이; for (int Loop_INDEX = 0; Loop_INDEX < 출력길이; Loop_INDEX++) 입력자료[Loop_INDEX] = 출력자료[Loop_INDEX]; }
        fișier_de_intrare = -1; fișier_de_ieșire = -1; 파이프입력 = false; 파이프출력 = false;
    }
}
