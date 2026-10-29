// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 Shell 내장 verktyg. */
public final class Shell_Verktyg {
    static int[] data = new int[16384];
    static int indatafil = -1;
    static int skapa_fil(int argument_INDEX, int Process_läge) {
        int 처리값 = 명령해석기.sökväg_2(argument_INDEX); return 처리값 < 0 ? 처리값 : Minne_Filer.Öppna(Process_läge);
    }
    static boolean Förbereda_indata(int argument_INDEX) {
        indatafil = -1;
        if (argument_INDEX < 명령해석기.kod_ANTAL) {
            indatafil = skapa_fil(argument_INDEX, 0);
            if (indatafil < 0) { 명령해석기.fel(indatafil); return false; }
        }
        return true;
    }
    static int Läs() {
        if (indatafil >= 3) return Minne_Filer.Läs(indatafil);
        while (true) {
            int byte_data = Tavla.직렬읽기(); if (byte_data == -2 || byte_data == 4) return 256;
            if (byte_data == 3) { 명령해석기.RESULTAT = 130; return 256; }
            if (byte_data >= 0) return byte_data; Tavla.NOMAVK_CPU();
        }
    }
    static void Stäng() { if (indatafil >= 3) Minne_Filer.Stäng(indatafil); indatafil = -1; }
    static void vy_värde() {
        int 마지막자리 = 명령해석기.kod_ANTAL == 1 ? 2 : 명령해석기.kod_ANTAL;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!Förbereda_indata(argument_INDEX)) continue;
            int byte_data; while ((byte_data = Läs()) != 256 && byte_data >= 0) Tavla.직렬쓰기(byte_data);
            if (byte_data < 0) 명령해석기.fel(byte_data); Stäng();
        }
    }
    static void fil_Jobb(String Action_nummer) {
        if (명령해석기.kod_ANTAL != 2) { 명령해석기.RESULTAT = 2; 단말.Skriv("사용법: mkdir/rmdir/touch filnamn\n"); return; }
        int 처리값 = 명령해석기.sökväg_2(1);
        if (처리값 >= 0) {
            if (Action_nummer.charAt(0) == 'm') 처리값 = Minne_Filer.Skapa_Katalog();
            else if (Action_nummer.charAt(0) == 'r') 처리값 = Minne_Filer.ta_bort_Katalog();
            else { 처리값 = Minne_Filer.Öppna(65); if (처리값 >= 3) 처리값 = Minne_Filer.Stäng(처리값); }
        }
        if (처리값 < 0) 명령해석기.fel(처리값);
    }
    static void kopia_värde(boolean 이동여부) {
        if (명령해석기.kod_ANTAL != 3) { 명령해석기.RESULTAT = 2; 단말.Skriv("사용법: cp/mv 원본 mål_deltagare (filnamn)\n"); return; }
        int 처리값 = 명령해석기.sökväg_2(1); if (처리값 >= 0) 처리값 = Minne_Filer.normalisera_värde();
        if (처리값 < 0) { 명령해석기.fel(처리값); return; }
        int 원본번호 = Minne_Filer.Sök_post(); if (원본번호 < 0) { 명령해석기.fel(-2); return; }
        int post_ANTAL = Minne_Filer.längd_värde[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) data[Loop_INDEX] = Minne_Filer.läsa_data(원본번호, Loop_INDEX);
        처리값 = 명령해석기.sökväg_2(2); if (처리값 >= 0) 처리값 = Minne_Filer.normalisera_värde();
        if (처리값 < 0) { 명령해석기.fel(처리값); return; }
        if (Minne_Filer.Sök_post() == 원본번호) { if (!이동여부) 명령해석기.fel(-22); return; }
        if (이동여부) { 처리값 = Minne_Filer.Byt_namn_post(원본번호); if (처리값 < 0) 명령해석기.fel(처리값); return; }
        int 열린파일번호 = Minne_Filer.Öppna(577); if (열린파일번호 < 0) { 명령해석기.fel(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) { 처리값 = Minne_Filer.Skriv(열린파일번호, data[Loop_INDEX]); if (처리값 < 0) { 명령해석기.fel(처리값); break; } }
        Minne_Filer.Stäng(열린파일번호);
    }
    static int siffra_värde(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.kod_ANTAL) return -1;
        int post_ANTAL = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.längd_värde[argument_INDEX]; Loop_INDEX++) { int kodpunkt = 명령해석기.kod_värde[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (kodpunkt < '0' || kodpunkt > '9' || post_ANTAL > 10000) return -1; post_ANTAL = post_ANTAL * 10 + kodpunkt - '0'; } return post_ANTAL;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.kod_ANTAL > argument_INDEX + 1) { 명령해석기.RESULTAT = 2; 단말.Skriv("사용법: wc [-c|-l|-w] [filnamn]\n"); return; }
        if (!Förbereda_indata(argument_INDEX)) return;
        int byte_ANTAL = 0, 줄수 = 0, 낱말수 = 0, byte_data; boolean 낱말 = false;
        while ((byte_data = Läs()) >= 0 && byte_data != 256) { byte_ANTAL++; if (byte_data == 10) 줄수++; boolean Space = byte_data == 32 || byte_data >= 9 && byte_data <= 13; if (!Space && !낱말) 낱말수++; 낱말 = !Space; }
        Stäng(); if (byte_data < 0) { 명령해석기.fel(byte_data); return; }
        if (선택번호 != 0) 단말.nummer(선택번호 == 1 ? byte_ANTAL : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.nummer(줄수); 단말.문자(' '); 단말.nummer(낱말수); 단말.문자(' '); 단말.nummer(byte_ANTAL); } 단말.문자(10);
    }
    static void Sök_post() {
        if (명령해석기.kod_ANTAL < 2 || 명령해석기.kod_ANTAL > 3) { 명령해석기.RESULTAT = 2; 단말.Skriv("사용법: grep 찾을문구 [filnamn]\n"); return; }
        if (!Förbereda_indata(2)) return;
        int post_ANTAL = 0, byte_data, 일치수 = 0;
        while (true) {
            byte_data = Läs();
            if (byte_data == 10 || byte_data == 256 || byte_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= post_ANTAL - 명령해석기.längd_värde[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int inre_koppling_placera = 0; inre_koppling_placera < 명령해석기.längd_värde[1]; inre_koppling_placera++) if (data[Loop_INDEX + inre_koppling_placera] != 명령해석기.kod_värde[명령해석기.시작점[1] + inre_koppling_placera]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (post_ANTAL > 0 || byte_data == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) Tavla.직렬쓰기(data[Loop_INDEX]); 단말.문자(10); 일치수++; }
                post_ANTAL = 0; if (byte_data != 10) break;
            } else if (post_ANTAL < data.length) data[post_ANTAL++] = byte_data;
            else { 명령해석기.fel(-28); Stäng(); return; }
        }
        Stäng(); if (byte_data < 0) 명령해석기.fel(byte_data); else if (명령해석기.RESULTAT == 0) 명령해석기.RESULTAT = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = siffra_värde(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.kod_ANTAL > argument_INDEX + 1) { 명령해석기.RESULTAT = 2; 단말.Skriv("사용법: head/tail [-n 줄수] [filnamn]\n"); return; }
        if (!Förbereda_indata(argument_INDEX)) return;
        int post_ANTAL = 0, byte_data;
        while ((byte_data = Läs()) != 256 && byte_data >= 0) { if (post_ANTAL == data.length) { 명령해석기.fel(-28); Stäng(); return; } data[post_ANTAL++] = byte_data; }
        Stäng(); if (byte_data < 0) { 명령해석기.fel(byte_data); return; }
        int lokal_START = 0, avsluta_placera = post_ANTAL;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int summa_ANTAL = 0; for (int Loop_INDEX = post_ANTAL - 2; Loop_INDEX >= 0; Loop_INDEX--) if (data[Loop_INDEX] == 10 && ++summa_ANTAL == 줄수) { lokal_START = Loop_INDEX + 1; break; } }
        else { int summa_ANTAL = 0; for (int Loop_INDEX = 0; Loop_INDEX < post_ANTAL; Loop_INDEX++) if (data[Loop_INDEX] == 10 && ++summa_ANTAL == 줄수) { avsluta_placera = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokal_START; Loop_INDEX < avsluta_placera; Loop_INDEX++) Tavla.직렬쓰기(data[Loop_INDEX]);
    }
    static void skriva_Tillsammans() {
        boolean Lägga_till = 명령해석기.같음(1, "-a"); int argument_INDEX = Lägga_till ? 2 : 1;
        if (명령해석기.kod_ANTAL != argument_INDEX + 1) { 명령해석기.RESULTAT = 2; 단말.Skriv("사용법: tee [-a] filnamn\n"); return; }
        int 열린파일번호 = skapa_fil(argument_INDEX, Lägga_till ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.fel(열린파일번호); return; }
        indatafil = -1; int byte_data;
        while ((byte_data = Läs()) != 256 && byte_data >= 0) { int 처리값 = Minne_Filer.Skriv(열린파일번호, byte_data); if (처리값 < 0) { 명령해석기.fel(처리값); break; } Tavla.직렬쓰기(byte_data); }
        Minne_Filer.Stäng(열린파일번호);
    }
}
