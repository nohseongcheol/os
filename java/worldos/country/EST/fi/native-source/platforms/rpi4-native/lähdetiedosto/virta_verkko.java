// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ydin_ARVO 안의 연결형 tavu_ARVO virta_ARVO. Ethernet/TCP 패킷 스택이 아닌 루프백 socket kerros_ARVO_e65604ef. */
public final class virta_verkko {
    static int[] Tila_ARVO = new int[16], portti_ARVO = new int[16], 짝 = new int[16], vertaissolmu_portti = new int[16], odottaa_ARVO = new int[16], tietojärjestelmät_raja = new int[16];
    static int[] etukamera_ARVO = new int[16], numero = new int[16], data = new int[16 * 1024];
    static int Seuraava_kohde = 50000;
    static int tarkistaa(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Tila_ARVO[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int portin_numero) { for (int Loop_INDEKSI = 0; Loop_INDEKSI < 16; Loop_INDEKSI++) if (Tila_ARVO[Loop_INDEKSI] != 0 && tietojärjestelmät_raja[Loop_INDEKSI] != 0 && portti_ARVO[Loop_INDEKSI] == portin_numero) return true; return false; }
    public static int Luo_merkintä() {
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 16; Loop_INDEKSI++) if (Tila_ARVO[Loop_INDEKSI] == 0) { Tila_ARVO[Loop_INDEKSI] = 1; vertaissolmu_portti[Loop_INDEKSI] = portti_ARVO[Loop_INDEKSI] = etukamera_ARVO[Loop_INDEKSI] = numero[Loop_INDEKSI] = odottaa_ARVO[Loop_INDEKSI] = tietojärjestelmät_raja[Loop_INDEKSI] = 0; 짝[Loop_INDEKSI] = -1; return Loop_INDEKSI + 40; }
        return -24;
    }
    public static int BIND_päätepiste(int 열린파일번호, int vastake_OSOITE, int portin_numero) {
        int Loop_INDEKSI = tarkistaa(열린파일번호); if (Loop_INDEKSI < 0) return -9;
        if (vastake_OSOITE != 0 && vastake_OSOITE != 0x7f000001) return -99;
        if (Tila_ARVO[Loop_INDEKSI] != 1 || portin_numero < 0 || portin_numero > 65535) return -22;
        if (portin_numero == 0) { do { portin_numero = Seuraava_kohde++; if (Seuraava_kohde > 65535) Seuraava_kohde = 50000; } while (사용중(portin_numero)); }
        if (사용중(portin_numero)) return -98; portti_ARVO[Loop_INDEKSI] = portin_numero; tietojärjestelmät_raja[Loop_INDEKSI] = 1; Tila_ARVO[Loop_INDEKSI] = 2; return 0;
    }
    public static int kuunnella_päätepiste(int 열린파일번호, int keskeneräiset_työt) { int Loop_INDEKSI = tarkistaa(열린파일번호); if (Loop_INDEKSI < 0) return -9; if (Tila_ARVO[Loop_INDEKSI] != 2 || keskeneräiset_työt < 1) return -22; Tila_ARVO[Loop_INDEKSI] = 3; return 0; }
    public static int Yhdistä(int 열린파일번호, int vastake_OSOITE, int portin_numero) {
        int Loop_INDEKSI = tarkistaa(열린파일번호); if (Loop_INDEKSI < 0) return -9; if (vastake_OSOITE != 0x7f000001) return -101;
        if (portin_numero < 1 || portin_numero > 65535 || Tila_ARVO[Loop_INDEKSI] > 2) return -22;
        int saada_page = -1; for (int sisäliitos_toimi = 0; sisäliitos_toimi < 16; sisäliitos_toimi++) if (Tila_ARVO[sisäliitos_toimi] == 3 && portti_ARVO[sisäliitos_toimi] == portin_numero) saada_page = sisäliitos_toimi;
        if (saada_page < 0) return -111;
        int 대기여부 = 0; for (int sisäliitos_toimi = 0; sisäliitos_toimi < 16; sisäliitos_toimi++) if (odottaa_ARVO[sisäliitos_toimi] == saada_page + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Tila_ARVO[Loop_INDEKSI] == 1) { int 처리값 = BIND_päätepiste(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int muut = Luo_merkintä(); if (muut < 0) return muut; muut -= 40;
        Tila_ARVO[Loop_INDEKSI] = Tila_ARVO[muut] = 4; 짝[Loop_INDEKSI] = muut; 짝[muut] = Loop_INDEKSI; portti_ARVO[muut] = portin_numero; vertaissolmu_portti[Loop_INDEKSI] = portin_numero; vertaissolmu_portti[muut] = portti_ARVO[Loop_INDEKSI]; odottaa_ARVO[muut] = saada_page + 1; return 0;
    }
    public static int hyväksyä_yhteys(int 열린파일번호) { int Loop_INDEKSI = tarkistaa(열린파일번호); if (Loop_INDEKSI < 0) return -9; if (Tila_ARVO[Loop_INDEKSI] != 3) return -22; for (int sisäliitos_toimi = 0; sisäliitos_toimi < 16; sisäliitos_toimi++) if (Tila_ARVO[sisäliitos_toimi] != 0 && odottaa_ARVO[sisäliitos_toimi] == Loop_INDEKSI + 1) { odottaa_ARVO[sisäliitos_toimi] = 0; return sisäliitos_toimi + 40; } return -11; }
    public static int Kirjoitus(int 열린파일번호, int merkintä_LASKE) {
        int Loop_INDEKSI = tarkistaa(열린파일번호); if (Loop_INDEKSI < 0) return -9; if (Tila_ARVO[Loop_INDEKSI] != 4) return -107;
        if (merkintä_LASKE < 0 || merkintä_LASKE > 512) return -22; if (merkintä_LASKE == 0) return 0;
        int sisäliitos_toimi = 짝[Loop_INDEKSI]; if (sisäliitos_toimi < 0) return -32; int summa_LASKE = 1024 - numero[sisäliitos_toimi]; if (summa_LASKE == 0) return -11; if (summa_LASKE > merkintä_LASKE) summa_LASKE = merkintä_LASKE;
        for (int Vertailu_toimi = 0; Vertailu_toimi < summa_LASKE; Vertailu_toimi++) data[sisäliitos_toimi * 1024 + (etukamera_ARVO[sisäliitos_toimi] + numero[sisäliitos_toimi] + Vertailu_toimi) % 1024] = silmukka_verkko.siirrä_ARVO_24592b8a[Vertailu_toimi]; numero[sisäliitos_toimi] += summa_LASKE; return summa_LASKE;
    }
    public static int Luku(int 열린파일번호, int merkintä_LASKE) {
        int Loop_INDEKSI = tarkistaa(열린파일번호); if (Loop_INDEKSI < 0) return -9; if (Tila_ARVO[Loop_INDEKSI] != 4) return -107; if (merkintä_LASKE < 0 || merkintä_LASKE > 512) return -22;
        if (merkintä_LASKE == 0) return 0; if (numero[Loop_INDEKSI] == 0) return 짝[Loop_INDEKSI] < 0 ? 0 : -11; if (merkintä_LASKE > numero[Loop_INDEKSI]) merkintä_LASKE = numero[Loop_INDEKSI];
        for (int Vertailu_toimi = 0; Vertailu_toimi < merkintä_LASKE; Vertailu_toimi++) silmukka_verkko.siirrä_ARVO_24592b8a[Vertailu_toimi] = data[Loop_INDEKSI * 1024 + (etukamera_ARVO[Loop_INDEKSI] + Vertailu_toimi) % 1024]; etukamera_ARVO[Loop_INDEKSI] = (etukamera_ARVO[Loop_INDEKSI] + merkintä_LASKE) % 1024; numero[Loop_INDEKSI] -= merkintä_LASKE; return merkintä_LASKE;
    }
    public static int lukea_päätepiste_portti(int 열린파일번호) { int Loop_INDEKSI = tarkistaa(열린파일번호); return Loop_INDEKSI < 0 ? -9 : portti_ARVO[Loop_INDEKSI]; }
    public static int lukea_vertaissolmu_portti(int 열린파일번호) { int Loop_INDEKSI = tarkistaa(열린파일번호); return Loop_INDEKSI < 0 ? -9 : vertaissolmu_portti[Loop_INDEKSI]; }
    public static int Sulje(int 열린파일번호) {
        int Loop_INDEKSI = tarkistaa(열린파일번호); if (Loop_INDEKSI < 0) return -9;
        if (Tila_ARVO[Loop_INDEKSI] == 3) for (int sisäliitos_toimi = 0; sisäliitos_toimi < 16; sisäliitos_toimi++) if (odottaa_ARVO[sisäliitos_toimi] == Loop_INDEKSI + 1) { if (짝[sisäliitos_toimi] >= 0) 짝[짝[sisäliitos_toimi]] = -1; Tila_ARVO[sisäliitos_toimi] = odottaa_ARVO[sisäliitos_toimi] = tietojärjestelmät_raja[sisäliitos_toimi] = 0; }
        if (짝[Loop_INDEKSI] >= 0) 짝[짝[Loop_INDEKSI]] = -1; Tila_ARVO[Loop_INDEKSI] = tietojärjestelmät_raja[Loop_INDEKSI] = numero[Loop_INDEKSI] = odottaa_ARVO[Loop_INDEKSI] = 0; return 0;
    }
}
