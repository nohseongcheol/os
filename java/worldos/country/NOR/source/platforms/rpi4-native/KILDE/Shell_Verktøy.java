// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 Shell 내장 Verktøy. */
public final class Shell_Verktøy {
    static int[] data = new int[16384];
    static int inndatafil = -1;
    static int åpen_Fil(int argument_INDEKS, int Prosess_MODUS) {
        int 처리값 = 명령해석기.Sti(argument_INDEKS); return 처리값 < 0 ? 처리값 : Minne_Filer.Åpne(Prosess_MODUS);
    }
    static boolean Forbered_inndata(int argument_INDEKS) {
        inndatafil = -1;
        if (argument_INDEKS < 명령해석기.token_ANTALL) {
            inndatafil = åpen_Fil(argument_INDEKS, 0);
            if (inndatafil < 0) { 명령해석기.feil(inndatafil); return false; }
        }
        return true;
    }
    static int Les() {
        if (inndatafil >= 3) return Minne_Filer.Les(inndatafil);
        while (true) {
            int byte_data = Tavle.직렬읽기(); if (byte_data == -2 || byte_data == 4) return 256;
            if (byte_data == 3) { 명령해석기.KR = 130; return 256; }
            if (byte_data >= 0) return byte_data; Tavle.AVKAST_CPU();
        }
    }
    static void Lukk() { if (inndatafil >= 3) Minne_Filer.Lukk(inndatafil); inndatafil = -1; }
    static void vise_VERDI() {
        int 마지막자리 = 명령해석기.token_ANTALL == 1 ? 2 : 명령해석기.token_ANTALL;
        for (int argument_INDEKS = 1; argument_INDEKS < 마지막자리; argument_INDEKS++) {
            if (!Forbered_inndata(argument_INDEKS)) continue;
            int byte_data; while ((byte_data = Les()) != 256 && byte_data >= 0) Tavle.직렬쓰기(byte_data);
            if (byte_data < 0) 명령해석기.feil(byte_data); Lukk();
        }
    }
    static void Fil_sak(String Gjøremål_nummer) {
        if (명령해석기.token_ANTALL != 2) { 명령해석기.KR = 2; 단말.Skriv("사용법: mkdir/rmdir/touch Fil\n"); return; }
        int 처리값 = 명령해석기.Sti(1);
        if (처리값 >= 0) {
            if (Gjøremål_nummer.charAt(0) == 'm') 처리값 = Minne_Filer.åpne_katalog();
            else if (Gjøremål_nummer.charAt(0) == 'r') 처리값 = Minne_Filer.fjerne_katalog();
            else { 처리값 = Minne_Filer.Åpne(65); if (처리값 >= 3) 처리값 = Minne_Filer.Lukk(처리값); }
        }
        if (처리값 < 0) 명령해석기.feil(처리값);
    }
    static void kopiere_VERDI(boolean 이동여부) {
        if (명령해석기.token_ANTALL != 3) { 명령해석기.KR = 2; 단말.Skriv("사용법: cp/mv 원본 mål_deltaker (Fil)\n"); return; }
        int 처리값 = 명령해석기.Sti(1); if (처리값 >= 0) 처리값 = Minne_Filer.normalisere_VERDI();
        if (처리값 < 0) { 명령해석기.feil(처리값); return; }
        int 원본번호 = Minne_Filer.Søk_oppføring(); if (원본번호 < 0) { 명령해석기.feil(-2); return; }
        int oppføring_ANTALL = Minne_Filer.lengde_VERDI[원본번호]; for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) data[Loop_INDEKS] = Minne_Filer.자료읽기(원본번호, Loop_INDEKS);
        처리값 = 명령해석기.Sti(2); if (처리값 >= 0) 처리값 = Minne_Filer.normalisere_VERDI();
        if (처리값 < 0) { 명령해석기.feil(처리값); return; }
        if (Minne_Filer.Søk_oppføring() == 원본번호) { if (!이동여부) 명령해석기.feil(-22); return; }
        if (이동여부) { 처리값 = Minne_Filer.Gi_nytt_navn_oppføring(원본번호); if (처리값 < 0) 명령해석기.feil(처리값); return; }
        int 열린파일번호 = Minne_Filer.Åpne(577); if (열린파일번호 < 0) { 명령해석기.feil(열린파일번호); return; }
        for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) { 처리값 = Minne_Filer.Skriv(열린파일번호, data[Loop_INDEKS]); if (처리값 < 0) { 명령해석기.feil(처리값); break; } }
        Minne_Filer.Lukk(열린파일번호);
    }
    static int siffer_VERDI(int argument_INDEKS) {
        if (argument_INDEKS >= 명령해석기.token_ANTALL) return -1;
        int oppføring_ANTALL = 0; for (int Loop_INDEKS = 0; Loop_INDEKS < 명령해석기.lengde_VERDI[argument_INDEKS]; Loop_INDEKS++) { int tegnkode = 명령해석기.token_VERDI[명령해석기.시작점[argument_INDEKS] + Loop_INDEKS]; if (tegnkode < '0' || tegnkode > '9' || oppføring_ANTALL > 10000) return -1; oppføring_ANTALL = oppføring_ANTALL * 10 + tegnkode - '0'; } return oppføring_ANTALL;
    }
    static void 세기() {
        int argument_INDEKS = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEKS++; }
        if (명령해석기.token_ANTALL > argument_INDEKS + 1) { 명령해석기.KR = 2; 단말.Skriv("사용법: wc [-c|-l|-w] [Fil]\n"); return; }
        if (!Forbered_inndata(argument_INDEKS)) return;
        int byte_ANTALL = 0, 줄수 = 0, 낱말수 = 0, byte_data; boolean 낱말 = false;
        while ((byte_data = Les()) >= 0 && byte_data != 256) { byte_ANTALL++; if (byte_data == 10) 줄수++; boolean Space = byte_data == 32 || byte_data >= 9 && byte_data <= 13; if (!Space && !낱말) 낱말수++; 낱말 = !Space; }
        Lukk(); if (byte_data < 0) { 명령해석기.feil(byte_data); return; }
        if (선택번호 != 0) 단말.nummer(선택번호 == 1 ? byte_ANTALL : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.nummer(줄수); 단말.문자(' '); 단말.nummer(낱말수); 단말.문자(' '); 단말.nummer(byte_ANTALL); } 단말.문자(10);
    }
    static void Søk_oppføring() {
        if (명령해석기.token_ANTALL < 2 || 명령해석기.token_ANTALL > 3) { 명령해석기.KR = 2; 단말.Skriv("사용법: grep 찾을문구 [Fil]\n"); return; }
        if (!Forbered_inndata(2)) return;
        int oppføring_ANTALL = 0, byte_data, 일치수 = 0;
        while (true) {
            byte_data = Les();
            if (byte_data == 10 || byte_data == 256 || byte_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEKS = 0; Loop_INDEKS <= oppføring_ANTALL - 명령해석기.lengde_VERDI[1]; Loop_INDEKS++) {
                    boolean 같은여부 = true; for (int indre_kobling_plassere = 0; indre_kobling_plassere < 명령해석기.lengde_VERDI[1]; indre_kobling_plassere++) if (data[Loop_INDEKS + indre_kobling_plassere] != 명령해석기.token_VERDI[명령해석기.시작점[1] + indre_kobling_plassere]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (oppføring_ANTALL > 0 || byte_data == 10)) { for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) Tavle.직렬쓰기(data[Loop_INDEKS]); 단말.문자(10); 일치수++; }
                oppføring_ANTALL = 0; if (byte_data != 10) break;
            } else if (oppføring_ANTALL < data.length) data[oppføring_ANTALL++] = byte_data;
            else { 명령해석기.feil(-28); Lukk(); return; }
        }
        Lukk(); if (byte_data < 0) 명령해석기.feil(byte_data); else if (명령해석기.KR == 0) 명령해석기.KR = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEKS = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = siffer_VERDI(2); argument_INDEKS = 3; }
        if (줄수 < 0 || 명령해석기.token_ANTALL > argument_INDEKS + 1) { 명령해석기.KR = 2; 단말.Skriv("사용법: head/tail [-n 줄수] [Fil]\n"); return; }
        if (!Forbered_inndata(argument_INDEKS)) return;
        int oppføring_ANTALL = 0, byte_data;
        while ((byte_data = Les()) != 256 && byte_data >= 0) { if (oppføring_ANTALL == data.length) { 명령해석기.feil(-28); Lukk(); return; } data[oppføring_ANTALL++] = byte_data; }
        Lukk(); if (byte_data < 0) { 명령해석기.feil(byte_data); return; }
        int lokal_START = 0, avslutte_en_samtale_plassere = oppføring_ANTALL;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int total_ANTALL = 0; for (int Loop_INDEKS = oppføring_ANTALL - 2; Loop_INDEKS >= 0; Loop_INDEKS--) if (data[Loop_INDEKS] == 10 && ++total_ANTALL == 줄수) { lokal_START = Loop_INDEKS + 1; break; } }
        else { int total_ANTALL = 0; for (int Loop_INDEKS = 0; Loop_INDEKS < oppføring_ANTALL; Loop_INDEKS++) if (data[Loop_INDEKS] == 10 && ++total_ANTALL == 줄수) { avslutte_en_samtale_plassere = Loop_INDEKS + 1; break; } }
        for (int Loop_INDEKS = lokal_START; Loop_INDEKS < avslutte_en_samtale_plassere; Loop_INDEKS++) Tavle.직렬쓰기(data[Loop_INDEKS]);
    }
    static void skrive_Sammen() {
        boolean Tilføye = 명령해석기.같음(1, "-a"); int argument_INDEKS = Tilføye ? 2 : 1;
        if (명령해석기.token_ANTALL != argument_INDEKS + 1) { 명령해석기.KR = 2; 단말.Skriv("사용법: tee [-a] Fil\n"); return; }
        int 열린파일번호 = åpen_Fil(argument_INDEKS, Tilføye ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.feil(열린파일번호); return; }
        inndatafil = -1; int byte_data;
        while ((byte_data = Les()) != 256 && byte_data >= 0) { int 처리값 = Minne_Filer.Skriv(열린파일번호, byte_data); if (처리값 < 0) { 명령해석기.feil(처리값); break; } Tavle.직렬쓰기(byte_data); }
        Minne_Filer.Lukk(열린파일번호);
    }
}
