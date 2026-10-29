// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 pasues 내장 Mjete. */
public final class pasues_Mjete {
    static int[] të_dhëna = new int[16384];
    static int 입력파일 = -1;
    static int hap_skedar(int argument_INDEX, int Proces_MODE) {
        int 처리값 = 명령해석기.POZICIONI(argument_INDEX); return 처리값 < 0 ? 처리값 : Memorie_Skedarët.Hap(Proces_MODE);
    }
    static boolean 입력준비(int argument_INDEX) {
        입력파일 = -1;
        if (argument_INDEX < 명령해석기.kodi_COUNT) {
            입력파일 = hap_skedar(argument_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.GABIM(입력파일); return false; }
        }
        return true;
    }
    static int Leximi() {
        if (입력파일 >= 3) return Memorie_Skedarët.Leximi(입력파일);
        while (true) {
            int bajt_të_dhëna = panel.직렬읽기(); if (bajt_të_dhëna == -2 || bajt_të_dhëna == 4) return 256;
            if (bajt_të_dhëna == 3) { 명령해석기.llogaritje = 130; return 256; }
            if (bajt_të_dhëna >= 0) return bajt_të_dhëna; panel.YIELD_CPU();
        }
    }
    static void Mbyll() { if (입력파일 >= 3) Memorie_Skedarët.Mbyll(입력파일); 입력파일 = -1; }
    static void Pamja_VALUE() {
        int 마지막자리 = 명령해석기.kodi_COUNT == 1 ? 2 : 명령해석기.kodi_COUNT;
        for (int argument_INDEX = 1; argument_INDEX < 마지막자리; argument_INDEX++) {
            if (!입력준비(argument_INDEX)) continue;
            int bajt_të_dhëna; while ((bajt_të_dhëna = Leximi()) != 256 && bajt_të_dhëna >= 0) panel.직렬쓰기(bajt_të_dhëna);
            if (bajt_të_dhëna < 0) 명령해석기.GABIM(bajt_të_dhëna); Mbyll();
        }
    }
    static void skedar_punë(String 동작번호) {
        if (명령해석기.kodi_COUNT != 2) { 명령해석기.llogaritje = 2; 단말.Shkrimi("사용법: mkdir/rmdir/touch Kartelë\n"); return; }
        int 처리값 = 명령해석기.POZICIONI(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Memorie_Skedarët.Krijo_direktori();
            else if (동작번호.charAt(0) == 'r') 처리값 = Memorie_Skedarët.heq_direktori();
            else { 처리값 = Memorie_Skedarët.Hap(65); if (처리값 >= 3) 처리값 = Memorie_Skedarët.Mbyll(처리값); }
        }
        if (처리값 < 0) 명령해석기.GABIM(처리값);
    }
    static void kopjoj_VALUE(boolean 이동여부) {
        if (명령해석기.kodi_COUNT != 3) { 명령해석기.llogaritje = 2; 단말.Shkrimi("사용법: cp/mv 원본 목적지 (Kartelë)\n"); return; }
        int 처리값 = 명령해석기.POZICIONI(1); if (처리값 >= 0) 처리값 = Memorie_Skedarët.normalizoj_VALUE();
        if (처리값 < 0) { 명령해석기.GABIM(처리값); return; }
        int 원본번호 = Memorie_Skedarët.FIND_futje(); if (원본번호 < 0) { 명령해석기.GABIM(-2); return; }
        int futje_COUNT = Memorie_Skedarët.gjatësi_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) të_dhëna[Loop_INDEX] = Memorie_Skedarët.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.POZICIONI(2); if (처리값 >= 0) 처리값 = Memorie_Skedarët.normalizoj_VALUE();
        if (처리값 < 0) { 명령해석기.GABIM(처리값); return; }
        if (Memorie_Skedarët.FIND_futje() == 원본번호) { if (!이동여부) 명령해석기.GABIM(-22); return; }
        if (이동여부) { 처리값 = Memorie_Skedarët.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.GABIM(처리값); return; }
        int 열린파일번호 = Memorie_Skedarët.Hap(577); if (열린파일번호 < 0) { 명령해석기.GABIM(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) { 처리값 = Memorie_Skedarët.Shkrimi(열린파일번호, të_dhëna[Loop_INDEX]); if (처리값 < 0) { 명령해석기.GABIM(처리값); break; } }
        Memorie_Skedarët.Mbyll(열린파일번호);
    }
    static int shifër_VALUE(int argument_INDEX) {
        if (argument_INDEX >= 명령해석기.kodi_COUNT) return -1;
        int futje_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.gjatësi_VALUE[argument_INDEX]; Loop_INDEX++) { int kodi_i_karakterit = 명령해석기.kodi_VALUE[명령해석기.시작점[argument_INDEX] + Loop_INDEX]; if (kodi_i_karakterit < '0' || kodi_i_karakterit > '9' || futje_COUNT > 10000) return -1; futje_COUNT = futje_COUNT * 10 + kodi_i_karakterit - '0'; } return futje_COUNT;
    }
    static void 세기() {
        int argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; argument_INDEX++; }
        if (명령해석기.kodi_COUNT > argument_INDEX + 1) { 명령해석기.llogaritje = 2; 단말.Shkrimi("사용법: wc [-c|-l|-w] [Kartelë]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int bajt_COUNT = 0, 줄수 = 0, 낱말수 = 0, bajt_të_dhëna; boolean 낱말 = false;
        while ((bajt_të_dhëna = Leximi()) >= 0 && bajt_të_dhëna != 256) { bajt_COUNT++; if (bajt_të_dhëna == 10) 줄수++; boolean HAPËSIRË = bajt_të_dhëna == 32 || bajt_të_dhëna >= 9 && bajt_të_dhëna <= 13; if (!HAPËSIRË && !낱말) 낱말수++; 낱말 = !HAPËSIRË; }
        Mbyll(); if (bajt_të_dhëna < 0) { 명령해석기.GABIM(bajt_të_dhëna); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? bajt_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(bajt_COUNT); } 단말.문자(10);
    }
    static void FIND_futje() {
        if (명령해석기.kodi_COUNT < 2 || 명령해석기.kodi_COUNT > 3) { 명령해석기.llogaritje = 2; 단말.Shkrimi("사용법: grep 찾을문구 [Kartelë]\n"); return; }
        if (!입력준비(2)) return;
        int futje_COUNT = 0, bajt_të_dhëna, 일치수 = 0;
        while (true) {
            bajt_të_dhëna = Leximi();
            if (bajt_të_dhëna == 10 || bajt_të_dhëna == 256 || bajt_të_dhëna < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= futje_COUNT - 명령해석기.gjatësi_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int bashkim_i_brendshëm_pozicioni = 0; bashkim_i_brendshëm_pozicioni < 명령해석기.gjatësi_VALUE[1]; bashkim_i_brendshëm_pozicioni++) if (të_dhëna[Loop_INDEX + bashkim_i_brendshëm_pozicioni] != 명령해석기.kodi_VALUE[명령해석기.시작점[1] + bashkim_i_brendshëm_pozicioni]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (futje_COUNT > 0 || bajt_të_dhëna == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) panel.직렬쓰기(të_dhëna[Loop_INDEX]); 단말.문자(10); 일치수++; }
                futje_COUNT = 0; if (bajt_të_dhëna != 10) break;
            } else if (futje_COUNT < të_dhëna.length) të_dhëna[futje_COUNT++] = bajt_të_dhëna;
            else { 명령해석기.GABIM(-28); Mbyll(); return; }
        }
        Mbyll(); if (bajt_të_dhëna < 0) 명령해석기.GABIM(bajt_të_dhëna); else if (명령해석기.llogaritje == 0) 명령해석기.llogaritje = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = shifër_VALUE(2); argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.kodi_COUNT > argument_INDEX + 1) { 명령해석기.llogaritje = 2; 단말.Shkrimi("사용법: head/tail [-n 줄수] [Kartelë]\n"); return; }
        if (!입력준비(argument_INDEX)) return;
        int futje_COUNT = 0, bajt_të_dhëna;
        while ((bajt_të_dhëna = Leximi()) != 256 && bajt_të_dhëna >= 0) { if (futje_COUNT == të_dhëna.length) { 명령해석기.GABIM(-28); Mbyll(); return; } të_dhëna[futje_COUNT++] = bajt_të_dhëna; }
        Mbyll(); if (bajt_të_dhëna < 0) { 명령해석기.GABIM(bajt_të_dhëna); return; }
        int lokal_nis = 0, mbaroj_pozicioni = futje_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = futje_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (të_dhëna[Loop_INDEX] == 10 && ++총수 == 줄수) { lokal_nis = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < futje_COUNT; Loop_INDEX++) if (të_dhëna[Loop_INDEX] == 10 && ++총수 == 줄수) { mbaroj_pozicioni = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokal_nis; Loop_INDEX < mbaroj_pozicioni; Loop_INDEX++) panel.직렬쓰기(të_dhëna[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int argument_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.kodi_COUNT != argument_INDEX + 1) { 명령해석기.llogaritje = 2; 단말.Shkrimi("사용법: tee [-a] Kartelë\n"); return; }
        int 열린파일번호 = hap_skedar(argument_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.GABIM(열린파일번호); return; }
        입력파일 = -1; int bajt_të_dhëna;
        while ((bajt_të_dhëna = Leximi()) != 256 && bajt_të_dhëna >= 0) { int 처리값 = Memorie_Skedarët.Shkrimi(열린파일번호, bajt_të_dhëna); if (처리값 < 0) { 명령해석기.GABIM(처리값); break; } panel.직렬쓰기(bajt_të_dhëna); }
        Memorie_Skedarët.Mbyll(열린파일번호);
    }
}
