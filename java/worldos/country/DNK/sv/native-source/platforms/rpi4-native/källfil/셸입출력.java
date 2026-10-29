// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] indata_data = new int[16384], utleverans_data = new int[16384];
    static int indata_längd, indata_placera, utleverans_längd, indatafil = -1, utdatafil = -1;
    static boolean pipa_indata, pipa_utleverans;
    static int fel_värde;
    static boolean Tillåt_interaktiv = true;
    public static int informationsteknik_interaktiv() { return Tillåt_interaktiv && indatafil < 3 && utdatafil < 3 && !pipa_indata && !pipa_utleverans ? 1 : 0; }
    public static int utmatningsposition(int Kanal_värde, int värde) {
        if (Kanal_värde != 1) return 0;
        if (utdatafil >= 3) { int 처리값 = Minne_Filer.Skriv(utdatafil, värde); if (처리값 < 0) fel_värde = 처리값; return 1; }
        if (!pipa_utleverans) return 0;
        if (utleverans_längd == utleverans_data.length) fel_värde = -28;
        else utleverans_data[utleverans_längd++] = värde;
        return 1;
    }
    public static int indata_värde() {
        if (indatafil >= 3) { int 처리값 = Minne_Filer.Läs(indatafil); return 처리값 == 256 ? -2 : 처리값; }
        if (pipa_indata) return indata_placera < indata_längd ? indata_data[indata_placera++] : -2;
        return -3; // UART로 Framåt_värde
    }
    static void Kör(boolean avstånd_pipa, boolean 뒤파이프) {
        pipa_indata = avstånd_pipa; pipa_utleverans = 뒤파이프;
        indata_placera = 0; utleverans_längd = 0; indatafil = -1; utdatafil = -1; fel_värde = 0;
    }
    static void 끝() {
        Tavla.입출력전환(0);
        if (indatafil >= 3) Minne_Filer.Stäng(indatafil);
        if (utdatafil >= 3) Minne_Filer.Stäng(utdatafil);
        if (pipa_utleverans) { indata_längd = utleverans_längd; for (int Loop_INDEX = 0; Loop_INDEX < utleverans_längd; Loop_INDEX++) indata_data[Loop_INDEX] = utleverans_data[Loop_INDEX]; }
        indatafil = -1; utdatafil = -1; pipa_indata = false; pipa_utleverans = false;
    }
}
