// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 slige 내장 innealan. */
public final class slige_innealan {
    static int[] dàta = new int[16384];
    static int 입력파일 = -1;
    static int fosgail_faidhle(int argamaid_INDEX, int Pròiseas_MODE) {
        int 처리값 = 명령해석기.Slighe(argamaid_INDEX); return 처리값 < 0 ? 처리값 : cuimhne_faidhlichean.fosgail(Pròiseas_MODE);
    }
    static boolean 입력준비(int argamaid_INDEX) {
        입력파일 = -1;
        if (argamaid_INDEX < 명령해석기.tòcan_COUNT) {
            입력파일 = fosgail_faidhle(argamaid_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.Mearachd(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return cuimhne_faidhlichean.읽기(입력파일);
        while (true) {
            int baidht_dàta = bòrd.직렬읽기(); if (baidht_dàta == -2 || baidht_dàta == 4) return 256;
            if (baidht_dàta == 3) { 명령해석기.tomhas = 130; return 256; }
            if (baidht_dàta >= 0) return baidht_dàta; bòrd.YIELD_CPU();
        }
    }
    static void dùin() { if (입력파일 >= 3) cuimhne_faidhlichean.dùin(입력파일); 입력파일 = -1; }
    static void seall_VALUE() {
        int 마지막자리 = 명령해석기.tòcan_COUNT == 1 ? 2 : 명령해석기.tòcan_COUNT;
        for (int argamaid_INDEX = 1; argamaid_INDEX < 마지막자리; argamaid_INDEX++) {
            if (!입력준비(argamaid_INDEX)) continue;
            int baidht_dàta; while ((baidht_dàta = 읽기()) != 256 && baidht_dàta >= 0) bòrd.직렬쓰기(baidht_dàta);
            if (baidht_dàta < 0) 명령해석기.Mearachd(baidht_dàta); dùin();
        }
    }
    static void faidhle_cùis(String 동작번호) {
        if (명령해석기.tòcan_COUNT != 2) { 명령해석기.tomhas = 2; 단말.sgrìobh("사용법: mkdir/rmdir/touch faidhle\n"); return; }
        int 처리값 = 명령해석기.Slighe(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = cuimhne_faidhlichean.Create_eòlaire();
            else if (동작번호.charAt(0) == 'r') 처리값 = cuimhne_faidhlichean.thoir_air_falbh_eòlaire();
            else { 처리값 = cuimhne_faidhlichean.fosgail(65); if (처리값 >= 3) 처리값 = cuimhne_faidhlichean.dùin(처리값); }
        }
        if (처리값 < 0) 명령해석기.Mearachd(처리값);
    }
    static void ionstans_VALUE(boolean 이동여부) {
        if (명령해석기.tòcan_COUNT != 3) { 명령해석기.tomhas = 2; 단말.sgrìobh("사용법: cp/mv 원본 목적지 (faidhle)\n"); return; }
        int 처리값 = 명령해석기.Slighe(1); if (처리값 >= 0) 처리값 = cuimhne_faidhlichean.àbhaistich_VALUE();
        if (처리값 < 0) { 명령해석기.Mearachd(처리값); return; }
        int 원본번호 = cuimhne_faidhlichean.FIND_cur_a_steach(); if (원본번호 < 0) { 명령해석기.Mearachd(-2); return; }
        int cur_a_steach_COUNT = cuimhne_faidhlichean.faid_VALUE[원본번호]; for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) dàta[lùb_INDEX] = cuimhne_faidhlichean.자료읽기(원본번호, lùb_INDEX);
        처리값 = 명령해석기.Slighe(2); if (처리값 >= 0) 처리값 = cuimhne_faidhlichean.àbhaistich_VALUE();
        if (처리값 < 0) { 명령해석기.Mearachd(처리값); return; }
        if (cuimhne_faidhlichean.FIND_cur_a_steach() == 원본번호) { if (!이동여부) 명령해석기.Mearachd(-22); return; }
        if (이동여부) { 처리값 = cuimhne_faidhlichean.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Mearachd(처리값); return; }
        int 열린파일번호 = cuimhne_faidhlichean.fosgail(577); if (열린파일번호 < 0) { 명령해석기.Mearachd(열린파일번호); return; }
        for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) { 처리값 = cuimhne_faidhlichean.sgrìobh(열린파일번호, dàta[lùb_INDEX]); if (처리값 < 0) { 명령해석기.Mearachd(처리값); break; } }
        cuimhne_faidhlichean.dùin(열린파일번호);
    }
    static int figear_VALUE(int argamaid_INDEX) {
        if (argamaid_INDEX >= 명령해석기.tòcan_COUNT) return -1;
        int cur_a_steach_COUNT = 0; for (int lùb_INDEX = 0; lùb_INDEX < 명령해석기.faid_VALUE[argamaid_INDEX]; lùb_INDEX++) { int còd_a_charactair = 명령해석기.tòcan_VALUE[명령해석기.시작점[argamaid_INDEX] + lùb_INDEX]; if (còd_a_charactair < '0' || còd_a_charactair > '9' || cur_a_steach_COUNT > 10000) return -1; cur_a_steach_COUNT = cur_a_steach_COUNT * 10 + còd_a_charactair - '0'; } return cur_a_steach_COUNT;
    }
    static void 세기() {
        int argamaid_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argamaid_INDEX++; }
        if (명령해석기.tòcan_COUNT > argamaid_INDEX + 1) { 명령해석기.tomhas = 2; 단말.sgrìobh("사용법: wc [-c|-l|-w] [faidhle]\n"); return; }
        if (!입력준비(argamaid_INDEX)) return;
        int baidht_COUNT = 0, 줄수 = 0, 낱말수 = 0, baidht_dàta; boolean 낱말 = false;
        while ((baidht_dàta = 읽기()) >= 0 && baidht_dàta != 256) { baidht_COUNT++; if (baidht_dàta == 10) 줄수++; boolean spàs = baidht_dàta == 32 || baidht_dàta >= 9 && baidht_dàta <= 13; if (!spàs && !낱말) 낱말수++; 낱말 = !spàs; }
        dùin(); if (baidht_dàta < 0) { 명령해석기.Mearachd(baidht_dàta); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? baidht_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(baidht_COUNT); } 단말.문자(10);
    }
    static void FIND_cur_a_steach() {
        if (명령해석기.tòcan_COUNT < 2 || 명령해석기.tòcan_COUNT > 3) { 명령해석기.tomhas = 2; 단말.sgrìobh("사용법: grep 찾을문구 [faidhle]\n"); return; }
        if (!입력준비(2)) return;
        int cur_a_steach_COUNT = 0, baidht_dàta, 일치수 = 0;
        while (true) {
            baidht_dàta = 읽기();
            if (baidht_dàta == 10 || baidht_dàta == 256 || baidht_dàta < 0) {
                boolean 찾은여부 = false;
                for (int lùb_INDEX = 0; lùb_INDEX <= cur_a_steach_COUNT - 명령해석기.faid_VALUE[1]; lùb_INDEX++) {
                    boolean 같은여부 = true; for (int Inner_Join_suidhich = 0; Inner_Join_suidhich < 명령해석기.faid_VALUE[1]; Inner_Join_suidhich++) if (dàta[lùb_INDEX + Inner_Join_suidhich] != 명령해석기.tòcan_VALUE[명령해석기.시작점[1] + Inner_Join_suidhich]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (cur_a_steach_COUNT > 0 || baidht_dàta == 10)) { for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) bòrd.직렬쓰기(dàta[lùb_INDEX]); 단말.문자(10); 일치수++; }
                cur_a_steach_COUNT = 0; if (baidht_dàta != 10) break;
            } else if (cur_a_steach_COUNT < dàta.length) dàta[cur_a_steach_COUNT++] = baidht_dàta;
            else { 명령해석기.Mearachd(-28); dùin(); return; }
        }
        dùin(); if (baidht_dàta < 0) 명령해석기.Mearachd(baidht_dàta); else if (명령해석기.tomhas == 0) 명령해석기.tomhas = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argamaid_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = figear_VALUE(2); argamaid_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.tòcan_COUNT > argamaid_INDEX + 1) { 명령해석기.tomhas = 2; 단말.sgrìobh("사용법: head/tail [-n 줄수] [faidhle]\n"); return; }
        if (!입력준비(argamaid_INDEX)) return;
        int cur_a_steach_COUNT = 0, baidht_dàta;
        while ((baidht_dàta = 읽기()) != 256 && baidht_dàta >= 0) { if (cur_a_steach_COUNT == dàta.length) { 명령해석기.Mearachd(-28); dùin(); return; } dàta[cur_a_steach_COUNT++] = baidht_dàta; }
        dùin(); if (baidht_dàta < 0) { 명령해석기.Mearachd(baidht_dàta); return; }
        int ionadail_Start = 0, crìochnaich_suidhich = cur_a_steach_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int lùb_INDEX = cur_a_steach_COUNT - 2; lùb_INDEX >= 0; lùb_INDEX--) if (dàta[lùb_INDEX] == 10 && ++총수 == 줄수) { ionadail_Start = lùb_INDEX + 1; break; } }
        else { int 총수 = 0; for (int lùb_INDEX = 0; lùb_INDEX < cur_a_steach_COUNT; lùb_INDEX++) if (dàta[lùb_INDEX] == 10 && ++총수 == 줄수) { crìochnaich_suidhich = lùb_INDEX + 1; break; } }
        for (int lùb_INDEX = ionadail_Start; lùb_INDEX < crìochnaich_suidhich; lùb_INDEX++) bòrd.직렬쓰기(dàta[lùb_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argamaid_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.tòcan_COUNT != argamaid_INDEX + 1) { 명령해석기.tomhas = 2; 단말.sgrìobh("사용법: tee [-a] faidhle\n"); return; }
        int 열린파일번호 = fosgail_faidhle(argamaid_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Mearachd(열린파일번호); return; }
        입력파일 = -1; int baidht_dàta;
        while ((baidht_dàta = 읽기()) != 256 && baidht_dàta >= 0) { int 처리값 = cuimhne_faidhlichean.sgrìobh(열린파일번호, baidht_dàta); if (처리값 < 0) { 명령해석기.Mearachd(처리값); break; } bòrd.직렬쓰기(baidht_dàta); }
        cuimhne_faidhlichean.dùin(열린파일번호);
    }
}
