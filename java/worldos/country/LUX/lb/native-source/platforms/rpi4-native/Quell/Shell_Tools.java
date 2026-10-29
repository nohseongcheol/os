// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 Shell 내장 Tools. */
public final class Shell_Tools {
    static int[] Daten = new int[16384];
    static int 입력파일 = -1;
    static int ariichten_Fichier(int Argument_INDEX, int Prozess_MODE) {
        int 처리값 = 명령해석기.Wee(Argument_INDEX); return 처리값 < 0 ? 처리값 : Späicher_Fichieren.ariichten(Prozess_MODE);
    }
    static boolean 입력준비(int Argument_INDEX) {
        입력파일 = -1;
        if (Argument_INDEX < 명령해석기.Token_COUNT) {
            입력파일 = ariichten_Fichier(Argument_INDEX, 0);
            if (입력파일 < 0) { 명령해석기.Feeler(입력파일); return false; }
        }
        return true;
    }
    static int 읽기() {
        if (입력파일 >= 3) return Späicher_Fichieren.읽기(입력파일);
        while (true) {
            int Byte_Daten = Board.직렬읽기(); if (Byte_Daten == -2 || Byte_Daten == 4) return 256;
            if (Byte_Daten == 3) { 명령해석기.Mooss = 130; return 256; }
            if (Byte_Daten >= 0) return Byte_Daten; Board.YIELD_CPU();
        }
    }
    static void Clôture() { if (입력파일 >= 3) Späicher_Fichieren.Clôture(입력파일); 입력파일 = -1; }
    static void Vue_VALUE() {
        int 마지막자리 = 명령해석기.Token_COUNT == 1 ? 2 : 명령해석기.Token_COUNT;
        for (int Argument_INDEX = 1; Argument_INDEX < 마지막자리; Argument_INDEX++) {
            if (!입력준비(Argument_INDEX)) continue;
            int Byte_Daten; while ((Byte_Daten = 읽기()) != 256 && Byte_Daten >= 0) Board.직렬쓰기(Byte_Daten);
            if (Byte_Daten < 0) 명령해석기.Feeler(Byte_Daten); Clôture();
        }
    }
    static void Fichier_Job(String 동작번호) {
        if (명령해석기.Token_COUNT != 2) { 명령해석기.Mooss = 2; 단말.schreiwen("사용법: mkdir/rmdir/touch Fichier\n"); return; }
        int 처리값 = 명령해석기.Wee(1);
        if (처리값 >= 0) {
            if (동작번호.charAt(0) == 'm') 처리값 = Späicher_Fichieren.Create_Verzeechnes();
            else if (동작번호.charAt(0) == 'r') 처리값 = Späicher_Fichieren.ewechhuelen_Verzeechnes();
            else { 처리값 = Späicher_Fichieren.ariichten(65); if (처리값 >= 3) 처리값 = Späicher_Fichieren.Clôture(처리값); }
        }
        if (처리값 < 0) 명령해석기.Feeler(처리값);
    }
    static void Instanz_VALUE(boolean 이동여부) {
        if (명령해석기.Token_COUNT != 3) { 명령해석기.Mooss = 2; 단말.schreiwen("사용법: cp/mv 원본 목적지 (Fichier)\n"); return; }
        int 처리값 = 명령해석기.Wee(1); if (처리값 >= 0) 처리값 = Späicher_Fichieren.normaliséieren_VALUE();
        if (처리값 < 0) { 명령해석기.Feeler(처리값); return; }
        int 원본번호 = Späicher_Fichieren.FIND_Agab(); if (원본번호 < 0) { 명령해석기.Feeler(-2); return; }
        int Agab_COUNT = Späicher_Fichieren.Längt_VALUE[원본번호]; for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) Daten[Loop_INDEX] = Späicher_Fichieren.자료읽기(원본번호, Loop_INDEX);
        처리값 = 명령해석기.Wee(2); if (처리값 >= 0) 처리값 = Späicher_Fichieren.normaliséieren_VALUE();
        if (처리값 < 0) { 명령해석기.Feeler(처리값); return; }
        if (Späicher_Fichieren.FIND_Agab() == 원본번호) { if (!이동여부) 명령해석기.Feeler(-22); return; }
        if (이동여부) { 처리값 = Späicher_Fichieren.이름바꾸기(원본번호); if (처리값 < 0) 명령해석기.Feeler(처리값); return; }
        int 열린파일번호 = Späicher_Fichieren.ariichten(577); if (열린파일번호 < 0) { 명령해석기.Feeler(열린파일번호); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) { 처리값 = Späicher_Fichieren.schreiwen(열린파일번호, Daten[Loop_INDEX]); if (처리값 < 0) { 명령해석기.Feeler(처리값); break; } }
        Späicher_Fichieren.Clôture(열린파일번호);
    }
    static int Ziffer_VALUE(int Argument_INDEX) {
        if (Argument_INDEX >= 명령해석기.Token_COUNT) return -1;
        int Agab_COUNT = 0; for (int Loop_INDEX = 0; Loop_INDEX < 명령해석기.Längt_VALUE[Argument_INDEX]; Loop_INDEX++) { int Zeechecode = 명령해석기.Token_VALUE[명령해석기.시작점[Argument_INDEX] + Loop_INDEX]; if (Zeechecode < '0' || Zeechecode > '9' || Agab_COUNT > 10000) return -1; Agab_COUNT = Agab_COUNT * 10 + Zeechecode - '0'; } return Agab_COUNT;
    }
    static void 세기() {
        int Argument_INDEX = 1, 선택번호 = 0;
        if (명령해석기.같음(1, "-c") || 명령해석기.같음(1, "-l") || 명령해석기.같음(1, "-w")) { 선택번호 = 명령해석기.같음(1, "-c") ? 1 : 명령해석기.같음(1, "-l") ? 2 : 3; Argument_INDEX++; }
        if (명령해석기.Token_COUNT > Argument_INDEX + 1) { 명령해석기.Mooss = 2; 단말.schreiwen("사용법: wc [-c|-l|-w] [Fichier]\n"); return; }
        if (!입력준비(Argument_INDEX)) return;
        int Byte_COUNT = 0, 줄수 = 0, 낱말수 = 0, Byte_Daten; boolean 낱말 = false;
        while ((Byte_Daten = 읽기()) >= 0 && Byte_Daten != 256) { Byte_COUNT++; if (Byte_Daten == 10) 줄수++; boolean Plaz = Byte_Daten == 32 || Byte_Daten >= 9 && Byte_Daten <= 13; if (!Plaz && !낱말) 낱말수++; 낱말 = !Plaz; }
        Clôture(); if (Byte_Daten < 0) { 명령해석기.Feeler(Byte_Daten); return; }
        if (선택번호 != 0) 단말.수(선택번호 == 1 ? Byte_COUNT : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.수(줄수); 단말.문자(' '); 단말.수(낱말수); 단말.문자(' '); 단말.수(Byte_COUNT); } 단말.문자(10);
    }
    static void FIND_Agab() {
        if (명령해석기.Token_COUNT < 2 || 명령해석기.Token_COUNT > 3) { 명령해석기.Mooss = 2; 단말.schreiwen("사용법: grep 찾을문구 [Fichier]\n"); return; }
        if (!입력준비(2)) return;
        int Agab_COUNT = 0, Byte_Daten, 일치수 = 0;
        while (true) {
            Byte_Daten = 읽기();
            if (Byte_Daten == 10 || Byte_Daten == 256 || Byte_Daten < 0) {
                boolean 찾은여부 = false;
                for (int Loop_INDEX = 0; Loop_INDEX <= Agab_COUNT - 명령해석기.Längt_VALUE[1]; Loop_INDEX++) {
                    boolean 같은여부 = true; for (int intern_Verknëppung_positionéieren = 0; intern_Verknëppung_positionéieren < 명령해석기.Längt_VALUE[1]; intern_Verknëppung_positionéieren++) if (Daten[Loop_INDEX + intern_Verknëppung_positionéieren] != 명령해석기.Token_VALUE[명령해석기.시작점[1] + intern_Verknëppung_positionéieren]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (Agab_COUNT > 0 || Byte_Daten == 10)) { for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) Board.직렬쓰기(Daten[Loop_INDEX]); 단말.문자(10); 일치수++; }
                Agab_COUNT = 0; if (Byte_Daten != 10) break;
            } else if (Agab_COUNT < Daten.length) Daten[Agab_COUNT++] = Byte_Daten;
            else { 명령해석기.Feeler(-28); Clôture(); return; }
        }
        Clôture(); if (Byte_Daten < 0) 명령해석기.Feeler(Byte_Daten); else if (명령해석기.Mooss == 0) 명령해석기.Mooss = 일치수 == 0 ? 1 : 0;
    }
    static void 머리(boolean 뒤쪽자리) {
        int Argument_INDEX = 1, 줄수 = 10;
        if (명령해석기.같음(1, "-n")) { 줄수 = Ziffer_VALUE(2); Argument_INDEX = 3; }
        if (줄수 < 0 || 명령해석기.Token_COUNT > Argument_INDEX + 1) { 명령해석기.Mooss = 2; 단말.schreiwen("사용법: head/tail [-n 줄수] [Fichier]\n"); return; }
        if (!입력준비(Argument_INDEX)) return;
        int Agab_COUNT = 0, Byte_Daten;
        while ((Byte_Daten = 읽기()) != 256 && Byte_Daten >= 0) { if (Agab_COUNT == Daten.length) { 명령해석기.Feeler(-28); Clôture(); return; } Daten[Agab_COUNT++] = Byte_Daten; }
        Clôture(); if (Byte_Daten < 0) { 명령해석기.Feeler(Byte_Daten); return; }
        int lokal_Start = 0, bëennegen_positionéieren = Agab_COUNT;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int 총수 = 0; for (int Loop_INDEX = Agab_COUNT - 2; Loop_INDEX >= 0; Loop_INDEX--) if (Daten[Loop_INDEX] == 10 && ++총수 == 줄수) { lokal_Start = Loop_INDEX + 1; break; } }
        else { int 총수 = 0; for (int Loop_INDEX = 0; Loop_INDEX < Agab_COUNT; Loop_INDEX++) if (Daten[Loop_INDEX] == 10 && ++총수 == 줄수) { bëennegen_positionéieren = Loop_INDEX + 1; break; } }
        for (int Loop_INDEX = lokal_Start; Loop_INDEX < bëennegen_positionéieren; Loop_INDEX++) Board.직렬쓰기(Daten[Loop_INDEX]);
    }
    static void 함께쓰기() {
        boolean 덧붙임여부 = 명령해석기.같음(1, "-a"); int Argument_INDEX = 덧붙임여부 ? 2 : 1;
        if (명령해석기.Token_COUNT != Argument_INDEX + 1) { 명령해석기.Mooss = 2; 단말.schreiwen("사용법: tee [-a] Fichier\n"); return; }
        int 열린파일번호 = ariichten_Fichier(Argument_INDEX, 덧붙임여부 ? 1089 : 577); if (열린파일번호 < 0) { 명령해석기.Feeler(열린파일번호); return; }
        입력파일 = -1; int Byte_Daten;
        while ((Byte_Daten = 읽기()) != 256 && Byte_Daten >= 0) { int 처리값 = Späicher_Fichieren.schreiwen(열린파일번호, Byte_Daten); if (처리값 < 0) { 명령해석기.Feeler(처리값); break; } Board.직렬쓰기(Byte_Daten); }
        Späicher_Fichieren.Clôture(열린파일번호);
    }
}
