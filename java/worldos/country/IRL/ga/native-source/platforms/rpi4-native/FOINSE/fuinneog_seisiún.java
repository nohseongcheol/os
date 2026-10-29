// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 blaosc staid_VALUE. Comhad 저장소는 공유하고 CONAIR/변수/LOG_ró/입력은 분리한다. */
public final class fuinneog_seisiún {
    static int[] 보관 = new int[4 * 30000], Ullmhaigh = new int[4];
    static int 현재, suíomh;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] sonraí, boolean Store_VALUE) {
        for (int lúb_INDEX = 0; lúb_INDEX < sonraí.length; lúb_INDEX++) { if (Store_VALUE) 보관[suíomh++] = sonraí[lúb_INDEX]; else sonraí[lúb_INDEX] = 보관[suíomh++]; }
    }
    static int VALUE(int sonraí_VALUE, boolean 저장여부) { if (저장여부) { 보관[suíomh++] = sonraí_VALUE; return sonraí_VALUE; } return 보관[suíomh++]; }
    static void lorg_suíomh(int 보관칸, boolean 저장여부) {
        suíomh = 보관칸 * 30000;
        ARRAY_VALUE(Cuimhne_Comhaid.현재, 저장여부); Cuimhne_Comhaid.현재길이 = VALUE(Cuimhne_Comhaid.현재길이, 저장여부);
        ARRAY_VALUE(blaosc_comhréir.변수이름, 저장여부); ARRAY_VALUE(blaosc_comhréir.변수값, 저장여부); ARRAY_VALUE(blaosc_comhréir.이름길이, 저장여부); ARRAY_VALUE(blaosc_comhréir.VALUE_fad, 저장여부);
        blaosc_comhréir.staid_VALUE = VALUE(blaosc_comhréir.staid_VALUE, 저장여부);
        ARRAY_VALUE(líne_Eagarthóir.LOG_ró, 저장여부); ARRAY_VALUE(líne_Eagarthóir.LOG_fad, 저장여부); ARRAY_VALUE(líne_Eagarthóir.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Líne, 저장여부);
        líne_Eagarthóir.LOG_COUNT = VALUE(líne_Eagarthóir.LOG_COUNT, 저장여부); líne_Eagarthóir.LOG_ró_cuir_deireadh_le = VALUE(líne_Eagarthóir.LOG_ró_cuir_deireadh_le, 저장여부);
        líne_Eagarthóir.SEARCH_VALUE = VALUE(líne_Eagarthóir.SEARCH_VALUE, 저장여부); líne_Eagarthóir.저장길이 = VALUE(líne_Eagarthóir.저장길이, 저장여부);
        líne_Eagarthóir.Méid = VALUE(líne_Eagarthóir.Méid, 저장여부); líne_Eagarthóir.cúrsóir_VALUE = VALUE(líne_Eagarthóir.cúrsóir_VALUE, 저장여부); líne_Eagarthóir.Start_fuinneog = VALUE(líne_Eagarthóir.Start_fuinneog, 저장여부);
        Ullmhaigh[보관칸] = 1;
    }
    static void Próiseas_VALUE_iontráil() {
        int 사건번호 = clár.Teirminéal(12); if (사건번호 == 0) return;
        lorg_suíomh(현재, true);
        for (int lúb_INDEX = 0; lúb_INDEX < 4; lúb_INDEX++) {
            if ((사건번호 & (1 << (8 + lúb_INDEX))) != 0) { clár.rialú_úsáideoir_clár(32 + lúb_INDEX); Ullmhaigh[lúb_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + lúb_INDEX))) != 0 && lúb_INDEX != 현재) Ullmhaigh[lúb_INDEX] = 0;
        }
        int Ar_aghaidh_suíomh = (사건번호 & 15) - 1; if (Ar_aghaidh_suíomh < 0) Ar_aghaidh_suíomh = 0;
        if (Ullmhaigh[Ar_aghaidh_suíomh] == 0) for (int lúb_INDEX = 0; lúb_INDEX < 30000; lúb_INDEX++) 보관[Ar_aghaidh_suíomh * 30000 + lúb_INDEX] = 0;
        현재 = Ar_aghaidh_suíomh; lorg_suíomh(현재, false); clár.Teirminéal(100 + 현재); 이어읽기 = true;
        단말.Scríobh("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (clár.rialú_úsáideoir_clár(16 + 현재) == 0) return false;
        셸입출력.Ceadaigh_idirghníomhach = true; 셸입출력.Rith_2(false, false); clár.입출력전환(1);
        int 처리값 = clár.rialú_úsáideoir_clár(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; blaosc_comhréir.staid_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Scríobh("exit "); 단말.수(처리값); 단말.문자(10); clár.Teirminéal(3); }
        return true;
    }
}
