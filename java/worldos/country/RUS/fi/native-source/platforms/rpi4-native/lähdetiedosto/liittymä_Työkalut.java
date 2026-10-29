// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 liittymä 내장 työkalut. */
public final class liittymä_Työkalut {
    static int[] data = new int[16384];
    static int syötetiedosto = -1;
    static int avata_Tiedosto(int argumentti_INDEKSI, int prosessi_tila) {
        int 처리값 = 명령해석기.polku_2(argumentti_INDEKSI); return 처리값 < 0 ? 처리값 : Muisti_Files.Avaa(prosessi_tila);
    }
    static boolean Valmistele_syöte(int argumentti_INDEKSI) {
        syötetiedosto = -1;
        if (argumentti_INDEKSI < 명령해석기.tunnus_LASKE) {
            syötetiedosto = avata_Tiedosto(argumentti_INDEKSI, 0);
            if (syötetiedosto < 0) { 명령해석기.VIRHE(syötetiedosto); return false; }
        }
        return true;
    }
    static int Luku() {
        if (syötetiedosto >= 3) return Muisti_Files.Luku(syötetiedosto);
        while (true) {
            int tavu_data = Taulu.직렬읽기(); if (tavu_data == -2 || tavu_data == 4) return 256;
            if (tavu_data == 3) { 명령해석기.TULOS = 130; return 256; }
            if (tavu_data >= 0) return tavu_data; Taulu.TUOTTO_suoritin();
        }
    }
    static void Sulje() { if (syötetiedosto >= 3) Muisti_Files.Sulje(syötetiedosto); syötetiedosto = -1; }
    static void Näkymä_ARVO() {
        int 마지막자리 = 명령해석기.tunnus_LASKE == 1 ? 2 : 명령해석기.tunnus_LASKE;
        for (int argumentti_INDEKSI = 1; argumentti_INDEKSI < 마지막자리; argumentti_INDEKSI++) {
            if (!Valmistele_syöte(argumentti_INDEKSI)) continue;
            int tavu_data; while ((tavu_data = Luku()) != 256 && tavu_data >= 0) Taulu.직렬쓰기(tavu_data);
            if (tavu_data < 0) 명령해석기.VIRHE(tavu_data); Sulje();
        }
    }
    static void Tiedosto_työ(String toimi_numero) {
        if (명령해석기.tunnus_LASKE != 2) { 명령해석기.TULOS = 2; 단말.Kirjoitus("사용법: mkdir/rmdir/touch tiedoston_nimi\n"); return; }
        int 처리값 = 명령해석기.polku_2(1);
        if (처리값 >= 0) {
            if (toimi_numero.charAt(0) == 'm') 처리값 = Muisti_Files.Luo_Directory();
            else if (toimi_numero.charAt(0) == 'r') 처리값 = Muisti_Files.poistaa_Directory();
            else { 처리값 = Muisti_Files.Avaa(65); if (처리값 >= 3) 처리값 = Muisti_Files.Sulje(처리값); }
        }
        if (처리값 < 0) 명령해석기.VIRHE(처리값);
    }
    static void kopioida_ARVO(boolean 이동여부) {
        if (명령해석기.tunnus_LASKE != 3) { 명령해석기.TULOS = 2; 단말.Kirjoitus("사용법: cp/mv 원본 kohde_päätepiste (tiedoston_nimi)\n"); return; }
        int 처리값 = 명령해석기.polku_2(1); if (처리값 >= 0) 처리값 = Muisti_Files.normalisoida_ARVO();
        if (처리값 < 0) { 명령해석기.VIRHE(처리값); return; }
        int 원본번호 = Muisti_Files.ETSI_merkintä(); if (원본번호 < 0) { 명령해석기.VIRHE(-2); return; }
        int merkintä_LASKE = Muisti_Files.kesto_ARVO[원본번호]; for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) data[Loop_INDEKSI] = Muisti_Files.lukea_data(원본번호, Loop_INDEKSI);
        처리값 = 명령해석기.polku_2(2); if (처리값 >= 0) 처리값 = Muisti_Files.normalisoida_ARVO();
        if (처리값 < 0) { 명령해석기.VIRHE(처리값); return; }
        if (Muisti_Files.ETSI_merkintä() == 원본번호) { if (!이동여부) 명령해석기.VIRHE(-22); return; }
        if (이동여부) { 처리값 = Muisti_Files.Nimeä_uudelleen_merkintä(원본번호); if (처리값 < 0) 명령해석기.VIRHE(처리값); return; }
        int 열린파일번호 = Muisti_Files.Avaa(577); if (열린파일번호 < 0) { 명령해석기.VIRHE(열린파일번호); return; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) { 처리값 = Muisti_Files.Kirjoitus(열린파일번호, data[Loop_INDEKSI]); if (처리값 < 0) { 명령해석기.VIRHE(처리값); break; } }
        Muisti_Files.Sulje(열린파일번호);
    }
    static int numero_ARVO(int argumentti_INDEKSI) {
        if (argumentti_INDEKSI >= 명령해석기.tunnus_LASKE) return -1;
        int merkintä_LASKE = 0; for (int Loop_INDEKSI = 0; Loop_INDEKSI < 명령해석기.kesto_ARVO[argumentti_INDEKSI]; Loop_INDEKSI++) { int merkkikoodi = 명령해석기.tunnus_ARVO_eb540501[명령해석기.시작점[argumentti_INDEKSI] + Loop_INDEKSI]; if (merkkikoodi < '0' || merkkikoodi > '9' || merkintä_LASKE > 10000) return -1; merkintä_LASKE = merkintä_LASKE * 10 + merkkikoodi - '0'; } return merkintä_LASKE;
    }
    static void 세기() {
        int argumentti_INDEKSI = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argumentti_INDEKSI++; }
        if (명령해석기.tunnus_LASKE > argumentti_INDEKSI + 1) { 명령해석기.TULOS = 2; 단말.Kirjoitus("사용법: wc [-c|-l|-w] [tiedoston_nimi]\n"); return; }
        if (!Valmistele_syöte(argumentti_INDEKSI)) return;
        int tavu_LASKE = 0, 줄수 = 0, 낱말수 = 0, tavu_data; boolean 낱말 = false;
        while ((tavu_data = Luku()) >= 0 && tavu_data != 256) { tavu_LASKE++; if (tavu_data == 10) 줄수++; boolean tila = tavu_data == 32 || tavu_data >= 9 && tavu_data <= 13; if (!tila && !낱말) 낱말수++; 낱말 = !tila; }
        Sulje(); if (tavu_data < 0) { 명령해석기.VIRHE(tavu_data); return; }
        if (선택번호 != 0) 단말.numero(선택번호 == 1 ? tavu_LASKE : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.numero(줄수); 단말.문자(' '); 단말.numero(낱말수); 단말.문자(' '); 단말.numero(tavu_LASKE); } 단말.문자(10);
    }
    static void ETSI_merkintä() {
        if (명령해석기.tunnus_LASKE < 2 || 명령해석기.tunnus_LASKE > 3) { 명령해석기.TULOS = 2; 단말.Kirjoitus("사용법: grep 찾을문구 [tiedoston_nimi]\n"); return; }
        if (!Valmistele_syöte(2)) return;
        int merkintä_LASKE = 0, tavu_data, 일치수 = 0;
        while (true) {
            tavu_data = Luku();
            if (tavu_data == 10 || tavu_data == 256 || tavu_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEKSI = 0; Loop_INDEKSI <= merkintä_LASKE - 명령해석기.kesto_ARVO[1]; Loop_INDEKSI++) {
                    boolean 같은여부 = true; for (int sisäliitos_toimi = 0; sisäliitos_toimi < 명령해석기.kesto_ARVO[1]; sisäliitos_toimi++) if (data[Loop_INDEKSI + sisäliitos_toimi] != 명령해석기.tunnus_ARVO_eb540501[명령해석기.시작점[1] + sisäliitos_toimi]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (merkintä_LASKE > 0 || tavu_data == 10)) { for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) Taulu.직렬쓰기(data[Loop_INDEKSI]); 단말.문자(10); 일치수++; }
                merkintä_LASKE = 0; if (tavu_data != 10) break;
            } else if (merkintä_LASKE < data.length) data[merkintä_LASKE++] = tavu_data;
            else { 명령해석기.VIRHE(-28); Sulje(); return; }
        }
        Sulje(); if (tavu_data < 0) 명령해석기.VIRHE(tavu_data); else if (명령해석기.TULOS == 0) 명령해석기.TULOS = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argumentti_INDEKSI = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = numero_ARVO(2); argumentti_INDEKSI = 3; }
        if (줄수 < 0 || 명령해석기.tunnus_LASKE > argumentti_INDEKSI + 1) { 명령해석기.TULOS = 2; 단말.Kirjoitus("사용법: head/tail [-n 줄수] [tiedoston_nimi]\n"); return; }
        if (!Valmistele_syöte(argumentti_INDEKSI)) return;
        int merkintä_LASKE = 0, tavu_data;
        while ((tavu_data = Luku()) != 256 && tavu_data >= 0) { if (merkintä_LASKE == data.length) { 명령해석기.VIRHE(-28); Sulje(); return; } data[merkintä_LASKE++] = tavu_data; }
        Sulje(); if (tavu_data < 0) { 명령해석기.VIRHE(tavu_data); return; }
        int paikallinen_alku = 0, lopettaa_puhelu_toimi = merkintä_LASKE;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int summa_LASKE = 0; for (int Loop_INDEKSI = merkintä_LASKE - 2; Loop_INDEKSI >= 0; Loop_INDEKSI--) if (data[Loop_INDEKSI] == 10 && ++summa_LASKE == 줄수) { paikallinen_alku = Loop_INDEKSI + 1; break; } }
        else { int summa_LASKE = 0; for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) if (data[Loop_INDEKSI] == 10 && ++summa_LASKE == 줄수) { lopettaa_puhelu_toimi = Loop_INDEKSI + 1; break; } }
        for (int Loop_INDEKSI = paikallinen_alku; Loop_INDEKSI < lopettaa_puhelu_toimi; Loop_INDEKSI++) Taulu.직렬쓰기(data[Loop_INDEKSI]);
    }
    static void kirjoitus_Yhdessä() {
        boolean liitä = 명령해석기.같음(1, "-a"); int argumentti_INDEKSI = liitä ? 2 : 1;
        if (명령해석기.tunnus_LASKE != argumentti_INDEKSI + 1) { 명령해석기.TULOS = 2; 단말.Kirjoitus("사용법: tee [-a] tiedoston_nimi\n"); return; }
        int 열린파일번호 = avata_Tiedosto(argumentti_INDEKSI, liitä ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.VIRHE(열린파일번호); return; }
        syötetiedosto = -1; int tavu_data;
        while ((tavu_data = Luku()) != 256 && tavu_data >= 0) { int 처리값 = Muisti_Files.Kirjoitus(열린파일번호, tavu_data); if (처리값 < 0) { 명령해석기.VIRHE(처리값); break; } Taulu.직렬쓰기(tavu_data); }
        Muisti_Files.Sulje(열린파일번호);
    }
}
