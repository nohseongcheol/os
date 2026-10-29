// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 shell stat_VALUE. fajl 저장소는 공유하고 mogħdija/변수/LOG_RECORD/입력은 분리한다. */
public final class tieqa_sessjoni {
    static int[] 보관 = new int[4 * 30000], Ħejji = new int[4];
    static int 현재, pożizzjoni;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] data, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < data.length; Loop_INDEX++) { if (Store_VALUE) 보관[pożizzjoni++] = data[Loop_INDEX]; else data[Loop_INDEX] = 보관[pożizzjoni++]; }
    }
    static int VALUE(int data_VALUE, boolean 저장여부) { if (저장여부) { 보관[pożizzjoni++] = data_VALUE; return data_VALUE; } return 보관[pożizzjoni++]; }
    static void fittex_pożizzjoni(int 보관칸, boolean 저장여부) {
        pożizzjoni = 보관칸 * 30000;
        ARRAY_VALUE(Memorja_Fajls.현재, 저장여부); Memorja_Fajls.현재길이 = VALUE(Memorja_Fajls.현재길이, 저장여부);
        ARRAY_VALUE(shell_sintassi.변수이름, 저장여부); ARRAY_VALUE(shell_sintassi.변수값, 저장여부); ARRAY_VALUE(shell_sintassi.이름길이, 저장여부); ARRAY_VALUE(shell_sintassi.VALUE_tul, 저장여부);
        shell_sintassi.stat_VALUE = VALUE(shell_sintassi.stat_VALUE, 저장여부);
        ARRAY_VALUE(linja_Editur.LOG_RECORD, 저장여부); ARRAY_VALUE(linja_Editur.LOG_tul, 저장여부); ARRAY_VALUE(linja_Editur.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.linja, 저장여부);
        linja_Editur.LOG_COUNT = VALUE(linja_Editur.LOG_COUNT, 저장여부); linja_Editur.LOG_RECORD_ttermina = VALUE(linja_Editur.LOG_RECORD_ttermina, 저장여부);
        linja_Editur.SEARCH_VALUE = VALUE(linja_Editur.SEARCH_VALUE, 저장여부); linja_Editur.저장길이 = VALUE(linja_Editur.저장길이, 저장여부);
        linja_Editur.daqqas = VALUE(linja_Editur.daqqas, 저장여부); linja_Editur.kerser_VALUE = VALUE(linja_Editur.kerser_VALUE, 저장여부); linja_Editur.Bidu_tieqa = VALUE(linja_Editur.Bidu_tieqa, 저장여부);
        Ħejji[보관칸] = 1;
    }
    static void Proċess_VALUE_entrata() {
        int 사건번호 = bord.Terminal(12); if (사건번호 == 0) return;
        fittex_pożizzjoni(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { bord.kontroll_utent_programm(32 + Loop_INDEX); Ħejji[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Ħejji[Loop_INDEX] = 0;
        }
        int Li_Jmiss_pożizzjoni = (사건번호 & 15) - 1; if (Li_Jmiss_pożizzjoni < 0) Li_Jmiss_pożizzjoni = 0;
        if (Ħejji[Li_Jmiss_pożizzjoni] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Li_Jmiss_pożizzjoni * 30000 + Loop_INDEX] = 0;
        현재 = Li_Jmiss_pożizzjoni; fittex_pożizzjoni(현재, false); bord.Terminal(100 + 현재); 이어읽기 = true;
        단말.kiteb("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (bord.kontroll_utent_programm(16 + 현재) == 0) return false;
        셸입출력.ppermetti_interattiv = true; 셸입출력.serje(false, false); bord.입출력전환(1);
        int 처리값 = bord.kontroll_utent_programm(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; shell_sintassi.stat_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.kiteb("exit "); 단말.수(처리값); 단말.문자(10); bord.Terminal(3); }
        return true;
    }
}
