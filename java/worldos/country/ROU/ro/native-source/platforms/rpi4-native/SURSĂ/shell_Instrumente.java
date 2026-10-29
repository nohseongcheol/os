// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 shell 내장 Instrumente. */
public final class shell_Instrumente {
    static int[] date = new int[16384];
    static int fișier_de_intrare = -1;
    static int crea_Fișier(int argument_INDEX, int Proces_mod) {
        int 처리값 = 명령해석기.Cale(argument_INDEX); return 처리값 < 0 ? 처리값 : Memorie_Fișiere.Deschide(Proces_mod);
    }
    static boolean 입력준비(int argument_INDEX) {
        fișier_de_intrare = -1;
        if (argument_INDEX < 명령해석기.token_COUNT) {
            fișier_de_intrare = crea_Fișier(argument_INDEX, 0);
            if (fișier_de_intrare < 0) { 명령해석기.eroare(fișier_de_intrare); return false; }
        }
        return true;
    }
    static int Citire() {
        if (fișier_de_intrare >= 3) return Memorie_Fișiere.Citire(fișier_de_intrare);
        while (true) {
            int byte_date = Avizier.직렬읽기(); if (byte_date == -2 || byte_date == 4) return 256;
            if (byte_date == 3) { 명령해석기.KR = 130; return 256; }
            if (byte_date >= 0) return byte_date; Avizier.YIELD_CPU();
        }
    }
    static void Închide() { if (fișier_de_intrare >= 3) Memorie_Fișiere.Închide(fișier_de_intrare); fișier_de_intrare = -1; }
    static void vizualiza_VALUE() {
        int 마지막자리 = 명령해석기.token_COUNT == 1 ? 2 : 명령해석기.token_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int byte_date; while ((byte_date = Citire()) != 256 && byte_date >= 0) Avizier.직렬쓰기(byte_date);
            if (byte_date < 0) 명령해석기.eroare(byte_date); Închide();
        }
    }
    static void Fișier_caz(String 동작번호) {
        if (명령해석기.token_COUNT != 2) { 명령해석기.KR = 2; 단말.Scriere("사용법: mkdir/rmdir/touch Fișier\n"); return; }
        int 처리값 = 명령해석기.Cale(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memorie_Fișiere.crea_Director();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memorie_Fișiere.elimina_Director();
            else { 처리값 = Memorie_Fișiere.Deschide(65); if (처리값 >= 3) 처리값 = Memorie_Fișiere.Închide(처리값); }
        }
        if (처리값 < 0) 명령해석기.eroare(처리값);
    }
    static void copia_VALUE(boolean 이동여부) {
        if (명령해석기.token_COUNT != 3) { 명령해석기.KR = 2; 단말.Scriere("사용법: cp/mv 원본 destinație_participant (Fișier)\n"); return; }
        int 처리값 = 명령해석기.Cale(1); if (처리값 >= 0) 처리값 = Memorie_Fișiere.normaliza_VALUE();
        if (처리값 < 0) { 명령해석기.eroare(처리값); return; }
        int 원본번호 = Memorie_Fișiere.FIND_intrare(); if (원본번호 < 0) { 명령해석기.eroare(-2); return; }
        int intrare_COUNT = Memorie_Fișiere.lungime_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) date[Loop_INDEX] = Memorie_Fișiere.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.Cale(2); if (처리값 >= 0) 처리값 = Memorie_Fișiere.normaliza_VALUE();
        if (처리값 < 0) { 명령해석기.eroare(처리값); return; }
        if (Memorie_Fișiere.FIND_intrare() == 원본번호) { if (!이동여부) 명령해석기.eroare(-22); return; }
        if (이동여부) { 처리값 = Memorie_Fișiere.Redenumire_intrare(원본번호); if (처리값 < 0) 명령해석기.eroare(처리값); return; }
        int 열린파일번호 = Memorie_Fișiere.Deschide(577); if (열린파일번호 < 0) { 명령해석기.eroare(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) { 처리값 = Memorie_Fișiere.Scriere(열린파일번호, date[Loop_INDEX]); if (처리값 < 0) { 명령해석기.eroare(처리값); break; } }
        Memorie_Fișiere.Închide(열린파일번호);
    }
    static int cifră_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.token_COUNT) return -1;
        int intrare_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.lungime_VALUE[argument_INDEX]; Loop_INDEX++) { int cod_caracter = 명령해석기.token_VALUE[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (cod_caracter < '0' || cod_caracter > '9' || intrare_COUNT > 10000) return -1; intrare_COUNT = intrare_COUNT * 10 + cod_caracter - '0'; } return intrare_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.KR = 2; 단말.Scriere("사용법: wc [-c|-l|-w] [Fișier]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int byte_COUNT = 0, 줄수 = 0, 낱말수 = 0, byte_date; boolean 낱말 = false;
        while ((byte_date = Citire()) >= 0 && byte_date != 256) { byte_COUNT++; if (byte_date == 10) 줄수++; boolean SPAȚIU = byte_date == 32 || byte_date >= 9 && byte_date <= 13; if (!SPAȚIU && !낱말) 낱말수++; 낱말 = !SPAȚIU; }
        Închide(); if (byte_date < 0) { 명령해석기.eroare(byte_date); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? byte_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(byte_COUNT); } 단말.문자(10);
    }
    static void FIND_intrare() {
        if (명령해석기.token_COUNT < 2 || 명령해석기.token_COUNT > 3) { 명령해석기.KR = 2; 단말.Scriere("사용법: grep 찾을문구 [Fișier]\n"); return; }
        if (!입력준비(2)) return;
        int intrare_COUNT = 0, byte_date, 일치수 = 0;
        while (true) {
            byte_date = Citire();
            if (byte_date == 10 || byte_date == 256 || byte_date < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= intrare_COUNT - 명령해석기.lungime_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int internă_poziție = 0; internă_poziție < 명령해석기.lungime_VALUE[1]; internă_poziție++) if (date[Loop_INDEX + internă_poziție] != 명령해석기.token_VALUE[명령해석기.시작점[1] + internă_poziție]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (intrare_COUNT > 0 || byte_date == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) Avizier.직렬쓰기(date[Loop_INDEX]); 단말.문자(10); 일치수++; }
                intrare_COUNT = 0; if (byte_date != 10) break;
            } else if (intrare_COUNT < date.length) date[intrare_COUNT++] = byte_date;
            else { 명령해석기.eroare(-28); Închide(); return; }
        }
        Închide(); if (byte_date < 0) 명령해석기.eroare(byte_date); else if (명령해석기.KR == 0) 명령해석기.KR = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = cifră_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.KR = 2; 단말.Scriere("사용법: head/tail [-n 줄수] [Fișier]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int intrare_COUNT = 0, byte_date;
        while ((byte_date = Citire()) != 256 && byte_date >= 0) { if (intrare_COUNT == date.length) { 명령해석기.eroare(-28); Închide(); return; } date[intrare_COUNT++] = byte_date; }
        Închide(); if (byte_date < 0) { 명령해석기.eroare(byte_date); return; }
        int local_buta = 0, termina_un_apel_poziție = intrare_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int total_COUNT = 0; for (int Loop_INDEX = intrare_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (date[Loop_INDEX] == 10 && ++total_COUNT == 줄수) { local_buta = Loop_INDEX + 1; break; } }
        else { int total_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) if (date[Loop_INDEX] == 10 && ++total_COUNT == 줄수) { termina_un_apel_poziție = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = local_buta; Loop_INDEX < termina_un_apel_poziție; Loop_INDEX++) Avizier.직렬쓰기(date[Loop_INDEX]);
    }
    static void scriere_Împreună() {
        boolean adăuga = 명령해석기.같음(1, "-a"); int argument_INDEX = adăuga ? 2 : 1;
        if (명령해석기.token_COUNT != argument_INDEX + 1) { 명령해석기.KR = 2; 단말.Scriere("사용법: tee [-a] Fișier\n"); return; }
        int 열린파일번호 = crea_Fișier(argument_INDEX, adăuga ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.eroare(열린파일번호); return; }
        fișier_de_intrare = -1; int byte_date;
        while ((byte_date = Citire()) != 256 && byte_date >= 0) { int 처리값 = Memorie_Fișiere.Scriere(열린파일번호, byte_date); if (처리값 < 0) { 명령해석기.eroare(처리값); break; } Avizier.직렬쓰기(byte_date); }
        Memorie_Fișiere.Închide(열린파일번호);
    }
}
