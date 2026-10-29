// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 ljuska 내장 Alati. */
public final class ljuska_Alati {
    static int[] podaci = new int[16384];
    static int ulazna_datoteka = -1;
    static int otvoreno_Datoteka(int argument_INDEX, int Proces_MODE) {
        int 처리값 = 명령해석기.PUTANJA(argument_INDEX); return 처리값 < 0 ? 처리값 : Memorija_Datoteke.Otvori(Proces_MODE);
    }
    static boolean 입력준비(int argument_INDEX) {
        ulazna_datoteka = -1;
        if (argument_INDEX < 명령해석기.token_COUNT) {
            ulazna_datoteka = otvoreno_Datoteka(argument_INDEX, 0);
            if (ulazna_datoteka < 0) { 명령해석기.GREŠKA(ulazna_datoteka); return false; }
        }
        return true;
    }
    static int Čitaj() {
        if (ulazna_datoteka >= 3) return Memorija_Datoteke.Čitaj(ulazna_datoteka);
        while (true) {
            int bajt_podaci = pano.직렬읽기(); if (bajt_podaci == -2 || bajt_podaci == 4) return 256;
            if (bajt_podaci == 3) { 명령해석기.REZULTAT = 130; return 256; }
            if (bajt_podaci >= 0) return bajt_podaci; pano.YIELD_CPU();
        }
    }
    static void Zatvori() { if (ulazna_datoteka >= 3) Memorija_Datoteke.Zatvori(ulazna_datoteka); ulazna_datoteka = -1; }
    static void Prikaz_VALUE() {
        int 마지막자리 = 명령해석기.token_COUNT == 1 ? 2 : 명령해석기.token_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int bajt_podaci; while ((bajt_podaci = Čitaj()) != 256 && bajt_podaci >= 0) pano.직렬쓰기(bajt_podaci);
            if (bajt_podaci < 0) 명령해석기.GREŠKA(bajt_podaci); Zatvori();
        }
    }
    static void Datoteka_Posao(String 동작번호) {
        if (명령해석기.token_COUNT != 2) { 명령해석기.REZULTAT = 2; 단말.Zapisuj("사용법: mkdir/rmdir/touch Datoteka\n"); return; }
        int 처리값 = 명령해석기.PUTANJA(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memorija_Datoteke.Create_imenik();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memorija_Datoteke.ukloniti_imenik();
            else { 처리값 = Memorija_Datoteke.Otvori(65); if (처리값 >= 3) 처리값 = Memorija_Datoteke.Zatvori(처리값); }
        }
        if (처리값 < 0) 명령해석기.GREŠKA(처리값);
    }
    static void instanca_VALUE(boolean 이동여부) {
        if (명령해석기.token_COUNT != 3) { 명령해석기.REZULTAT = 2; 단말.Zapisuj("사용법: cp/mv 원본 odredište_sudionik (Datoteka)\n"); return; }
        int 처리값 = 명령해석기.PUTANJA(1); if (처리값 >= 0) 처리값 = Memorija_Datoteke.normalizirati_VALUE();
        if (처리값 < 0) { 명령해석기.GREŠKA(처리값); return; }
        int 원본번호 = Memorija_Datoteke.FIND_unos(); if (원본번호 < 0) { 명령해석기.GREŠKA(-2); return; }
        int unos_COUNT = Memorija_Datoteke.길이[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) podaci[Loop_INDEX] = Memorija_Datoteke.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.PUTANJA(2); if (처리값 >= 0) 처리값 = Memorija_Datoteke.normalizirati_VALUE();
        if (처리값 < 0) { 명령해석기.GREŠKA(처리값); return; }
        if (Memorija_Datoteke.FIND_unos() == 원본번호) { if (!이동여부) 명령해석기.GREŠKA(-22); return; }
        if (이동여부) { 처리값 = Memorija_Datoteke.Preimenuj_unos(원본번호); if (처리값 < 0) 명령해석기.GREŠKA(처리값); return; }
        int 열린파일번호 = Memorija_Datoteke.Otvori(577); if (열린파일번호 < 0) { 명령해석기.GREŠKA(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) { 처리값 = Memorija_Datoteke.Zapisuj(열린파일번호, podaci[Loop_INDEX]); if (처리값 < 0) { 명령해석기.GREŠKA(처리값); break; } }
        Memorija_Datoteke.Zatvori(열린파일번호);
    }
    static int znamenka_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.token_COUNT) return -1;
        int unos_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.길이[argument_INDEX]; Loop_INDEX++) { int kodna_točka = 명령해석기.token_VALUE[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (kodna_točka < '0' || kodna_točka > '9' || unos_COUNT > 10000) return -1; unos_COUNT = unos_COUNT * 10 + kodna_točka - '0'; } return unos_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.REZULTAT = 2; 단말.Zapisuj("사용법: wc [-c|-l|-w] [Datoteka]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int bajt_COUNT = 0, 줄수 = 0, 낱말수 = 0, bajt_podaci; boolean 낱말 = false;
        while ((bajt_podaci = Čitaj()) >= 0 && bajt_podaci != 256) { bajt_COUNT++; if (bajt_podaci == 10) 줄수++; boolean Space = bajt_podaci == 32 || bajt_podaci >= 9 && bajt_podaci <= 13; if (!Space && !낱말) 낱말수++; 낱말 = !Space; }
        Zatvori(); if (bajt_podaci < 0) { 명령해석기.GREŠKA(bajt_podaci); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? bajt_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(bajt_COUNT); } 단말.문자(10);
    }
    static void FIND_unos() {
        if (명령해석기.token_COUNT < 2 || 명령해석기.token_COUNT > 3) { 명령해석기.REZULTAT = 2; 단말.Zapisuj("사용법: grep 찾을문구 [Datoteka]\n"); return; }
        if (!입력준비(2)) return;
        int unos_COUNT = 0, bajt_podaci, 일치수 = 0;
        while (true) {
            bajt_podaci = Čitaj();
            if (bajt_podaci == 10 || bajt_podaci == 256 || bajt_podaci < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= unos_COUNT - 명령해석기.길이[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int unutarnji_položaj = 0; unutarnji_položaj < 명령해석기.길이[1]; unutarnji_položaj++) if (podaci[Loop_INDEX + unutarnji_položaj] != 명령해석기.token_VALUE[명령해석기.시작점[1] + unutarnji_položaj]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (unos_COUNT > 0 || bajt_podaci == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) pano.직렬쓰기(podaci[Loop_INDEX]); 단말.문자(10); 일치수++; }
                unos_COUNT = 0; if (bajt_podaci != 10) break;
            } else if (unos_COUNT < podaci.length) podaci[unos_COUNT++] = bajt_podaci;
            else { 명령해석기.GREŠKA(-28); Zatvori(); return; }
        }
        Zatvori(); if (bajt_podaci < 0) 명령해석기.GREŠKA(bajt_podaci); else if (명령해석기.REZULTAT == 0) 명령해석기.REZULTAT = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = znamenka_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.REZULTAT = 2; 단말.Zapisuj("사용법: head/tail [-n 줄수] [Datoteka]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int unos_COUNT = 0, bajt_podaci;
        while ((bajt_podaci = Čitaj()) != 256 && bajt_podaci >= 0) { if (unos_COUNT == podaci.length) { 명령해석기.GREŠKA(-28); Zatvori(); return; } podaci[unos_COUNT++] = bajt_podaci; }
        Zatvori(); if (bajt_podaci < 0) { 명령해석기.GREŠKA(bajt_podaci); return; }
        int lokalno_START = 0, završiti_razgovor_položaj = unos_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int ukupni_zbroj_COUNT = 0; for (int Loop_INDEX = unos_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (podaci[Loop_INDEX] == 10 && ++ukupni_zbroj_COUNT == 줄수) { lokalno_START = Loop_INDEX + 1; break; } }
        else { int ukupni_zbroj_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) if (podaci[Loop_INDEX] == 10 && ++ukupni_zbroj_COUNT == 줄수) { završiti_razgovor_položaj = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokalno_START; Loop_INDEX < završiti_razgovor_položaj; Loop_INDEX++) pano.직렬쓰기(podaci[Loop_INDEX]);
    }
    static void zapisivanje_Zajedno() {
        boolean dodati = 명령해석기.같음(1, "-a"); int argument_INDEX = dodati ? 2 : 1;
        if (명령해석기.token_COUNT != argument_INDEX + 1) { 명령해석기.REZULTAT = 2; 단말.Zapisuj("사용법: tee [-a] Datoteka\n"); return; }
        int 열린파일번호 = otvoreno_Datoteka(argument_INDEX, dodati ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.GREŠKA(열린파일번호); return; }
        ulazna_datoteka = -1; int bajt_podaci;
        while ((bajt_podaci = Čitaj()) != 256 && bajt_podaci >= 0) { int 처리값 = Memorija_Datoteke.Zapisuj(열린파일번호, bajt_podaci); if (처리값 < 0) { 명령해석기.GREŠKA(처리값); break; } pano.직렬쓰기(bajt_podaci); }
        Memorija_Datoteke.Zatvori(열린파일번호);
    }
}
