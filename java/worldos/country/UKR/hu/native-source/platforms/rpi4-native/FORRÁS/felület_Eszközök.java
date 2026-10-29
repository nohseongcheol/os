// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 felület 내장 Eszközök. */
public final class felület_Eszközök {
    static int[] adat = new int[16384];
    static int bemeneti_fájl = -1;
    static int készít_Fájl(int argumentum_INDEX, int folyamat_mód) {
        int 처리값 = 명령해석기.ÚTVONAL(argumentum_INDEX); return 처리값 < 0 ? 처리값 : Memória_Files.Megnyitás(folyamat_mód);
    }
    static boolean Előkészítés_bevitel(int argumentum_INDEX) {
        bemeneti_fájl = -1;
        if (argumentum_INDEX < 명령해석기.kód_DARAB) {
            bemeneti_fájl = készít_Fájl(argumentum_INDEX, 0);
            if (bemeneti_fájl < 0) { 명령해석기.HIBA(bemeneti_fájl); return false; }
        }
        return true;
    }
    static int Olvasás() {
        if (bemeneti_fájl >= 3) return Memória_Files.Olvasás(bemeneti_fájl);
        while (true) {
            int bájt_adat = fal.직렬읽기(); if (bájt_adat == -2 || bájt_adat == 4) return 256;
            if (bájt_adat == 3) { 명령해석기.KR = 130; return 256; }
            if (bájt_adat >= 0) return bájt_adat; fal.HOZAM_CPU();
        }
    }
    static void Bezárás() { if (bemeneti_fájl >= 3) Memória_Files.Bezárás(bemeneti_fájl); bemeneti_fájl = -1; }
    static void Nézet_ÉRTÉK() {
        int 마지막자리 = 명령해석기.kód_DARAB == 1 ? 2 : 명령해석기.kód_DARAB;
        for (int argumentum_INDEX = 1; argumentum_INDEX < 마지막자리; argumentum_INDEX++) {
            if (!Előkészítés_bevitel(argumentum_INDEX)) continue;
            int bájt_adat; while ((bájt_adat = Olvasás()) != 256 && bájt_adat >= 0) fal.직렬쓰기(bájt_adat);
            if (bájt_adat < 0) 명령해석기.HIBA(bájt_adat); Bezárás();
        }
    }
    static void Fájl_eset(String Action_szám) {
        if (명령해석기.kód_DARAB != 2) { 명령해석기.KR = 2; 단말.Írás("사용법: mkdir/rmdir/touch Fájl\n"); return; }
        int 처리값 = 명령해석기.ÚTVONAL(1);
        if (처리값 >= 0) {
            if (Action_szám.charAt(0) == 'm') 처리값 = Memória_Files.készít_címtár();
            else if (Action_szám.charAt(0) == 'r') 처리값 = Memória_Files.eltávolít_címtár();
            else { 처리값 = Memória_Files.Megnyitás(65); if (처리값 >= 3) 처리값 = Memória_Files.Bezárás(처리값); }
        }
        if (처리값 < 0) 명령해석기.HIBA(처리값);
    }
    static void másol_ÉRTÉK(boolean 이동여부) {
        if (명령해석기.kód_DARAB != 3) { 명령해석기.KR = 2; 단말.Írás("사용법: cp/mv 원본 cél_végpont (Fájl)\n"); return; }
        int 처리값 = 명령해석기.ÚTVONAL(1); if (처리값 >= 0) 처리값 = Memória_Files.normalizál_ÉRTÉK();
        if (처리값 < 0) { 명령해석기.HIBA(처리값); return; }
        int 원본번호 = Memória_Files.keres_bejegyzés(); if (원본번호 < 0) { 명령해석기.HIBA(-2); return; }
        int bejegyzés_DARAB = Memória_Files.hossz_ÉRTÉK[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) adat[Loop_INDEX] = Memória_Files.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.ÚTVONAL(2); if (처리값 >= 0) 처리값 = Memória_Files.normalizál_ÉRTÉK();
        if (처리값 < 0) { 명령해석기.HIBA(처리값); return; }
        if (Memória_Files.keres_bejegyzés() == 원본번호) { if (!이동여부) 명령해석기.HIBA(-22); return; }
        if (이동여부) { 처리값 = Memória_Files.Átnevezés_bejegyzés(원본번호); if (처리값 < 0) 명령해석기.HIBA(처리값); return; }
        int 열린파일번호 = Memória_Files.Megnyitás(577); if (열린파일번호 < 0) { 명령해석기.HIBA(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) { 처리값 = Memória_Files.Írás(열린파일번호, adat[Loop_INDEX]); if (처리값 < 0) { 명령해석기.HIBA(처리값); break; } }
        Memória_Files.Bezárás(열린파일번호);
    }
    static int számjegy_ÉRTÉK(int argumentum_INDEX) {
        if (argumentum_INDEX >= 명령해석기.kód_DARAB) return -1;
        int bejegyzés_DARAB = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.hossz_ÉRTÉK[argumentum_INDEX]; Loop_INDEX++) { int kódpont = 명령해석기.kód_ÉRTÉK[명령해석기.시작점[argumentum_INDEX] + Loop_INDEX]; if (kódpont < '0' || kódpont > '9' || bejegyzés_DARAB > 10000) return -1; bejegyzés_DARAB = bejegyzés_DARAB * 10 + kódpont - '0'; } return bejegyzés_DARAB;
    }
    static void 세기() {
        int argumentum_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argumentum_INDEX++; }
        if (명령해석기.kód_DARAB > argumentum_INDEX + 1) { 명령해석기.KR = 2; 단말.Írás("사용법: wc [-c|-l|-w] [Fájl]\n"); return; }
        if (!Előkészítés_bevitel(argumentum_INDEX)) return;
        int bájt_DARAB = 0, 줄수 = 0, 낱말수 = 0, bájt_adat; boolean 낱말 = false;
        while ((bájt_adat = Olvasás()) >= 0 && bájt_adat != 256) { bájt_DARAB++; if (bájt_adat == 10) 줄수++; boolean tér = bájt_adat == 32 || bájt_adat >= 9 && bájt_adat <= 13; if (!tér && !낱말) 낱말수++; 낱말 = !tér; }
        Bezárás(); if (bájt_adat < 0) { 명령해석기.HIBA(bájt_adat); return; }
        if (선택번호 != 0) 단말.szám(선택번호 == 1 ? bájt_DARAB : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.szám(줄수); 단말.문자(' '); 단말.szám(낱말수); 단말.문자(' '); 단말.szám(bájt_DARAB); } 단말.문자(10);
    }
    static void keres_bejegyzés() {
        if (명령해석기.kód_DARAB < 2 || 명령해석기.kód_DARAB > 3) { 명령해석기.KR = 2; 단말.Írás("사용법: grep 찾을문구 [Fájl]\n"); return; }
        if (!Előkészítés_bevitel(2)) return;
        int bejegyzés_DARAB = 0, bájt_adat, 일치수 = 0;
        while (true) {
            bájt_adat = Olvasás();
            if (bájt_adat == 10 || bájt_adat == 256 || bájt_adat < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= bejegyzés_DARAB - 명령해석기.hossz_ÉRTÉK[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int belső_pozíció = 0; belső_pozíció < 명령해석기.hossz_ÉRTÉK[1]; belső_pozíció++) if (adat[Loop_INDEX + belső_pozíció] != 명령해석기.kód_ÉRTÉK[명령해석기.시작점[1] + belső_pozíció]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (bejegyzés_DARAB > 0 || bájt_adat == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) fal.직렬쓰기(adat[Loop_INDEX]); 단말.문자(10); 일치수++; }
                bejegyzés_DARAB = 0; if (bájt_adat != 10) break;
            } else if (bejegyzés_DARAB < adat.length) adat[bejegyzés_DARAB++] = bájt_adat;
            else { 명령해석기.HIBA(-28); Bezárás(); return; }
        }
        Bezárás(); if (bájt_adat < 0) 명령해석기.HIBA(bájt_adat); else if (명령해석기.KR == 0) 명령해석기.KR = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argumentum_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = számjegy_ÉRTÉK(2); argumentum_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.kód_DARAB > argumentum_INDEX + 1) { 명령해석기.KR = 2; 단말.Írás("사용법: head/tail [-n 줄수] [Fájl]\n"); return; }
        if (!Előkészítés_bevitel(argumentum_INDEX)) return;
        int bejegyzés_DARAB = 0, bájt_adat;
        while ((bájt_adat = Olvasás()) != 256 && bájt_adat >= 0) { if (bejegyzés_DARAB == adat.length) { 명령해석기.HIBA(-28); Bezárás(); return; } adat[bejegyzés_DARAB++] = bájt_adat; }
        Bezárás(); if (bájt_adat < 0) { 명령해석기.HIBA(bájt_adat); return; }
        int helyi_START = 0, megszüntet_pozíció = bejegyzés_DARAB;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int összesen_DARAB = 0; for (int Loop_INDEX = bejegyzés_DARAB - 2; Loop_INDEX >= 0; Loop_INDEX--) if (adat[Loop_INDEX] == 10 && ++összesen_DARAB == 줄수) { helyi_START = Loop_INDEX + 1; break; } }
        else { int összesen_DARAB = 0; for (int Loop_INDEX = 0; Loop_INDEX < bejegyzés_DARAB; Loop_INDEX++) if (adat[Loop_INDEX] == 10 && ++összesen_DARAB == 줄수) { megszüntet_pozíció = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = helyi_START; Loop_INDEX < megszüntet_pozíció; Loop_INDEX++) fal.직렬쓰기(adat[Loop_INDEX]);
    }
    static void ír_Együtt() {
        boolean hozzáfűz = 명령해석기.같음(1, "-a"); int argumentum_INDEX = hozzáfűz ? 2 : 1;
        if (명령해석기.kód_DARAB != argumentum_INDEX + 1) { 명령해석기.KR = 2; 단말.Írás("사용법: tee [-a] Fájl\n"); return; }
        int 열린파일번호 = készít_Fájl(argumentum_INDEX, hozzáfűz ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.HIBA(열린파일번호); return; }
        bemeneti_fájl = -1; int bájt_adat;
        while ((bájt_adat = Olvasás()) != 256 && bájt_adat >= 0) { int 처리값 = Memória_Files.Írás(열린파일번호, bájt_adat); if (처리값 < 0) { 명령해석기.HIBA(처리값); break; } fal.직렬쓰기(bájt_adat); }
        Memória_Files.Bezárás(열린파일번호);
    }
}
