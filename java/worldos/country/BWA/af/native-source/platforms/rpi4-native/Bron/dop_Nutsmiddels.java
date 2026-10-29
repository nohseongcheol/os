// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 dop 내장 Nutsmiddels. */
public final class dop_Nutsmiddels {
    static int[] data = new int[16384];
    static int 입력파일 = -1;
    static int skep_lêer(int argument_INDEX, int Proses_MODE) {
        int 처리값 = 명령해석기.Pad(argument_INDEX); return 처리값 < 0 ? 처리값 : Geheue_Lêers.skep(Proses_MODE);
    }
    static boolean 입력준비(int argument_INDEX) {
        입력파일 = -1;
        if (argument_INDEX < 명령해석기.kenteken_COUNT) {
            입력파일 = skep_lêer(argument_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.Fout(입력파일); return false; }
        }
        return true;
    }
    static int Lees() {
        if (입력파일 >= 3) return Geheue_Lêers.Lees(입력파일);
        while (true) {
            int greep_data = bord.직렬읽기(); if (greep_data == -2 || greep_data == 4) return 256;
            if (greep_data == 3) { 명령해석기.maatreël = 130; return 256; }
            if (greep_data >= 0) return greep_data; bord.YIELD_SVE();
        }
    }
    static void Sluit() { if (입력파일 >= 3) Geheue_Lêers.Sluit(입력파일); 입력파일 = -1; }
    static void bekyk_VALUE() {
        int 마지막자리 = 명령해석기.kenteken_COUNT == 1 ? 2 : 명령해석기.kenteken_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int greep_data; while ((greep_data = Lees()) != 256 && greep_data >= 0) bord.직렬쓰기(greep_data);
            if (greep_data < 0) 명령해석기.Fout(greep_data); Sluit();
        }
    }
    static void lêer_saak(String 동작번호) {
        if (명령해석기.kenteken_COUNT != 2) { 명령해석기.maatreël = 2; 단말.Skryf("사용법: mkdir/rmdir/touch Lêer\n"); return; }
        int 처리값 = 명령해석기.Pad(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Geheue_Lêers.Skep_gids();
            else if (동작번호.charAt(0) == 'r') 처리값 = Geheue_Lêers.verwyder_gids();
            else { 처리값 = Geheue_Lêers.skep(65); if (처리값 >= 3) 처리값 = Geheue_Lêers.Sluit(처리값); }
        }
        if (처리값 < 0) 명령해석기.Fout(처리값);
    }
    static void geval_VALUE(boolean 이동여부) {
        if (명령해석기.kenteken_COUNT != 3) { 명령해석기.maatreël = 2; 단말.Skryf("사용법: cp/mv 원본 목적지 (Lêer)\n"); return; }
        int 처리값 = 명령해석기.Pad(1); if (처리값 >= 0) 처리값 = Geheue_Lêers.normaliseer_VALUE();
        if (처리값 < 0) { 명령해석기.Fout(처리값); return; }
        int 원본번호 = Geheue_Lêers.FIND_inskrywing(); if (원본번호 < 0) { 명령해석기.Fout(-2); return; }
        int inskrywing_COUNT = Geheue_Lêers.lengte_VALUE[원본번호]; for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) data[lus_INDEX] = Geheue_Lêers.자료읽기(원본번호, lus_INDEX);
        처리값 = 명령해석기.Pad(2); if (처리값 >= 0) 처리값 = Geheue_Lêers.normaliseer_VALUE();
        if (처리값 < 0) { 명령해석기.Fout(처리값); return; }
        if (Geheue_Lêers.FIND_inskrywing() == 원본번호) { if (!이동여부) 명령해석기.Fout(-22); return; }
        if (이동여부) { 처리값 = Geheue_Lêers.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Fout(처리값); return; }
        int 열린파일번호 = Geheue_Lêers.skep(577); if (열린파일번호 < 0) { 명령해석기.Fout(열린파일번호); return; }
        for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) { 처리값 = Geheue_Lêers.Skryf(열린파일번호, data[lus_INDEX]); if (처리값 < 0) { 명령해석기.Fout(처리값); break; } }
        Geheue_Lêers.Sluit(열린파일번호);
    }
    static int syfer_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.kenteken_COUNT) return -1;
        int inskrywing_COUNT = 0; for (int lus_INDEX = 0; lus_INDEX < 명령해석기.lengte_VALUE[argument_INDEX]; lus_INDEX++) { int karakterkode = 명령해석기.kenteken_VALUE[명령해석기.시작점[argument_INDEX] + lus_INDEX]; if (karakterkode < '0' || karakterkode > '9' || inskrywing_COUNT > 10000) return -1; inskrywing_COUNT = inskrywing_COUNT * 10 + karakterkode - '0'; } return inskrywing_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.kenteken_COUNT > argument_INDEX + 1) { 명령해석기.maatreël = 2; 단말.Skryf("사용법: wc [-c|-l|-w] [Lêer]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int greep_COUNT = 0, 줄수 = 0, 낱말수 = 0, greep_data; boolean 낱말 = false;
        while ((greep_data = Lees()) >= 0 && greep_data != 256) { greep_COUNT++; if (greep_data == 10) 줄수++; boolean ruimte = greep_data == 32 || greep_data >= 9 && greep_data <= 13; if (!ruimte && !낱말) 낱말수++; 낱말 = !ruimte; }
        Sluit(); if (greep_data < 0) { 명령해석기.Fout(greep_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? greep_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(greep_COUNT); } 단말.문자(10);
    }
    static void FIND_inskrywing() {
        if (명령해석기.kenteken_COUNT < 2 || 명령해석기.kenteken_COUNT > 3) { 명령해석기.maatreël = 2; 단말.Skryf("사용법: grep 찾을문구 [Lêer]\n"); return; }
        if (!입력준비(2)) return;
        int inskrywing_COUNT = 0, greep_data, 일치수 = 0;
        while (true) {
            greep_data = Lees();
            if (greep_data == 10 || greep_data == 256 || greep_data < 0) {
                boolean 찾은여부 = false;
                for (int lus_INDEX = 0; lus_INDEX <= inskrywing_COUNT - 명령해석기.lengte_VALUE[1]; lus_INDEX++) {
                    boolean 같은여부 = true; for (int binnebind_plaas = 0; binnebind_plaas < 명령해석기.lengte_VALUE[1]; binnebind_plaas++) if (data[lus_INDEX + binnebind_plaas] != 명령해석기.kenteken_VALUE[명령해석기.시작점[1] + binnebind_plaas]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (inskrywing_COUNT > 0 || greep_data == 10)) { for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) bord.직렬쓰기(data[lus_INDEX]); 단말.문자(10); 일치수++; }
                inskrywing_COUNT = 0; if (greep_data != 10) break;
            } else if (inskrywing_COUNT < data.length) data[inskrywing_COUNT++] = greep_data;
            else { 명령해석기.Fout(-28); Sluit(); return; }
        }
        Sluit(); if (greep_data < 0) 명령해석기.Fout(greep_data); else if (명령해석기.maatreël == 0) 명령해석기.maatreël = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = syfer_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.kenteken_COUNT > argument_INDEX + 1) { 명령해석기.maatreël = 2; 단말.Skryf("사용법: head/tail [-n 줄수] [Lêer]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int inskrywing_COUNT = 0, greep_data;
        while ((greep_data = Lees()) != 256 && greep_data >= 0) { if (inskrywing_COUNT == data.length) { 명령해석기.Fout(-28); Sluit(); return; } data[inskrywing_COUNT++] = greep_data; }
        Sluit(); if (greep_data < 0) { 명령해석기.Fout(greep_data); return; }
        int lokaal_BEGIN = 0, beëindig_plaas = inskrywing_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int lus_INDEX = inskrywing_COUNT - 2; lus_INDEX >= 0; lus_INDEX--) if (data[lus_INDEX] == 10 && ++총수 == 줄수) { lokaal_BEGIN = lus_INDEX + 1; break; } }
        else { int 총수 = 0; for (int lus_INDEX = 0; lus_INDEX < inskrywing_COUNT; lus_INDEX++) if (data[lus_INDEX] == 10 && ++총수 == 줄수) { beëindig_plaas = lus_INDEX + 1; break; } }
        for (int lus_INDEX = lokaal_BEGIN; lus_INDEX < beëindig_plaas; lus_INDEX++) bord.직렬쓰기(data[lus_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argument_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.kenteken_COUNT != argument_INDEX + 1) { 명령해석기.maatreël = 2; 단말.Skryf("사용법: tee [-a] Lêer\n"); return; }
        int 열린파일번호 = skep_lêer(argument_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Fout(열린파일번호); return; }
        입력파일 = -1; int greep_data;
        while ((greep_data = Lees()) != 256 && greep_data >= 0) { int 처리값 = Geheue_Lêers.Skryf(열린파일번호, greep_data); if (처리값 < 0) { 명령해석기.Fout(처리값); break; } bord.직렬쓰기(greep_data); }
        Geheue_Lêers.Sluit(열린파일번호);
    }
}
