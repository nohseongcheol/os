// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 ljuska 내장 Alati. */
public final class ljuska_Alati {
    static int[] podaci = new int[16384];
    static int 입력파일 = -1;
    static int kreirati_fajl(int argument_INDEX, int proces_mod) {
        int 처리값 = 명령해석기.Putanja(argument_INDEX); return 처리값 < 0 ? 처리값 : Memorija_Fajlovi.Otvori(proces_mod);
    }
    static boolean 입력준비(int argument_INDEX) {
        입력파일 = -1;
        if (argument_INDEX < 명령해석기.token_COUNT) {
            입력파일 = kreirati_fajl(argument_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.GRESKA(입력파일); return false; }
        }
        return true;
    }
    static int Čitaj() {
        if (입력파일 >= 3) return Memorija_Fajlovi.Čitaj(입력파일);
        while (true) {
            int bajt_podaci = ploča.직렬읽기(); if (bajt_podaci == -2 || bajt_podaci == 4) return 256;
            if (bajt_podaci == 3) { 명령해석기.mjera = 130; return 256; }
            if (bajt_podaci >= 0) return bajt_podaci; ploča.YIELD_CPU();
        }
    }
    static void Zatvori() { if (입력파일 >= 3) Memorija_Fajlovi.Zatvori(입력파일); 입력파일 = -1; }
    static void Prikaz_VALUE() {
        int 마지막자리 = 명령해석기.token_COUNT == 1 ? 2 : 명령해석기.token_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int bajt_podaci; while ((bajt_podaci = Čitaj()) != 256 && bajt_podaci >= 0) ploča.직렬쓰기(bajt_podaci);
            if (bajt_podaci < 0) 명령해석기.GRESKA(bajt_podaci); Zatvori();
        }
    }
    static void fajl_slučaj(String 동작번호) {
        if (명령해석기.token_COUNT != 2) { 명령해석기.mjera = 2; 단말.Piši("사용법: mkdir/rmdir/touch Fajl\n"); return; }
        int 처리값 = 명령해석기.Putanja(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memorija_Fajlovi.Create_Direktorij();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memorija_Fajlovi.ukloniti_Direktorij();
            else { 처리값 = Memorija_Fajlovi.Otvori(65); if (처리값 >= 3) 처리값 = Memorija_Fajlovi.Zatvori(처리값); }
        }
        if (처리값 < 0) 명령해석기.GRESKA(처리값);
    }
    static void instanca_VALUE(boolean 이동여부) {
        if (명령해석기.token_COUNT != 3) { 명령해석기.mjera = 2; 단말.Piši("사용법: cp/mv 원본 odredište_završna_tačka (Fajl)\n"); return; }
        int 처리값 = 명령해석기.Putanja(1); if (처리값 >= 0) 처리값 = Memorija_Fajlovi.normalizirati_VALUE();
        if (처리값 < 0) { 명령해석기.GRESKA(처리값); return; }
        int 원본번호 = Memorija_Fajlovi.FIND_unos(); if (원본번호 < 0) { 명령해석기.GRESKA(-2); return; }
        int unos_COUNT = Memorija_Fajlovi.dužina_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) podaci[Loop_INDEX] = Memorija_Fajlovi.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.Putanja(2); if (처리값 >= 0) 처리값 = Memorija_Fajlovi.normalizirati_VALUE();
        if (처리값 < 0) { 명령해석기.GRESKA(처리값); return; }
        if (Memorija_Fajlovi.FIND_unos() == 원본번호) { if (!이동여부) 명령해석기.GRESKA(-22); return; }
        if (이동여부) { 처리값 = Memorija_Fajlovi.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.GRESKA(처리값); return; }
        int 열린파일번호 = Memorija_Fajlovi.Otvori(577); if (열린파일번호 < 0) { 명령해석기.GRESKA(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) { 처리값 = Memorija_Fajlovi.Piši(열린파일번호, podaci[Loop_INDEX]); if (처리값 < 0) { 명령해석기.GRESKA(처리값); break; } }
        Memorija_Fajlovi.Zatvori(열린파일번호);
    }
    static int cifra_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.token_COUNT) return -1;
        int unos_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.dužina_VALUE[argument_INDEX]; Loop_INDEX++) { int kôd_znaka = 명령해석기.token_VALUE[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (kôd_znaka < '0' || kôd_znaka > '9' || unos_COUNT > 10000) return -1; unos_COUNT = unos_COUNT * 10 + kôd_znaka - '0'; } return unos_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.mjera = 2; 단말.Piši("사용법: wc [-c|-l|-w] [Fajl]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int bajt_COUNT = 0, 줄수 = 0, 낱말수 = 0, bajt_podaci; boolean 낱말 = false;
        while ((bajt_podaci = Čitaj()) >= 0 && bajt_podaci != 256) { bajt_COUNT++; if (bajt_podaci == 10) 줄수++; boolean prostor = bajt_podaci == 32 || bajt_podaci >= 9 && bajt_podaci <= 13; if (!prostor && !낱말) 낱말수++; 낱말 = !prostor; }
        Zatvori(); if (bajt_podaci < 0) { 명령해석기.GRESKA(bajt_podaci); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? bajt_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(bajt_COUNT); } 단말.문자(10);
    }
    static void FIND_unos() {
        if (명령해석기.token_COUNT < 2 || 명령해석기.token_COUNT > 3) { 명령해석기.mjera = 2; 단말.Piši("사용법: grep 찾을문구 [Fajl]\n"); return; }
        if (!입력준비(2)) return;
        int unos_COUNT = 0, bajt_podaci, 일치수 = 0;
        while (true) {
            bajt_podaci = Čitaj();
            if (bajt_podaci == 10 || bajt_podaci == 256 || bajt_podaci < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= unos_COUNT - 명령해석기.dužina_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int unutrašnje_spajanje_položaj = 0; unutrašnje_spajanje_položaj < 명령해석기.dužina_VALUE[1]; unutrašnje_spajanje_položaj++) if (podaci[Loop_INDEX + unutrašnje_spajanje_položaj] != 명령해석기.token_VALUE[명령해석기.시작점[1] + unutrašnje_spajanje_položaj]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (unos_COUNT > 0 || bajt_podaci == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) ploča.직렬쓰기(podaci[Loop_INDEX]); 단말.문자(10); 일치수++; }
                unos_COUNT = 0; if (bajt_podaci != 10) break;
            } else if (unos_COUNT < podaci.length) podaci[unos_COUNT++] = bajt_podaci;
            else { 명령해석기.GRESKA(-28); Zatvori(); return; }
        }
        Zatvori(); if (bajt_podaci < 0) 명령해석기.GRESKA(bajt_podaci); else if (명령해석기.mjera == 0) 명령해석기.mjera = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = cifra_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.mjera = 2; 단말.Piši("사용법: head/tail [-n 줄수] [Fajl]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int unos_COUNT = 0, bajt_podaci;
        while ((bajt_podaci = Čitaj()) != 256 && bajt_podaci >= 0) { if (unos_COUNT == podaci.length) { 명령해석기.GRESKA(-28); Zatvori(); return; } podaci[unos_COUNT++] = bajt_podaci; }
        Zatvori(); if (bajt_podaci < 0) { 명령해석기.GRESKA(bajt_podaci); return; }
        int lokalni_START = 0, završiti_položaj = unos_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = unos_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (podaci[Loop_INDEX] == 10 && ++총수 == 줄수) { lokalni_START = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < unos_COUNT; Loop_INDEX++) if (podaci[Loop_INDEX] == 10 && ++총수 == 줄수) { završiti_položaj = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokalni_START; Loop_INDEX < završiti_položaj; Loop_INDEX++) ploča.직렬쓰기(podaci[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argument_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.token_COUNT != argument_INDEX + 1) { 명령해석기.mjera = 2; 단말.Piši("사용법: tee [-a] Fajl\n"); return; }
        int 열린파일번호 = kreirati_fajl(argument_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.GRESKA(열린파일번호); return; }
        입력파일 = -1; int bajt_podaci;
        while ((bajt_podaci = Čitaj()) != 256 && bajt_podaci >= 0) { int 처리값 = Memorija_Fajlovi.Piši(열린파일번호, bajt_podaci); if (처리값 < 0) { 명령해석기.GRESKA(처리값); break; } ploča.직렬쓰기(bajt_podaci); }
        Memorija_Fajlovi.Zatvori(열린파일번호);
    }
}
