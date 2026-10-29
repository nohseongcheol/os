// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 čaula 내장 Rīki. */
public final class čaula_Rīki {
    static int[] dati = new int[16384];
    static int ievades_fails = -1;
    static int atvērt_Fails(int arg_INDEX, int Process_MODE) {
        int 처리값 = 명령해석기.CEĻŠ(arg_INDEX); return 처리값 < 0 ? 처리값 : atmiņa_Faili.Atvērt(Process_MODE);
    }
    static boolean 입력준비(int arg_INDEX) {
        ievades_fails = -1;
        if (arg_INDEX < 명령해석기.daļiņa_COUNT) {
            ievades_fails = atvērt_Fails(arg_INDEX, 0);
            if (ievades_fails < 0) { 명령해석기.Kļūda(ievades_fails); return false; }
        }
        return true;
    }
    static int Lasīt() {
        if (ievades_fails >= 3) return atmiņa_Faili.Lasīt(ievades_fails);
        while (true) {
            int byte_dati = Panelis.직렬읽기(); if (byte_dati == -2 || byte_dati == 4) return 256;
            if (byte_dati == 3) { 명령해석기.mērs = 130; return 256; }
            if (byte_dati >= 0) return byte_dati; Panelis.YIELD_apstrādātājs();
        }
    }
    static void Aizvērt() { if (ievades_fails >= 3) atmiņa_Faili.Aizvērt(ievades_fails); ievades_fails = -1; }
    static void Skats_VALUE() {
        int 마지막자리 = 명령해석기.daļiņa_COUNT == 1 ? 2 : 명령해석기.daļiņa_COUNT;
        for (int arg_INDEX = 1; arg_INDEX < 마지막자리; arg_INDEX++) {
            if (!입력준비(arg_INDEX)) continue;
            int byte_dati; while ((byte_dati = Lasīt()) != 256 && byte_dati >= 0) Panelis.직렬쓰기(byte_dati);
            if (byte_dati < 0) 명령해석기.Kļūda(byte_dati); Aizvērt();
        }
    }
    static void Fails_Darbs(String darbība_numurs) {
        if (명령해석기.daļiņa_COUNT != 2) { 명령해석기.mērs = 2; 단말.Rakstīt("사용법: mkdir/rmdir/touch Fails\n"); return; }
        int 처리값 = 명령해석기.CEĻŠ(1);
        if (처리값 >= 0) {
            if (darbība_numurs.charAt(0) == 'm') 처리값 = atmiņa_Faili.atvērt_Direktorijs();
            else if (darbība_numurs.charAt(0) == 'r') 처리값 = atmiņa_Faili.noņemt_Direktorijs();
            else { 처리값 = atmiņa_Faili.Atvērt(65); if (처리값 >= 3) 처리값 = atmiņa_Faili.Aizvērt(처리값); }
        }
        if (처리값 < 0) 명령해석기.Kļūda(처리값);
    }
    static void kopēt_VALUE(boolean 이동여부) {
        if (명령해석기.daļiņa_COUNT != 3) { 명령해석기.mērs = 2; 단말.Rakstīt("사용법: cp/mv 원본 mērķis_dalībnieks (Fails)\n"); return; }
        int 처리값 = 명령해석기.CEĻŠ(1); if (처리값 >= 0) 처리값 = atmiņa_Faili.normalizēt_VALUE();
        if (처리값 < 0) { 명령해석기.Kļūda(처리값); return; }
        int 원본번호 = atmiņa_Faili.FIND_ievade(); if (원본번호 < 0) { 명령해석기.Kļūda(-2); return; }
        int ievade_COUNT = atmiņa_Faili.길이[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) dati[Loop_INDEX] = atmiņa_Faili.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.CEĻŠ(2); if (처리값 >= 0) 처리값 = atmiņa_Faili.normalizēt_VALUE();
        if (처리값 < 0) { 명령해석기.Kļūda(처리값); return; }
        if (atmiņa_Faili.FIND_ievade() == 원본번호) { if (!이동여부) 명령해석기.Kļūda(-22); return; }
        if (이동여부) { 처리값 = atmiņa_Faili.Pārdēvēt_ievade(원본번호); if (처리값 < 0) 명령해석기.Kļūda(처리값); return; }
        int 열린파일번호 = atmiņa_Faili.Atvērt(577); if (열린파일번호 < 0) { 명령해석기.Kļūda(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) { 처리값 = atmiņa_Faili.Rakstīt(열린파일번호, dati[Loop_INDEX]); if (처리값 < 0) { 명령해석기.Kļūda(처리값); break; } }
        atmiņa_Faili.Aizvērt(열린파일번호);
    }
    static int cipars_VALUE(int arg_INDEX) {
        if (arg_INDEX >= 명령해석기.daļiņa_COUNT) return -1;
        int ievade_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.길이[arg_INDEX]; Loop_INDEX++) { int koda_punkts = 명령해석기.daļiņa_VALUE[명령해석기.시작점[arg_INDEX] + Loop_INDEX]; if (koda_punkts < '0' || koda_punkts > '9' || ievade_COUNT > 10000) return -1; ievade_COUNT = ievade_COUNT * 10 + koda_punkts - '0'; } return ievade_COUNT;
    }
    static void 세기() {
        int arg_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; arg_INDEX++; }
        if (명령해석기.daļiņa_COUNT > arg_INDEX + 1) { 명령해석기.mērs = 2; 단말.Rakstīt("사용법: wc [-c|-l|-w] [Fails]\n"); return; }
        if (!입력준비(arg_INDEX)) return;
        int byte_COUNT = 0, 줄수 = 0, 낱말수 = 0, byte_dati; boolean 낱말 = false;
        while ((byte_dati = Lasīt()) >= 0 && byte_dati != 256) { byte_COUNT++; if (byte_dati == 10) 줄수++; boolean telpa = byte_dati == 32 || byte_dati >= 9 && byte_dati <= 13; if (!telpa && !낱말) 낱말수++; 낱말 = !telpa; }
        Aizvērt(); if (byte_dati < 0) { 명령해석기.Kļūda(byte_dati); return; }
        if (선택번호 != 0) 단말.numurs(선택번호 == 1 ? byte_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.numurs(줄수); 단말.문자(' '); 단말.numurs(낱말수); 단말.문자(' '); 단말.numurs(byte_COUNT); } 단말.문자(10);
    }
    static void FIND_ievade() {
        if (명령해석기.daļiņa_COUNT < 2 || 명령해석기.daļiņa_COUNT > 3) { 명령해석기.mērs = 2; 단말.Rakstīt("사용법: grep 찾을문구 [Fails]\n"); return; }
        if (!입력준비(2)) return;
        int ievade_COUNT = 0, byte_dati, 일치수 = 0;
        while (true) {
            byte_dati = Lasīt();
            if (byte_dati == 10 || byte_dati == 256 || byte_dati < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= ievade_COUNT - 명령해석기.길이[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int iekšējais_amats = 0; iekšējais_amats < 명령해석기.길이[1]; iekšējais_amats++) if (dati[Loop_INDEX + iekšējais_amats] != 명령해석기.daļiņa_VALUE[명령해석기.시작점[1] + iekšējais_amats]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (ievade_COUNT > 0 || byte_dati == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) Panelis.직렬쓰기(dati[Loop_INDEX]); 단말.문자(10); 일치수++; }
                ievade_COUNT = 0; if (byte_dati != 10) break;
            } else if (ievade_COUNT < dati.length) dati[ievade_COUNT++] = byte_dati;
            else { 명령해석기.Kļūda(-28); Aizvērt(); return; }
        }
        Aizvērt(); if (byte_dati < 0) 명령해석기.Kļūda(byte_dati); else if (명령해석기.mērs == 0) 명령해석기.mērs = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int arg_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = cipars_VALUE(2); arg_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.daļiņa_COUNT > arg_INDEX + 1) { 명령해석기.mērs = 2; 단말.Rakstīt("사용법: head/tail [-n 줄수] [Fails]\n"); return; }
        if (!입력준비(arg_INDEX)) return;
        int ievade_COUNT = 0, byte_dati;
        while ((byte_dati = Lasīt()) != 256 && byte_dati >= 0) { if (ievade_COUNT == dati.length) { 명령해석기.Kļūda(-28); Aizvērt(); return; } dati[ievade_COUNT++] = byte_dati; }
        Aizvērt(); if (byte_dati < 0) { 명령해석기.Kļūda(byte_dati); return; }
        int vietējs_Sākt = 0, beigt_zvanu_amats = ievade_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int kopsumma_COUNT = 0; for (int Loop_INDEX = ievade_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (dati[Loop_INDEX] == 10 && ++kopsumma_COUNT == 줄수) { vietējs_Sākt = Loop_INDEX + 1; break; } }
        else { int kopsumma_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < ievade_COUNT; Loop_INDEX++) if (dati[Loop_INDEX] == 10 && ++kopsumma_COUNT == 줄수) { beigt_zvanu_amats = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = vietējs_Sākt; Loop_INDEX < beigt_zvanu_amats; Loop_INDEX++) Panelis.직렬쓰기(dati[Loop_INDEX]);
    }
    static void rakstīšana_Kopā() {
        boolean Pievienot = 명령해석기.같음(1, "-a"); int arg_INDEX = Pievienot ? 2 : 1;
        if (명령해석기.daļiņa_COUNT != arg_INDEX + 1) { 명령해석기.mērs = 2; 단말.Rakstīt("사용법: tee [-a] Fails\n"); return; }
        int 열린파일번호 = atvērt_Fails(arg_INDEX, Pievienot ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Kļūda(열린파일번호); return; }
        ievades_fails = -1; int byte_dati;
        while ((byte_dati = Lasīt()) != 256 && byte_dati >= 0) { int 처리값 = atmiņa_Faili.Rakstīt(열린파일번호, byte_dati); if (처리값 < 0) { 명령해석기.Kļūda(처리값); break; } Panelis.직렬쓰기(byte_dati); }
        atmiņa_Faili.Aizvērt(열린파일번호);
    }
}
