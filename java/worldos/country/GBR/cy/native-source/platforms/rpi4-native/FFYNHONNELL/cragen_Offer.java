// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 cragen 내장 Offer. */
public final class cragen_Offer {
    static int[] data = new int[16384];
    static int 입력파일 = -1;
    static int agor_ffeil(int arg_INDEX, int Proses_MODE) {
        int 처리값 = 명령해석기.LLWYBR(arg_INDEX); return 처리값 < 0 ? 처리값 : Cof_Ffeil.Agor(Proses_MODE);
    }
    static boolean 입력준비(int arg_INDEX) {
        입력파일 = -1;
        if (arg_INDEX < 명령해석기.tocyn_COUNT_3176ee99) {
            입력파일 = agor_ffeil(arg_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.Gwall(입력파일); return false; }
        }
        return true;
    }
    static int Darllen() {
        if (입력파일 >= 3) return Cof_Ffeil.Darllen(입력파일);
        while (true) {
            int beit_data = bwrdd.직렬읽기(); if (beit_data == -2 || beit_data == 4) return 256;
            if (beit_data == 3) { 명령해석기.mesur = 130; return 256; }
            if (beit_data >= 0) return beit_data; bwrdd.atal_CPU();
        }
    }
    static void Cau() { if (입력파일 >= 3) Cof_Ffeil.Cau(입력파일); 입력파일 = -1; }
    static void Gwedd_VALUE() {
        int 마지막자리 = 명령해석기.tocyn_COUNT_3176ee99 == 1 ? 2 : 명령해석기.tocyn_COUNT_3176ee99;
        for (int arg_INDEX = 1; arg_INDEX < 마지막자리; arg_INDEX++) {
            if (!입력준비(arg_INDEX)) continue;
            int beit_data; while ((beit_data = Darllen()) != 256 && beit_data >= 0) bwrdd.직렬쓰기(beit_data);
            if (beit_data < 0) 명령해석기.Gwall(beit_data); Cau();
        }
    }
    static void ffeil_tasg(String 동작번호) {
        if (명령해석기.tocyn_COUNT_3176ee99 != 2) { 명령해석기.mesur = 2; 단말.Ysgrifennu("사용법: mkdir/rmdir/touch Ffeil\n"); return; }
        int 처리값 = 명령해석기.LLWYBR(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Cof_Ffeil.Creu_cyfeiriadur();
            else if (동작번호.charAt(0) == 'r') 처리값 = Cof_Ffeil.tynnu_cyfeiriadur();
            else { 처리값 = Cof_Ffeil.Agor(65); if (처리값 >= 3) 처리값 = Cof_Ffeil.Cau(처리값); }
        }
        if (처리값 < 0) 명령해석기.Gwall(처리값);
    }
    static void copïo_VALUE(boolean 이동여부) {
        if (명령해석기.tocyn_COUNT_3176ee99 != 3) { 명령해석기.mesur = 2; 단말.Ysgrifennu("사용법: cp/mv 원본 목적지 (Ffeil)\n"); return; }
        int 처리값 = 명령해석기.LLWYBR(1); if (처리값 >= 0) 처리값 = Cof_Ffeil.normaleiddio_VALUE();
        if (처리값 < 0) { 명령해석기.Gwall(처리값); return; }
        int 원본번호 = Cof_Ffeil.FIND_cofnod(); if (원본번호 < 0) { 명령해석기.Gwall(-2); return; }
        int cofnod_COUNT = Cof_Ffeil.hyd_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) data[Loop_INDEX] = Cof_Ffeil.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.LLWYBR(2); if (처리값 >= 0) 처리값 = Cof_Ffeil.normaleiddio_VALUE();
        if (처리값 < 0) { 명령해석기.Gwall(처리값); return; }
        if (Cof_Ffeil.FIND_cofnod() == 원본번호) { if (!이동여부) 명령해석기.Gwall(-22); return; }
        if (이동여부) { 처리값 = Cof_Ffeil.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Gwall(처리값); return; }
        int 열린파일번호 = Cof_Ffeil.Agor(577); if (열린파일번호 < 0) { 명령해석기.Gwall(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) { 처리값 = Cof_Ffeil.Ysgrifennu(열린파일번호, data[Loop_INDEX]); if (처리값 < 0) { 명령해석기.Gwall(처리값); break; } }
        Cof_Ffeil.Cau(열린파일번호);
    }
    static int digid_VALUE(int arg_INDEX) {
        if (arg_INDEX >= 명령해석기.tocyn_COUNT_3176ee99) return -1;
        int cofnod_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.hyd_VALUE[arg_INDEX]; Loop_INDEX++) { int cod_nod = 명령해석기.tocyn_VALUE_eb540501[명령해석기.시작점[arg_INDEX] + Loop_INDEX]; if (cod_nod < '0' || cod_nod > '9' || cofnod_COUNT > 10000) return -1; cofnod_COUNT = cofnod_COUNT * 10 + cod_nod - '0'; } return cofnod_COUNT;
    }
    static void 세기() {
        int arg_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; arg_INDEX++; }
        if (명령해석기.tocyn_COUNT_3176ee99 > arg_INDEX + 1) { 명령해석기.mesur = 2; 단말.Ysgrifennu("사용법: wc [-c|-l|-w] [Ffeil]\n"); return; }
        if (!입력준비(arg_INDEX)) return;
        int beit_COUNT = 0, 줄수 = 0, 낱말수 = 0, beit_data; boolean 낱말 = false;
        while ((beit_data = Darllen()) >= 0 && beit_data != 256) { beit_COUNT++; if (beit_data == 10) 줄수++; boolean lle = beit_data == 32 || beit_data >= 9 && beit_data <= 13; if (!lle && !낱말) 낱말수++; 낱말 = !lle; }
        Cau(); if (beit_data < 0) { 명령해석기.Gwall(beit_data); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? beit_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(beit_COUNT); } 단말.문자(10);
    }
    static void FIND_cofnod() {
        if (명령해석기.tocyn_COUNT_3176ee99 < 2 || 명령해석기.tocyn_COUNT_3176ee99 > 3) { 명령해석기.mesur = 2; 단말.Ysgrifennu("사용법: grep 찾을문구 [Ffeil]\n"); return; }
        if (!입력준비(2)) return;
        int cofnod_COUNT = 0, beit_data, 일치수 = 0;
        while (true) {
            beit_data = Darllen();
            if (beit_data == 10 || beit_data == 256 || beit_data < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= cofnod_COUNT - 명령해석기.hyd_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int uno_mewnol_safle = 0; uno_mewnol_safle < 명령해석기.hyd_VALUE[1]; uno_mewnol_safle++) if (data[Loop_INDEX + uno_mewnol_safle] != 명령해석기.tocyn_VALUE_eb540501[명령해석기.시작점[1] + uno_mewnol_safle]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (cofnod_COUNT > 0 || beit_data == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) bwrdd.직렬쓰기(data[Loop_INDEX]); 단말.문자(10); 일치수++; }
                cofnod_COUNT = 0; if (beit_data != 10) break;
            } else if (cofnod_COUNT < data.length) data[cofnod_COUNT++] = beit_data;
            else { 명령해석기.Gwall(-28); Cau(); return; }
        }
        Cau(); if (beit_data < 0) 명령해석기.Gwall(beit_data); else if (명령해석기.mesur == 0) 명령해석기.mesur = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int arg_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = digid_VALUE(2); arg_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.tocyn_COUNT_3176ee99 > arg_INDEX + 1) { 명령해석기.mesur = 2; 단말.Ysgrifennu("사용법: head/tail [-n 줄수] [Ffeil]\n"); return; }
        if (!입력준비(arg_INDEX)) return;
        int cofnod_COUNT = 0, beit_data;
        while ((beit_data = Darllen()) != 256 && beit_data >= 0) { if (cofnod_COUNT == data.length) { 명령해석기.Gwall(-28); Cau(); return; } data[cofnod_COUNT++] = beit_data; }
        Cau(); if (beit_data < 0) { 명령해석기.Gwall(beit_data); return; }
        int lleol_START = 0, gorffen_safle = cofnod_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = cofnod_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { lleol_START = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < cofnod_COUNT; Loop_INDEX++) if (data[Loop_INDEX] == 10 && ++총수 == 줄수) { gorffen_safle = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lleol_START; Loop_INDEX < gorffen_safle; Loop_INDEX++) bwrdd.직렬쓰기(data[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int arg_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.tocyn_COUNT_3176ee99 != arg_INDEX + 1) { 명령해석기.mesur = 2; 단말.Ysgrifennu("사용법: tee [-a] Ffeil\n"); return; }
        int 열린파일번호 = agor_ffeil(arg_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Gwall(열린파일번호); return; }
        입력파일 = -1; int beit_data;
        while ((beit_data = Darllen()) != 256 && beit_data >= 0) { int 처리값 = Cof_Ffeil.Ysgrifennu(열린파일번호, beit_data); if (처리값 < 0) { 명령해석기.Gwall(처리값); break; } bwrdd.직렬쓰기(beit_data); }
        Cof_Ffeil.Cau(열린파일번호);
    }
}
