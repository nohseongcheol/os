// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 Shell Status_VALUE. Fichier 저장소는 공유하고 Wee/변수/LOG_Rei/입력은 분리한다. */
public final class Fënster_Sessioun {
    static int[] 보관 = new int[4 * 30000], Préparéieren = new int[4];
    static int 현재, positionéieren;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] Daten, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < Daten.length; Loop_INDEX++) { if (Store_VALUE) 보관[positionéieren++] = Daten[Loop_INDEX]; else Daten[Loop_INDEX] = 보관[positionéieren++]; }
    }
    static int VALUE(int Daten_VALUE, boolean 저장여부) { if (저장여부) { 보관[positionéieren++] = Daten_VALUE; return Daten_VALUE; } return 보관[positionéieren++]; }
    static void sichen_positionéieren(int 보관칸, boolean 저장여부) {
        positionéieren = 보관칸 * 30000;
        ARRAY_VALUE(Späicher_Fichieren.현재, 저장여부); Späicher_Fichieren.현재길이 = VALUE(Späicher_Fichieren.현재길이, 저장여부);
        ARRAY_VALUE(Shell_Syntax.변수이름, 저장여부); ARRAY_VALUE(Shell_Syntax.변수값, 저장여부); ARRAY_VALUE(Shell_Syntax.이름길이, 저장여부); ARRAY_VALUE(Shell_Syntax.VALUE_Längt, 저장여부);
        Shell_Syntax.Status_VALUE = VALUE(Shell_Syntax.Status_VALUE, 저장여부);
        ARRAY_VALUE(Zeil_Editeur.LOG_Rei, 저장여부); ARRAY_VALUE(Zeil_Editeur.LOG_Längt, 저장여부); ARRAY_VALUE(Zeil_Editeur.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Zeil, 저장여부);
        Zeil_Editeur.LOG_COUNT = VALUE(Zeil_Editeur.LOG_COUNT, 저장여부); Zeil_Editeur.LOG_Rei_bëennegen = VALUE(Zeil_Editeur.LOG_Rei_bëennegen, 저장여부);
        Zeil_Editeur.Sich_VALUE = VALUE(Zeil_Editeur.Sich_VALUE, 저장여부); Zeil_Editeur.저장길이 = VALUE(Zeil_Editeur.저장길이, 저장여부);
        Zeil_Editeur.d_Gréisst_veränneren = VALUE(Zeil_Editeur.d_Gréisst_veränneren, 저장여부); Zeil_Editeur.Curseur_VALUE = VALUE(Zeil_Editeur.Curseur_VALUE, 저장여부); Zeil_Editeur.Start_Fënster = VALUE(Zeil_Editeur.Start_Fënster, 저장여부);
        Préparéieren[보관칸] = 1;
    }
    static void Prozess_VALUE_Agab() {
        int 사건번호 = Board.Terminal(12); if (사건번호 == 0) return;
        sichen_positionéieren(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Board.Kontroll_Benotzer_App(32 + Loop_INDEX); Préparéieren[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Préparéieren[Loop_INDEX] = 0;
        }
        int Weider_positionéieren = (사건번호 & 15) - 1; if (Weider_positionéieren < 0) Weider_positionéieren = 0;
        if (Préparéieren[Weider_positionéieren] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Weider_positionéieren * 30000 + Loop_INDEX] = 0;
        현재 = Weider_positionéieren; sichen_positionéieren(현재, false); Board.Terminal(100 + 현재); 이어읽기 = true;
        단말.schreiwen("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Board.Kontroll_Benotzer_App(16 + 현재) == 0) return false;
        셸입출력.Erlaben_interaktiv = true; 셸입출력.Laf(false, false); Board.입출력전환(1);
        int 처리값 = Board.Kontroll_Benotzer_App(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; Shell_Syntax.Status_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.schreiwen("exit "); 단말.수(처리값); 단말.문자(10); Board.Terminal(3); }
        return true;
    }
}
