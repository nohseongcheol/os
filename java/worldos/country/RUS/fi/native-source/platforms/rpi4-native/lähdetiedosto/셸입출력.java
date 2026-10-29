// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] syöte_data = new int[16384], tulos_data = new int[16384];
    static int syöte_kesto, syöte_toimi, tulos_kesto, syötetiedosto = -1, kohdetiedosto_9ceb7bd4 = -1;
    static boolean pystyviiva_syöte, pystyviiva_tulos;
    static int virhe_ARVO;
    static boolean Salli_vuorovaikutteinen = true;
    public static int tietojärjestelmät_vuorovaikutteinen() { return Salli_vuorovaikutteinen && syötetiedosto < 3 && kohdetiedosto_9ceb7bd4 < 3 && !pystyviiva_syöte && !pystyviiva_tulos ? 1 : 0; }
    public static int tulostuspaikka(int Media_ARVO, int ARVO) {
        if (Media_ARVO != 1) return 0;
        if (kohdetiedosto_9ceb7bd4 >= 3) { int 처리값 = Muisti_Files.Kirjoitus(kohdetiedosto_9ceb7bd4, ARVO); if (처리값 < 0) virhe_ARVO = 처리값; return 1; }
        if (!pystyviiva_tulos) return 0;
        if (tulos_kesto == tulos_data.length) virhe_ARVO = -28;
        else tulos_data[tulos_kesto++] = ARVO;
        return 1;
    }
    public static int syöte_ARVO() {
        if (syötetiedosto >= 3) { int 처리값 = Muisti_Files.Luku(syötetiedosto); return 처리값 == 256 ? -2 : 처리값; }
        if (pystyviiva_syöte) return syöte_toimi < syöte_kesto ? syöte_data[syöte_toimi++] : -2;
        return -3; // UART로 siirrä_ARVO_24592b8a
    }
    static void Suorita_2(boolean riviväli_pystyviiva, boolean seuraava_pystyviiva) {
        pystyviiva_syöte = riviväli_pystyviiva; pystyviiva_tulos = seuraava_pystyviiva;
        syöte_toimi = 0; tulos_kesto = 0; syötetiedosto = -1; kohdetiedosto_9ceb7bd4 = -1; virhe_ARVO = 0;
    }
    static void 끝() {
        Taulu.입출력전환(0);
        if (syötetiedosto >= 3) Muisti_Files.Sulje(syötetiedosto);
        if (kohdetiedosto_9ceb7bd4 >= 3) Muisti_Files.Sulje(kohdetiedosto_9ceb7bd4);
        if (pystyviiva_tulos) { syöte_kesto = tulos_kesto; for (int Loop_INDEKSI = 0; Loop_INDEKSI < tulos_kesto; Loop_INDEKSI++) syöte_data[Loop_INDEKSI] = tulos_data[Loop_INDEKSI]; }
        syötetiedosto = -1; kohdetiedosto_9ceb7bd4 = -1; pystyviiva_syöte = false; pystyviiva_tulos = false;
    }
}
