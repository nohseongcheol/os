// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 grensesnitt 내장 Verktøy. */
public final class grensesnitt_Verktøy {
    static int[] data = new int[16384];
    static int 입력파일 = -1;
    static int opne_fil(int argument_INDEX, int Prosess_MODE) {
        int 처리값 = 명령해석기.STIGE(argument_INDEX); return 처리값 < 0 ? 처리값 : Minne_Filer.Opna(Prosess_MODE);
    }
    static boolean 입력준비(int argument_INDEX) {
        입력파일 = -1;
        if (argument_INDEX < 명령해석기.token_COUNT) {
            입력파일 = opne_fil(argument_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.FEIL(입력파일); return false; }
        }
        return true;
    }
    static int Les() {
        if (입력파일 >= 3) return Minne_Filer.Les(입력파일);
        while (true) {
            int byte_data = Tavle.직렬읽기(); if (byte_data == -2 || byte_data == 4) return 256;
            if (byte_data == 3) { 명령해석기.forretningsmål = 130; return 256; }
            if (byte_data >= 0) return byte_data; Tavle.YIELD_CPU();
        }
    }
    static void Lukk() { if (입력파일 >= 3) Minne_Filer.Lukk(입력파일); 입력파일 = -1; }
    static void vise_VALUE() {
        int 마지막자리 = 명령해석기.token_COUNT == 1 ? 2 : 명령해석기.token_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int byte_data; while ((byte_data = Les()) != 256 && byte_data >= 0) Tavle.직렬쓰기(byte_data);
            if (byte_data < 0) 명령해석기.FEIL(byte_data); Lukk();
        }
    }
    static void fil_sak(String 동작번호) {
        if (명령해석기.token_COUNT != 2) { 명령해석기.forretningsmål = 2; 단말.Skriv("사용법: mkdir/rmdir/touch Fil\n"); return; }
        int 처리값 = 명령해석기.STIGE(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Minne_Filer.Opprett_katalog();
            else if (동작번호.charAt(0) == 'r') 처리값 = Minne_Filer.fjerne_katalog();
            else { 처리값 = Minne_Filer.Opna(65); if (처리값 >= 3) 처리값 = Minne_Filer.Lukk(처리값); }
        }
        if (처리값 < 0) 명령해석기.FEIL(처리값);
    }
    static void kopiere_VALUE(boolean 이동여부) {
        if (명령해석기.token_COUNT != 3) { 명령해석기.forretningsmål = 2; 단말.Skriv("사용법: cp/mv 원본 mål_endepunkt (Fil)\n"); return; }
        int 처리값 = 명령해석기.STIGE(1); if (처리값 >= 0) 처리값 = Minne_Filer.normalisere_VALUE();
        if (처리값 < 0) { 명령해석기.FEIL(처리값); return; }
        int 원본번호 = Minne_Filer.Søk_oppføring(); if (원본번호 < 0) { 명령해석기.FEIL(-2); return; }
        int oppføring_COUNT = Minne_Filer.lengd_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) data[Loop_INDEX] = Minne_Filer.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.STIGE(2); if (처리값 >= 0) 처리값 = Minne_Filer.normalisere_VALUE();
        if (처리값 < 0) { 명령해석기.FEIL(처리값); return; }
        if (Minne_Filer.Søk_oppføring() == 원본번호) { if (!이동여부) 명령해석기.FEIL(-22); return; }
        if (이동여부) { 처리값 = Minne_Filer.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.FEIL(처리값); return; }
        int 열린파일번호 = Minne_Filer.Opna(577); if (열린파일번호 < 0) { 명령해석기.FEIL(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) { 처리값 = Minne_Filer.Skriv(열린파일번호, data[Loop_INDEX]); if (처리값 < 0) { 명령해석기.FEIL(처리값); break; } }
        Minne_Filer.Lukk(열린파일번호);
    }
    static int siffer_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.token_COUNT) return -1;
        int oppføring_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.lengd_VALUE[argument_INDEX]; Loop_INDEX++) { int teiknkode = 명령해석기.token_VALUE[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (teiknkode < '0' || teiknkode > '9' || oppføring_COUNT > 10000) return -1; oppføring_COUNT = oppføring_COUNT * 10 + teiknkode - '0'; } return oppføring_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.forretningsmål = 2; 단말.Skriv("사용법: wc [-c|-l|-w] [Fil]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int byte_COUNT = 0, 줄수 = 0, 낱말수 = 0, byte_data; boolean 낱말 = false;
        while ((byte_data = Les()) >= 0 && byte_data != 256) { byte_COUNT++; if (byte_data == 10) 줄수++; boolean område = byte_data == 32 || byte_data >= 9 && byte_data <= 13; if (!område && !낱말) 낱말수++; 낱말 = !område; }
        Lukk(); if (byte_data < 0) { 명령해석기.FEIL(byte_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? byte_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(byte_COUNT); } 단말.문자(10);
    }
    static void Søk_oppføring() {
        if (명령해석기.token_COUNT < 2 || 명령해석기.token_COUNT > 3) { 명령해석기.forretningsmål = 2; 단말.Skriv("사용법: grep 찾을문구 [Fil]\n"); return; }
        if (!입력준비(2)) return;
        int oppføring_COUNT = 0, byte_data, 일치수 = 0;
        while (true) {
            byte_data = Les();
            if (byte_data == 10 || byte_data == 256 || byte_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= oppføring_COUNT - 명령해석기.lengd_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int indre_kopling_plassere = 0; indre_kopling_plassere < 명령해석기.lengd_VALUE[1]; indre_kopling_plassere++) if (data[Loop_INDEX + indre_kopling_plassere] != 명령해석기.token_VALUE[명령해석기.시작점[1] + indre_kopling_plassere]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (oppføring_COUNT > 0 || byte_data == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) Tavle.직렬쓰기(data[Loop_INDEX]); 단말.문자(10); 일치수++; }
                oppføring_COUNT = 0; if (byte_data != 10) break;
            } else if (oppføring_COUNT < data.length) data[oppføring_COUNT++] = byte_data;
            else { 명령해석기.FEIL(-28); Lukk(); return; }
        }
        Lukk(); if (byte_data < 0) 명령해석기.FEIL(byte_data); else if (명령해석기.forretningsmål == 0) 명령해석기.forretningsmål = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = siffer_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.token_COUNT > argument_INDEX + 1) { 명령해석기.forretningsmål = 2; 단말.Skriv("사용법: head/tail [-n 줄수] [Fil]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int oppføring_COUNT = 0, byte_data;
        while ((byte_data = Les()) != 256 && byte_data >= 0) { if (oppføring_COUNT == data.length) { 명령해석기.FEIL(-28); Lukk(); return; } data[oppføring_COUNT++] = byte_data; }
        Lukk(); if (byte_data < 0) { 명령해석기.FEIL(byte_data); return; }
        int lokal_START = 0, avslutte_plassere = oppføring_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = oppføring_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { lokal_START = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < oppføring_COUNT; Loop_INDEX++) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { avslutte_plassere = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokal_START; Loop_INDEX < avslutte_plassere; Loop_INDEX++) Tavle.직렬쓰기(data[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argument_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.token_COUNT != argument_INDEX + 1) { 명령해석기.forretningsmål = 2; 단말.Skriv("사용법: tee [-a] Fil\n"); return; }
        int 열린파일번호 = opne_fil(argument_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.FEIL(열린파일번호); return; }
        입력파일 = -1; int byte_data;
        while ((byte_data = Les()) != 256 && byte_data >= 0) { int 처리값 = Minne_Filer.Skriv(열린파일번호, byte_data); if (처리값 < 0) { 명령해석기.FEIL(처리값); break; } Tavle.직렬쓰기(byte_data); }
        Minne_Filer.Lukk(열린파일번호);
    }
}
