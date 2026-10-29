// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 skel 내장 Verkfæri. */
public final class skel_Verkfæri {
    static int[] gögn = new int[16384];
    static int 입력파일 = -1;
    static int opið_skrá(int frumbreyta_INDEX, int Ferli_MODE) {
        int 처리값 = 명령해석기.SLÓÐ(frumbreyta_INDEX); return 처리값 < 0 ? 처리값 : Minni_Skrár.Opna(Ferli_MODE);
    }
    static boolean 입력준비(int frumbreyta_INDEX) {
        입력파일 = -1;
        if (frumbreyta_INDEX < 명령해석기.tákn_COUNT) {
            입력파일 = opið_skrá(frumbreyta_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.Villa(입력파일); return false; }
        }
        return true;
    }
    static int Lestur() {
        if (입력파일 >= 3) return Minni_Skrár.Lestur(입력파일);
        while (true) {
            int bæti_gögn = bretti.직렬읽기(); if (bæti_gögn == -2 || bæti_gögn == 4) return 256;
            if (bæti_gögn == 3) { 명령해석기.NIÐURSTAÐA = 130; return 256; }
            if (bæti_gögn >= 0) return bæti_gögn; bretti.YIELD_örgjörvi();
        }
    }
    static void Loka() { if (입력파일 >= 3) Minni_Skrár.Loka(입력파일); 입력파일 = -1; }
    static void Sýn_VALUE() {
        int 마지막자리 = 명령해석기.tákn_COUNT == 1 ? 2 : 명령해석기.tákn_COUNT;
        for (int frumbreyta_INDEX = 1; frumbreyta_INDEX < 마지막자리; frumbreyta_INDEX++) {
            if (!입력준비(frumbreyta_INDEX)) continue;
            int bæti_gögn; while ((bæti_gögn = Lestur()) != 256 && bæti_gögn >= 0) bretti.직렬쓰기(bæti_gögn);
            if (bæti_gögn < 0) 명령해석기.Villa(bæti_gögn); Loka();
        }
    }
    static void skrá_mál(String aðgerð_númer) {
        if (명령해석기.tákn_COUNT != 2) { 명령해석기.NIÐURSTAÐA = 2; 단말.Skrift("사용법: mkdir/rmdir/touch Skrá\n"); return; }
        int 처리값 = 명령해석기.SLÓÐ(1);
        if (처리값 >= 0) {
            if (aðgerð_númer.charAt(0) == 'm') 처리값 = Minni_Skrár.stofna_skráasafn();
            else if (aðgerð_númer.charAt(0) == 'r') 처리값 = Minni_Skrár.fjarlægja_skráasafn();
            else { 처리값 = Minni_Skrár.Opna(65); if (처리값 >= 3) 처리값 = Minni_Skrár.Loka(처리값); }
        }
        if (처리값 < 0) 명령해석기.Villa(처리값);
    }
    static void afrita_VALUE(boolean 이동여부) {
        if (명령해석기.tákn_COUNT != 3) { 명령해석기.NIÐURSTAÐA = 2; 단말.Skrift("사용법: cp/mv 원본 endastaður_endastöð (Skrá)\n"); return; }
        int 처리값 = 명령해석기.SLÓÐ(1); if (처리값 >= 0) 처리값 = Minni_Skrár.staðla_VALUE();
        if (처리값 < 0) { 명령해석기.Villa(처리값); return; }
        int 원본번호 = Minni_Skrár.FIND_færsla(); if (원본번호 < 0) { 명령해석기.Villa(-2); return; }
        int færsla_COUNT = Minni_Skrár.lengd_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) gögn[Loop_INDEX] = Minni_Skrár.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.SLÓÐ(2); if (처리값 >= 0) 처리값 = Minni_Skrár.staðla_VALUE();
        if (처리값 < 0) { 명령해석기.Villa(처리값); return; }
        if (Minni_Skrár.FIND_færsla() == 원본번호) { if (!이동여부) 명령해석기.Villa(-22); return; }
        if (이동여부) { 처리값 = Minni_Skrár.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Villa(처리값); return; }
        int 열린파일번호 = Minni_Skrár.Opna(577); if (열린파일번호 < 0) { 명령해석기.Villa(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) { 처리값 = Minni_Skrár.Skrift(열린파일번호, gögn[Loop_INDEX]); if (처리값 < 0) { 명령해석기.Villa(처리값); break; } }
        Minni_Skrár.Loka(열린파일번호);
    }
    static int tölustafur_VALUE(int frumbreyta_INDEX) {
        if (frumbreyta_INDEX >= 명령해석기.tákn_COUNT) return -1;
        int færsla_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.lengd_VALUE[frumbreyta_INDEX]; Loop_INDEX++) { int stafkóði = 명령해석기.tákn_VALUE_eb540501[명령해석기.시작점[frumbreyta_INDEX] + Loop_INDEX]; if (stafkóði < '0' || stafkóði > '9' || færsla_COUNT > 10000) return -1; færsla_COUNT = færsla_COUNT * 10 + stafkóði - '0'; } return færsla_COUNT;
    }
    static void 세기() {
        int frumbreyta_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; frumbreyta_INDEX++; }
        if (명령해석기.tákn_COUNT > frumbreyta_INDEX + 1) { 명령해석기.NIÐURSTAÐA = 2; 단말.Skrift("사용법: wc [-c|-l|-w] [Skrá]\n"); return; }
        if (!입력준비(frumbreyta_INDEX)) return;
        int bæti_COUNT = 0, 줄수 = 0, 낱말수 = 0, bæti_gögn; boolean 낱말 = false;
        while ((bæti_gögn = Lestur()) >= 0 && bæti_gögn != 256) { bæti_COUNT++; if (bæti_gögn == 10) 줄수++; boolean svæði = bæti_gögn == 32 || bæti_gögn >= 9 && bæti_gögn <= 13; if (!svæði && !낱말) 낱말수++; 낱말 = !svæði; }
        Loka(); if (bæti_gögn < 0) { 명령해석기.Villa(bæti_gögn); return; }
        if (선택번호 != 0) 단말.númer(선택번호 == 1 ? bæti_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.númer(줄수); 단말.문자(' '); 단말.númer(낱말수); 단말.문자(' '); 단말.númer(bæti_COUNT); } 단말.문자(10);
    }
    static void FIND_færsla() {
        if (명령해석기.tákn_COUNT < 2 || 명령해석기.tákn_COUNT > 3) { 명령해석기.NIÐURSTAÐA = 2; 단말.Skrift("사용법: grep 찾을문구 [Skrá]\n"); return; }
        if (!입력준비(2)) return;
        int færsla_COUNT = 0, bæti_gögn, 일치수 = 0;
        while (true) {
            bæti_gögn = Lestur();
            if (bæti_gögn == 10 || bæti_gögn == 256 || bæti_gögn < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= færsla_COUNT - 명령해석기.lengd_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int innri_samtenging_staða = 0; innri_samtenging_staða < 명령해석기.lengd_VALUE[1]; innri_samtenging_staða++) if (gögn[Loop_INDEX + innri_samtenging_staða] != 명령해석기.tákn_VALUE_eb540501[명령해석기.시작점[1] + innri_samtenging_staða]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (færsla_COUNT > 0 || bæti_gögn == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) bretti.직렬쓰기(gögn[Loop_INDEX]); 단말.문자(10); 일치수++; }
                færsla_COUNT = 0; if (bæti_gögn != 10) break;
            } else if (færsla_COUNT < gögn.length) gögn[færsla_COUNT++] = bæti_gögn;
            else { 명령해석기.Villa(-28); Loka(); return; }
        }
        Loka(); if (bæti_gögn < 0) 명령해석기.Villa(bæti_gögn); else if (명령해석기.NIÐURSTAÐA == 0) 명령해석기.NIÐURSTAÐA = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int frumbreyta_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = tölustafur_VALUE(2); frumbreyta_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.tákn_COUNT > frumbreyta_INDEX + 1) { 명령해석기.NIÐURSTAÐA = 2; 단말.Skrift("사용법: head/tail [-n 줄수] [Skrá]\n"); return; }
        if (!입력준비(frumbreyta_INDEX)) return;
        int færsla_COUNT = 0, bæti_gögn;
        while ((bæti_gögn = Lestur()) != 256 && bæti_gögn >= 0) { if (færsla_COUNT == gögn.length) { 명령해석기.Villa(-28); Loka(); return; } gögn[færsla_COUNT++] = bæti_gögn; }
        Loka(); if (bæti_gögn < 0) { 명령해석기.Villa(bæti_gögn); return; }
        int staðbundið_Opna = 0, ljúka_staða = færsla_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int samtala_COUNT = 0; for (int Loop_INDEX = færsla_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (gögn[Loop_INDEX] == 10 && ++samtala_COUNT == 줄수) { staðbundið_Opna = Loop_INDEX + 1; break; } }
        else { int samtala_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < færsla_COUNT; Loop_INDEX++) if (gögn[Loop_INDEX] == 10 && ++samtala_COUNT == 줄수) { ljúka_staða = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = staðbundið_Opna; Loop_INDEX < ljúka_staða; Loop_INDEX++) bretti.직렬쓰기(gögn[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int frumbreyta_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.tákn_COUNT != frumbreyta_INDEX + 1) { 명령해석기.NIÐURSTAÐA = 2; 단말.Skrift("사용법: tee [-a] Skrá\n"); return; }
        int 열린파일번호 = opið_skrá(frumbreyta_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Villa(열린파일번호); return; }
        입력파일 = -1; int bæti_gögn;
        while ((bæti_gögn = Lestur()) != 256 && bæti_gögn >= 0) { int 처리값 = Minni_Skrár.Skrift(열린파일번호, bæti_gögn); if (처리값 < 0) { 명령해석기.Villa(처리값); break; } bretti.직렬쓰기(bæti_gögn); }
        Minni_Skrár.Loka(열린파일번호);
    }
}
