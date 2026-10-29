// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 cragen cyflwr_VALUE. Ffeil 저장소는 공유하고 LLWYBR/변수/LOG_rhes/입력은 분리한다. */
public final class ffenestr_sesiwn {
    static int[] 보관 = new int[4 * 30000], Paratoi = new int[4];
    static int 현재, safle;
    static boolean 이어읽기;
    static void ARAE_VALUE(int[] data, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < data.length; Loop_INDEX++) { if (Store_VALUE) 보관[safle++] = data[Loop_INDEX]; else data[Loop_INDEX] = 보관[safle++]; }
    }
    static int VALUE(int data_VALUE, boolean 저장여부) { if (저장여부) { 보관[safle++] = data_VALUE; return data_VALUE; } return 보관[safle++]; }
    static void chwilio_safle(int 보관칸, boolean 저장여부) {
        safle = 보관칸 * 30000;
        ARAE_VALUE(Cof_Ffeil.현재, 저장여부); Cof_Ffeil.현재길이 = VALUE(Cof_Ffeil.현재길이, 저장여부);
        ARAE_VALUE(cragen_cystrawen.변수이름, 저장여부); ARAE_VALUE(cragen_cystrawen.변수값, 저장여부); ARAE_VALUE(cragen_cystrawen.이름길이, 저장여부); ARAE_VALUE(cragen_cystrawen.VALUE_hyd, 저장여부);
        cragen_cystrawen.cyflwr_VALUE = VALUE(cragen_cystrawen.cyflwr_VALUE, 저장여부);
        ARAE_VALUE(llinell_Editor.LOG_rhes, 저장여부); ARAE_VALUE(llinell_Editor.LOG_hyd, 저장여부); ARAE_VALUE(llinell_Editor.Store_VALUE, 저장여부); ARAE_VALUE(명령해석기.llinell, 저장여부);
        llinell_Editor.LOG_COUNT = VALUE(llinell_Editor.LOG_COUNT, 저장여부); llinell_Editor.LOG_rhes_gorffen = VALUE(llinell_Editor.LOG_rhes_gorffen, 저장여부);
        llinell_Editor.SEARCH_VALUE = VALUE(llinell_Editor.SEARCH_VALUE, 저장여부); llinell_Editor.저장길이 = VALUE(llinell_Editor.저장길이, 저장여부);
        llinell_Editor.Maint = VALUE(llinell_Editor.Maint, 저장여부); llinell_Editor.cyrchwr_VALUE = VALUE(llinell_Editor.cyrchwr_VALUE, 저장여부); llinell_Editor.START_ffenestr = VALUE(llinell_Editor.START_ffenestr, 저장여부);
        Paratoi[보관칸] = 1;
    }
    static void Proses_VALUE_cofnod() {
        int 사건번호 = bwrdd.Terfynell(12); if (사건번호 == 0) return;
        chwilio_safle(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { bwrdd.rheoli_defnyddiwr_Rhaglen(32 + Loop_INDEX); Paratoi[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Paratoi[Loop_INDEX] = 0;
        }
        int Nesaf_safle = (사건번호 & 15) - 1; if (Nesaf_safle < 0) Nesaf_safle = 0;
        if (Paratoi[Nesaf_safle] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Nesaf_safle * 30000 + Loop_INDEX] = 0;
        현재 = Nesaf_safle; chwilio_safle(현재, false); bwrdd.Terfynell(100 + 현재); 이어읽기 = true;
        단말.Ysgrifennu("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (bwrdd.rheoli_defnyddiwr_Rhaglen(16 + 현재) == 0) return false;
        셸입출력.Caniatáu_rhyngweithiol = true; 셸입출력.Gweithredu_2(false, false); bwrdd.입출력전환(1);
        int 처리값 = bwrdd.rheoli_defnyddiwr_Rhaglen(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; cragen_cystrawen.cyflwr_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Ysgrifennu("exit "); 단말.수(처리값); 단말.문자(10); bwrdd.Terfynell(3); }
        return true;
    }
}
