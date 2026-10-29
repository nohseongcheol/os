// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 anga 내장 Ngā_Utauta. */
public final class anga_Ngā_Utauta {
    static int[] raraunga = new int[16384];
    static int 입력파일 = -1;
    static int tiwhikete_kōnae(int tohenga_INDEX, int Hātepe_MODE) {
        int 처리값 = 명령해석기.ara(tohenga_INDEX); return 처리값 < 0 ? 처리값 : Pūmahara_Ngā_Kōnae.Huaki(Hātepe_MODE);
    }
    static boolean 입력준비(int tohenga_INDEX) {
        입력파일 = -1;
        if (tohenga_INDEX < 명령해석기.tohu_COUNT) {
            입력파일 = tiwhikete_kōnae(tohenga_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.Pōhēhē(입력파일); return false; }
        }
        return true;
    }
    static int Pānuitia() {
        if (입력파일 >= 3) return Pūmahara_Ngā_Kōnae.Pānuitia(입력파일);
        while (true) {
            int paita_raraunga = papa.직렬읽기(); if (paita_raraunga == -2 || paita_raraunga == 4) return 256;
            if (paita_raraunga == 3) { 명령해석기.mēhua = 130; return 256; }
            if (paita_raraunga >= 0) return paita_raraunga; papa.YIELD_PTM();
        }
    }
    static void Kati() { if (입력파일 >= 3) Pūmahara_Ngā_Kōnae.Kati(입력파일); 입력파일 = -1; }
    static void tiro_uara() {
        int 마지막자리 = 명령해석기.tohu_COUNT == 1 ? 2 : 명령해석기.tohu_COUNT;
        for (int tohenga_INDEX = 1; tohenga_INDEX < 마지막자리; tohenga_INDEX++) {
            if (!입력준비(tohenga_INDEX)) continue;
            int paita_raraunga; while ((paita_raraunga = Pānuitia()) != 256 && paita_raraunga >= 0) papa.직렬쓰기(paita_raraunga);
            if (paita_raraunga < 0) 명령해석기.Pōhēhē(paita_raraunga); Kati();
        }
    }
    static void kōnae_kēhi(String 동작번호) {
        if (명령해석기.tohu_COUNT != 2) { 명령해석기.mēhua = 2; 단말.Tuhia("사용법: mkdir/rmdir/touch Kōnae\n"); return; }
        int 처리값 = 명령해석기.ara(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Pūmahara_Ngā_Kōnae.Waihanga_whaiaronga();
            else if (동작번호.charAt(0) == 'r') 처리값 = Pūmahara_Ngā_Kōnae.tango_whaiaronga();
            else { 처리값 = Pūmahara_Ngā_Kōnae.Huaki(65); if (처리값 >= 3) 처리값 = Pūmahara_Ngā_Kōnae.Kati(처리값); }
        }
        if (처리값 < 0) 명령해석기.Pōhēhē(처리값);
    }
    static void tārua_uara(boolean 이동여부) {
        if (명령해석기.tohu_COUNT != 3) { 명령해석기.mēhua = 2; 단말.Tuhia("사용법: cp/mv 원본 목적지 (Kōnae)\n"); return; }
        int 처리값 = 명령해석기.ara(1); if (처리값 >= 0) 처리값 = Pūmahara_Ngā_Kōnae.whakanoa_uara();
        if (처리값 < 0) { 명령해석기.Pōhēhē(처리값); return; }
        int 원본번호 = Pūmahara_Ngā_Kōnae.FIND_tāurunga(); if (원본번호 < 0) { 명령해석기.Pōhēhē(-2); return; }
        int tāurunga_COUNT = Pūmahara_Ngā_Kōnae.roa_uara[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) raraunga[Loop_INDEX] = Pūmahara_Ngā_Kōnae.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.ara(2); if (처리값 >= 0) 처리값 = Pūmahara_Ngā_Kōnae.whakanoa_uara();
        if (처리값 < 0) { 명령해석기.Pōhēhē(처리값); return; }
        if (Pūmahara_Ngā_Kōnae.FIND_tāurunga() == 원본번호) { if (!이동여부) 명령해석기.Pōhēhē(-22); return; }
        if (이동여부) { 처리값 = Pūmahara_Ngā_Kōnae.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Pōhēhē(처리값); return; }
        int 열린파일번호 = Pūmahara_Ngā_Kōnae.Huaki(577); if (열린파일번호 < 0) { 명령해석기.Pōhēhē(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) { 처리값 = Pūmahara_Ngā_Kōnae.Tuhia(열린파일번호, raraunga[Loop_INDEX]); if (처리값 < 0) { 명령해석기.Pōhēhē(처리값); break; } }
        Pūmahara_Ngā_Kōnae.Kati(열린파일번호);
    }
    static int mati_uara(int tohenga_INDEX) {
        if (tohenga_INDEX >= 명령해석기.tohu_COUNT) return -1;
        int tāurunga_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.roa_uara[tohenga_INDEX]; Loop_INDEX++) { int waehere_pūāhua = 명령해석기.tohu_uara_eb540501[명령해석기.시작점[tohenga_INDEX] + Loop_INDEX]; if (waehere_pūāhua < '0' || waehere_pūāhua > '9' || tāurunga_COUNT > 10000) return -1; tāurunga_COUNT = tāurunga_COUNT * 10 + waehere_pūāhua - '0'; } return tāurunga_COUNT;
    }
    static void 세기() {
        int tohenga_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; tohenga_INDEX++; }
        if (명령해석기.tohu_COUNT > tohenga_INDEX + 1) { 명령해석기.mēhua = 2; 단말.Tuhia("사용법: wc [-c|-l|-w] [Kōnae]\n"); return; }
        if (!입력준비(tohenga_INDEX)) return;
        int paita_COUNT = 0, 줄수 = 0, 낱말수 = 0, paita_raraunga; boolean 낱말 = false;
        while ((paita_raraunga = Pānuitia()) >= 0 && paita_raraunga != 256) { paita_COUNT++; if (paita_raraunga == 10) 줄수++; boolean wāhi = paita_raraunga == 32 || paita_raraunga >= 9 && paita_raraunga <= 13; if (!wāhi && !낱말) 낱말수++; 낱말 = !wāhi; }
        Kati(); if (paita_raraunga < 0) { 명령해석기.Pōhēhē(paita_raraunga); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? paita_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(paita_COUNT); } 단말.문자(10);
    }
    static void FIND_tāurunga() {
        if (명령해석기.tohu_COUNT < 2 || 명령해석기.tohu_COUNT > 3) { 명령해석기.mēhua = 2; 단말.Tuhia("사용법: grep 찾을문구 [Kōnae]\n"); return; }
        if (!입력준비(2)) return;
        int tāurunga_COUNT = 0, paita_raraunga, 일치수 = 0;
        while (true) {
            paita_raraunga = Pānuitia();
            if (paita_raraunga == 10 || paita_raraunga == 256 || paita_raraunga < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= tāurunga_COUNT - 명령해석기.roa_uara[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int hono_roto_tūranga = 0; hono_roto_tūranga < 명령해석기.roa_uara[1]; hono_roto_tūranga++) if (raraunga[Loop_INDEX + hono_roto_tūranga] != 명령해석기.tohu_uara_eb540501[명령해석기.시작점[1] + hono_roto_tūranga]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (tāurunga_COUNT > 0 || paita_raraunga == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) papa.직렬쓰기(raraunga[Loop_INDEX]); 단말.문자(10); 일치수++; }
                tāurunga_COUNT = 0; if (paita_raraunga != 10) break;
            } else if (tāurunga_COUNT < raraunga.length) raraunga[tāurunga_COUNT++] = paita_raraunga;
            else { 명령해석기.Pōhēhē(-28); Kati(); return; }
        }
        Kati(); if (paita_raraunga < 0) 명령해석기.Pōhēhē(paita_raraunga); else if (명령해석기.mēhua == 0) 명령해석기.mēhua = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int tohenga_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = mati_uara(2); tohenga_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.tohu_COUNT > tohenga_INDEX + 1) { 명령해석기.mēhua = 2; 단말.Tuhia("사용법: head/tail [-n 줄수] [Kōnae]\n"); return; }
        if (!입력준비(tohenga_INDEX)) return;
        int tāurunga_COUNT = 0, paita_raraunga;
        while ((paita_raraunga = Pānuitia()) != 256 && paita_raraunga >= 0) { if (tāurunga_COUNT == raraunga.length) { 명령해석기.Pōhēhē(-28); Kati(); return; } raraunga[tāurunga_COUNT++] = paita_raraunga; }
        Kati(); if (paita_raraunga < 0) { 명령해석기.Pōhēhē(paita_raraunga); return; }
        int paetata_Start = 0, mutu_tūranga = tāurunga_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = tāurunga_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (raraunga[Loop_INDEX] == 10 && ++총수 == 줄수) { paetata_Start = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < tāurunga_COUNT; Loop_INDEX++) if (raraunga[Loop_INDEX] == 10 && ++총수 == 줄수) { mutu_tūranga = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = paetata_Start; Loop_INDEX < mutu_tūranga; Loop_INDEX++) papa.직렬쓰기(raraunga[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int tohenga_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.tohu_COUNT != tohenga_INDEX + 1) { 명령해석기.mēhua = 2; 단말.Tuhia("사용법: tee [-a] Kōnae\n"); return; }
        int 열린파일번호 = tiwhikete_kōnae(tohenga_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Pōhēhē(열린파일번호); return; }
        입력파일 = -1; int paita_raraunga;
        while ((paita_raraunga = Pānuitia()) != 256 && paita_raraunga >= 0) { int 처리값 = Pūmahara_Ngā_Kōnae.Tuhia(열린파일번호, paita_raraunga); if (처리값 < 0) { 명령해석기.Pōhēhē(처리값); break; } papa.직렬쓰기(paita_raraunga); }
        Pūmahara_Ngā_Kōnae.Kati(열린파일번호);
    }
}
