// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] inndata_data = new int[16384], produksjon_data = new int[16384];
    static int inndata_lengde, inndata_plassere, produksjon_lengde, inndatafil = -1, utdatafil = -1;
    static boolean loddrett_strek_inndata, loddrett_strek_produksjon;
    static int feil_VERDI;
    static boolean Tillat_interaktiv = true;
    public static int informasjonssystemer_interaktiv() { return Tillat_interaktiv && inndatafil < 3 && utdatafil < 3 && !loddrett_strek_inndata && !loddrett_strek_produksjon ? 1 : 0; }
    public static int Utgang(int Kanal_VERDI, int VERDI) {
        if (Kanal_VERDI != 1) return 0;
        if (utdatafil >= 3) { int 처리값 = Minne_Filer.Skriv(utdatafil, VERDI); if (처리값 < 0) feil_VERDI = 처리값; return 1; }
        if (!loddrett_strek_produksjon) return 0;
        if (produksjon_lengde == produksjon_data.length) feil_VERDI = -28;
        else produksjon_data[produksjon_lengde++] = VERDI;
        return 1;
    }
    public static int inndata_VERDI() {
        if (inndatafil >= 3) { int 처리값 = Minne_Filer.Les(inndatafil); return 처리값 == 256 ? -2 : 처리값; }
        if (loddrett_strek_inndata) return inndata_plassere < inndata_lengde ? inndata_data[inndata_plassere++] : -2;
        return -3; // UART로 Frem_VERDI
    }
    static void Kjør_2(boolean linjeavstand_loddrett_strek, boolean 뒤파이프) {
        loddrett_strek_inndata = linjeavstand_loddrett_strek; loddrett_strek_produksjon = 뒤파이프;
        inndata_plassere = 0; produksjon_lengde = 0; inndatafil = -1; utdatafil = -1; feil_VERDI = 0;
    }
    static void 끝() {
        Tavle.입출력전환(0);
        if (inndatafil >= 3) Minne_Filer.Lukk(inndatafil);
        if (utdatafil >= 3) Minne_Filer.Lukk(utdatafil);
        if (loddrett_strek_produksjon) { inndata_lengde = produksjon_lengde; for (int Loop_INDEKS = 0; Loop_INDEKS < produksjon_lengde; Loop_INDEKS++) inndata_data[Loop_INDEKS] = produksjon_data[Loop_INDEKS]; }
        inndatafil = -1; utdatafil = -1; loddrett_strek_inndata = false; loddrett_strek_produksjon = false;
    }
}
