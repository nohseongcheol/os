// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 lupina 내장 Orodja. */
public final class lupina_Orodja {
    static int[] podatki = new int[16384];
    static int vhodna_datoteka = -1;
    static int odprto_Datoteka(int argument_INDEX, int Proces_MODE) {
        int 처리값 = 명령해석기.POT(argument_INDEX); return 처리값 < 0 ? 처리값 : pomnilnik_Datoteke.Odpri(Proces_MODE);
    }
    static boolean 입력준비(int argument_INDEX) {
        vhodna_datoteka = -1;
        if (argument_INDEX < 명령해석기.žeton_COUNT) {
            vhodna_datoteka = odprto_Datoteka(argument_INDEX, 0);
            if (vhodna_datoteka < 0) { 명령해석기.NAPAKA(vhodna_datoteka); return false; }
        }
        return true;
    }
    static int Branje() {
        if (vhodna_datoteka >= 3) return pomnilnik_Datoteke.Branje(vhodna_datoteka);
        while (true) {
            int bajt_podatki = Tabla.직렬읽기(); if (bajt_podatki == -2 || bajt_podatki == 4) return 256;
            if (bajt_podatki == 3) { 명령해석기.REZULTAT = 130; return 256; }
            if (bajt_podatki >= 0) return bajt_podatki; Tabla.YIELD_CPE();
        }
    }
    static void Zapri() { if (vhodna_datoteka >= 3) pomnilnik_Datoteke.Zapri(vhodna_datoteka); vhodna_datoteka = -1; }
    static void Pogled_VALUE() {
        int 마지막자리 = 명령해석기.žeton_COUNT == 1 ? 2 : 명령해석기.žeton_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int bajt_podatki; while ((bajt_podatki = Branje()) != 256 && bajt_podatki >= 0) Tabla.직렬쓰기(bajt_podatki);
            if (bajt_podatki < 0) 명령해석기.NAPAKA(bajt_podatki); Zapri();
        }
    }
    static void Datoteka_posel(String 동작번호) {
        if (명령해석기.žeton_COUNT != 2) { 명령해석기.REZULTAT = 2; 단말.Pisanje("사용법: mkdir/rmdir/touch Datoteka\n"); return; }
        int 처리값 = 명령해석기.POT(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = pomnilnik_Datoteke.Ustvari_Imenik();
            else if (동작번호.charAt(0) == 'r') 처리값 = pomnilnik_Datoteke.odstraniti_Imenik();
            else { 처리값 = pomnilnik_Datoteke.Odpri(65); if (처리값 >= 3) 처리값 = pomnilnik_Datoteke.Zapri(처리값); }
        }
        if (처리값 < 0) 명령해석기.NAPAKA(처리값);
    }
    static void kopirati_VALUE(boolean 이동여부) {
        if (명령해석기.žeton_COUNT != 3) { 명령해석기.REZULTAT = 2; 단말.Pisanje("사용법: cp/mv 원본 cilj_končna_točka (Datoteka)\n"); return; }
        int 처리값 = 명령해석기.POT(1); if (처리값 >= 0) 처리값 = pomnilnik_Datoteke.normalizirati_VALUE();
        if (처리값 < 0) { 명령해석기.NAPAKA(처리값); return; }
        int 원본번호 = pomnilnik_Datoteke.FIND_vnos(); if (원본번호 < 0) { 명령해석기.NAPAKA(-2); return; }
        int vnos_COUNT = pomnilnik_Datoteke.길이[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) podatki[Loop_INDEX] = pomnilnik_Datoteke.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.POT(2); if (처리값 >= 0) 처리값 = pomnilnik_Datoteke.normalizirati_VALUE();
        if (처리값 < 0) { 명령해석기.NAPAKA(처리값); return; }
        if (pomnilnik_Datoteke.FIND_vnos() == 원본번호) { if (!이동여부) 명령해석기.NAPAKA(-22); return; }
        if (이동여부) { 처리값 = pomnilnik_Datoteke.Preimenuj_vnos(원본번호); if (처리값 < 0) 명령해석기.NAPAKA(처리값); return; }
        int 열린파일번호 = pomnilnik_Datoteke.Odpri(577); if (열린파일번호 < 0) { 명령해석기.NAPAKA(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) { 처리값 = pomnilnik_Datoteke.Pisanje(열린파일번호, podatki[Loop_INDEX]); if (처리값 < 0) { 명령해석기.NAPAKA(처리값); break; } }
        pomnilnik_Datoteke.Zapri(열린파일번호);
    }
    static int številka_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.žeton_COUNT) return -1;
        int vnos_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.길이[argument_INDEX]; Loop_INDEX++) { int koda_znaka = 명령해석기.žeton_VALUE[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (koda_znaka < '0' || koda_znaka > '9' || vnos_COUNT > 10000) return -1; vnos_COUNT = vnos_COUNT * 10 + koda_znaka - '0'; } return vnos_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.žeton_COUNT > argument_INDEX + 1) { 명령해석기.REZULTAT = 2; 단말.Pisanje("사용법: wc [-c|-l|-w] [Datoteka]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int bajt_COUNT = 0, 줄수 = 0, 낱말수 = 0, bajt_podatki; boolean 낱말 = false;
        while ((bajt_podatki = Branje()) >= 0 && bajt_podatki != 256) { bajt_COUNT++; if (bajt_podatki == 10) 줄수++; boolean Space = bajt_podatki == 32 || bajt_podatki >= 9 && bajt_podatki <= 13; if (!Space && !낱말) 낱말수++; 낱말 = !Space; }
        Zapri(); if (bajt_podatki < 0) { 명령해석기.NAPAKA(bajt_podatki); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? bajt_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(bajt_COUNT); } 단말.문자(10);
    }
    static void FIND_vnos() {
        if (명령해석기.žeton_COUNT < 2 || 명령해석기.žeton_COUNT > 3) { 명령해석기.REZULTAT = 2; 단말.Pisanje("사용법: grep 찾을문구 [Datoteka]\n"); return; }
        if (!입력준비(2)) return;
        int vnos_COUNT = 0, bajt_podatki, 일치수 = 0;
        while (true) {
            bajt_podatki = Branje();
            if (bajt_podatki == 10 || bajt_podatki == 256 || bajt_podatki < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= vnos_COUNT - 명령해석기.길이[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int notranje_položaj = 0; notranje_položaj < 명령해석기.길이[1]; notranje_položaj++) if (podatki[Loop_INDEX + notranje_položaj] != 명령해석기.žeton_VALUE[명령해석기.시작점[1] + notranje_položaj]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (vnos_COUNT > 0 || bajt_podatki == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) Tabla.직렬쓰기(podatki[Loop_INDEX]); 단말.문자(10); 일치수++; }
                vnos_COUNT = 0; if (bajt_podatki != 10) break;
            } else if (vnos_COUNT < podatki.length) podatki[vnos_COUNT++] = bajt_podatki;
            else { 명령해석기.NAPAKA(-28); Zapri(); return; }
        }
        Zapri(); if (bajt_podatki < 0) 명령해석기.NAPAKA(bajt_podatki); else if (명령해석기.REZULTAT == 0) 명령해석기.REZULTAT = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = številka_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.žeton_COUNT > argument_INDEX + 1) { 명령해석기.REZULTAT = 2; 단말.Pisanje("사용법: head/tail [-n 줄수] [Datoteka]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int vnos_COUNT = 0, bajt_podatki;
        while ((bajt_podatki = Branje()) != 256 && bajt_podatki >= 0) { if (vnos_COUNT == podatki.length) { 명령해석기.NAPAKA(-28); Zapri(); return; } podatki[vnos_COUNT++] = bajt_podatki; }
        Zapri(); if (bajt_podatki < 0) { 명령해석기.NAPAKA(bajt_podatki); return; }
        int lokalen_krajeven_Start = 0, končati_klic_položaj = vnos_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int skupaj_COUNT = 0; for (int Loop_INDEX = vnos_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (podatki[Loop_INDEX] == 10 && ++skupaj_COUNT == 줄수) { lokalen_krajeven_Start = Loop_INDEX + 1; break; } }
        else { int skupaj_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < vnos_COUNT; Loop_INDEX++) if (podatki[Loop_INDEX] == 10 && ++skupaj_COUNT == 줄수) { končati_klic_položaj = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokalen_krajeven_Start; Loop_INDEX < končati_klic_položaj; Loop_INDEX++) Tabla.직렬쓰기(podatki[Loop_INDEX]);
    }
    static void pisati_Skupaj() {
        boolean dodati = 명령해석기.같음(1, "-a"); int argument_INDEX = dodati ? 2 : 1;
        if (명령해석기.žeton_COUNT != argument_INDEX + 1) { 명령해석기.REZULTAT = 2; 단말.Pisanje("사용법: tee [-a] Datoteka\n"); return; }
        int 열린파일번호 = odprto_Datoteka(argument_INDEX, dodati ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.NAPAKA(열린파일번호); return; }
        vhodna_datoteka = -1; int bajt_podatki;
        while ((bajt_podatki = Branje()) != 256 && bajt_podatki >= 0) { int 처리값 = pomnilnik_Datoteke.Pisanje(열린파일번호, bajt_podatki); if (처리값 < 0) { 명령해석기.NAPAKA(처리값); break; } Tabla.직렬쓰기(bajt_podatki); }
        pomnilnik_Datoteke.Zapri(열린파일번호);
    }
}
