// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 Shell 내장 Værktøjer. */
public final class Shell_Værktøjer {
    static int[] data = new int[16384];
    static int inputfil = -1;
    static int åben_fil(int argument_INDEKS, int Proces_HYPPIGST) {
        int 처리값 = 명령해석기.Sti(argument_INDEKS); return 처리값 < 0 ? 처리값 : Hukommelse_Filer.Åbn(Proces_HYPPIGST);
    }
    static boolean Tilrettelæg_input(int argument_INDEKS) {
        inputfil = -1;
        if (argument_INDEKS < 명령해석기.token_TÆL) {
            inputfil = åben_fil(argument_INDEKS, 0);
            if (inputfil < 0) { 명령해석기.fejl(inputfil); return false; }
        }
        return true;
    }
    static int Læse() {
        if (inputfil >= 3) return Hukommelse_Filer.Læse(inputfil);
        while (true) {
            int byte_data = Tavle.직렬읽기(); if (byte_data == -2 || byte_data == 4) return 256;
            if (byte_data == 3) { 명령해석기.KR = 130; return 256; }
            if (byte_data >= 0) return byte_data; Tavle.AFKAST_CPU();
        }
    }
    static void Luk() { if (inputfil >= 3) Hukommelse_Filer.Luk(inputfil); inputfil = -1; }
    static void Visning_VÆRDI() {
        int 마지막자리 = 명령해석기.token_TÆL == 1 ? 2 : 명령해석기.token_TÆL;
        for (int argument_INDEKS = 1; argument_INDEKS < 마지막자리; argument_INDEKS++) {
            if (!Tilrettelæg_input(argument_INDEKS)) continue;
            int byte_data; while ((byte_data = Læse()) != 256 && byte_data >= 0) Tavle.직렬쓰기(byte_data);
            if (byte_data < 0) 명령해석기.fejl(byte_data); Luk();
        }
    }
    static void fil_job(String To_do_tal) {
        if (명령해석기.token_TÆL != 2) { 명령해석기.KR = 2; 단말.Skrive("사용법: mkdir/rmdir/touch Fil\n"); return; }
        int 처리값 = 명령해석기.Sti(1);
        if (처리값 >= 0) {
            if (To_do_tal.charAt(0) == 'm') 처리값 = Hukommelse_Filer.åbne_mappe();
            else if (To_do_tal.charAt(0) == 'r') 처리값 = Hukommelse_Filer.fjerne_mappe();
            else { 처리값 = Hukommelse_Filer.Åbn(65); if (처리값 >= 3) 처리값 = Hukommelse_Filer.Luk(처리값); }
        }
        if (처리값 < 0) 명령해석기.fejl(처리값);
    }
    static void kopiere_VÆRDI(boolean 이동여부) {
        if (명령해석기.token_TÆL != 3) { 명령해석기.KR = 2; 단말.Skrive("사용법: cp/mv 원본 destination_slutpunkt (Fil)\n"); return; }
        int 처리값 = 명령해석기.Sti(1); if (처리값 >= 0) 처리값 = Hukommelse_Filer.normalisere_VÆRDI();
        if (처리값 < 0) { 명령해석기.fejl(처리값); return; }
        int 원본번호 = Hukommelse_Filer.Søg_post(); if (원본번호 < 0) { 명령해석기.fejl(-2); return; }
        int post_TÆL_8f7753a1 = Hukommelse_Filer.varighed_VÆRDI[원본번호]; for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) data[Loop_INDEKS] = Hukommelse_Filer.자료읽기(원본번호, Loop_INDEKS);
        처리값 = 명령해석기.Sti(2); if (처리값 >= 0) 처리값 = Hukommelse_Filer.normalisere_VÆRDI();
        if (처리값 < 0) { 명령해석기.fejl(처리값); return; }
        if (Hukommelse_Filer.Søg_post() == 원본번호) { if (!이동여부) 명령해석기.fejl(-22); return; }
        if (이동여부) { 처리값 = Hukommelse_Filer.Omdøb_post(원본번호); if (처리값 < 0) 명령해석기.fejl(처리값); return; }
        int 열린파일번호 = Hukommelse_Filer.Åbn(577); if (열린파일번호 < 0) { 명령해석기.fejl(열린파일번호); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) { 처리값 = Hukommelse_Filer.Skrive(열린파일번호, data[Loop_INDEKS]); if (처리값 < 0) { 명령해석기.fejl(처리값); break; } }
        Hukommelse_Filer.Luk(열린파일번호);
    }
    static int ciffer_VÆRDI(int argument_INDEKS) {
        if (argument_INDEKS >= 명령해석기.token_TÆL) return -1;
        int post_TÆL_8f7753a1 = 0; for (int Loop_INDEKS = 0; Loop_INDEKS < 명령해석기.varighed_VÆRDI[argument_INDEKS]; Loop_INDEKS++) { int tegnkode = 명령해석기.token_VÆRDI[명령해석기.시작점[argument_INDEKS] + Loop_INDEKS]; if (tegnkode < '0' || tegnkode > '9' || post_TÆL_8f7753a1 > 10000) return -1; post_TÆL_8f7753a1 = post_TÆL_8f7753a1 * 10 + tegnkode - '0'; } return post_TÆL_8f7753a1;
    }
    static void 세기() {
        int argument_INDEKS = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEKS++; }
        if (명령해석기.token_TÆL > argument_INDEKS + 1) { 명령해석기.KR = 2; 단말.Skrive("사용법: wc [-c|-l|-w] [Fil]\n"); return; }
        if (!Tilrettelæg_input(argument_INDEKS)) return;
        int byte_TÆL = 0, 줄수 = 0, 낱말수 = 0, byte_data; boolean 낱말 = false;
        while ((byte_data = Læse()) >= 0 && byte_data != 256) { byte_TÆL++; if (byte_data == 10) 줄수++; boolean Space = byte_data == 32 || byte_data >= 9 && byte_data <= 13; if (!Space && !낱말) 낱말수++; 낱말 = !Space; }
        Luk(); if (byte_data < 0) { 명령해석기.fejl(byte_data); return; }
        if (선택번호 != 0) 단말.tal(선택번호 == 1 ? byte_TÆL : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.tal(줄수); 단말.문자(' '); 단말.tal(낱말수); 단말.문자(' '); 단말.tal(byte_TÆL); } 단말.문자(10);
    }
    static void Søg_post() {
        if (명령해석기.token_TÆL < 2 || 명령해석기.token_TÆL > 3) { 명령해석기.KR = 2; 단말.Skrive("사용법: grep 찾을문구 [Fil]\n"); return; }
        if (!Tilrettelæg_input(2)) return;
        int post_TÆL_8f7753a1 = 0, byte_data, 일치수 = 0;
        while (true) {
            byte_data = Læse();
            if (byte_data == 10 || byte_data == 256 || byte_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEKS = 0; Loop_INDEKS <= post_TÆL_8f7753a1 - 명령해석기.varighed_VÆRDI[1]; Loop_INDEKS++) {
                    boolean 같은여부 = true; for (int indre_placere = 0; indre_placere < 명령해석기.varighed_VÆRDI[1]; indre_placere++) if (data[Loop_INDEKS + indre_placere] != 명령해석기.token_VÆRDI[명령해석기.시작점[1] + indre_placere]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (post_TÆL_8f7753a1 > 0 || byte_data == 10)) { for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) Tavle.직렬쓰기(data[Loop_INDEKS]); 단말.문자(10); 일치수++; }
                post_TÆL_8f7753a1 = 0; if (byte_data != 10) break;
            } else if (post_TÆL_8f7753a1 < data.length) data[post_TÆL_8f7753a1++] = byte_data;
            else { 명령해석기.fejl(-28); Luk(); return; }
        }
        Luk(); if (byte_data < 0) 명령해석기.fejl(byte_data); else if (명령해석기.KR == 0) 명령해석기.KR = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEKS = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = ciffer_VÆRDI(2); argument_INDEKS = 3; }
        if (줄수 < 0 || 명령해석기.token_TÆL > argument_INDEKS + 1) { 명령해석기.KR = 2; 단말.Skrive("사용법: head/tail [-n 줄수] [Fil]\n"); return; }
        if (!Tilrettelæg_input(argument_INDEKS)) return;
        int post_TÆL_8f7753a1 = 0, byte_data;
        while ((byte_data = Læse()) != 256 && byte_data >= 0) { if (post_TÆL_8f7753a1 == data.length) { 명령해석기.fejl(-28); Luk(); return; } data[post_TÆL_8f7753a1++] = byte_data; }
        Luk(); if (byte_data < 0) { 명령해석기.fejl(byte_data); return; }
        int lokal_START = 0, afslutte_et_opkald_placere = post_TÆL_8f7753a1;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int i_alt_TÆL = 0; for (int Loop_INDEKS = post_TÆL_8f7753a1 - 2; Loop_INDEKS >= 0; Loop_INDEKS--) if (data[Loop_INDEKS] == 10 && ++i_alt_TÆL == 줄수) { lokal_START = Loop_INDEKS + 1; break; } }
        else { int i_alt_TÆL = 0; for (int Loop_INDEKS = 0; Loop_INDEKS < post_TÆL_8f7753a1; Loop_INDEKS++) if (data[Loop_INDEKS] == 10 && ++i_alt_TÆL == 줄수) { afslutte_et_opkald_placere = Loop_INDEKS + 1; break; } }
        for (int Loop_INDEKS = lokal_START; Loop_INDEKS < afslutte_et_opkald_placere; Loop_INDEKS++) Tavle.직렬쓰기(data[Loop_INDEKS]);
    }
    static void 함께쓰기() {
        boolean tilføj = 명령해석기.같음(1, "-a"); int argument_INDEKS = tilføj ? 2 : 1;
        if (명령해석기.token_TÆL != argument_INDEKS + 1) { 명령해석기.KR = 2; 단말.Skrive("사용법: tee [-a] Fil\n"); return; }
        int 열린파일번호 = åben_fil(argument_INDEKS, tilføj ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.fejl(열린파일번호); return; }
        inputfil = -1; int byte_data;
        while ((byte_data = Læse()) != 256 && byte_data >= 0) { int 처리값 = Hukommelse_Filer.Skrive(열린파일번호, byte_data); if (처리값 < 0) { 명령해석기.fejl(처리값); break; } Tavle.직렬쓰기(byte_data); }
        Hukommelse_Filer.Luk(열린파일번호);
    }
}
