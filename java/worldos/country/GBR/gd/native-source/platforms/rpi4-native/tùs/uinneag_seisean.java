// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 slige cor_VALUE. faidhle 저장소는 공유하고 Slighe/변수/LOG_ràgh/입력은 분리한다. */
public final class uinneag_seisean {
    static int[] 보관 = new int[4 * 30000], Ullaich = new int[4];
    static int 현재, suidhich;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] dàta, boolean Store_VALUE) {
        for (int lùb_INDEX = 0; lùb_INDEX < dàta.length; lùb_INDEX++) { if (Store_VALUE) 보관[suidhich++] = dàta[lùb_INDEX]; else dàta[lùb_INDEX] = 보관[suidhich++]; }
    }
    static int VALUE(int dàta_VALUE, boolean 저장여부) { if (저장여부) { 보관[suidhich++] = dàta_VALUE; return dàta_VALUE; } return 보관[suidhich++]; }
    static void sir_suidhich(int 보관칸, boolean 저장여부) {
        suidhich = 보관칸 * 30000;
        ARRAY_VALUE(cuimhne_faidhlichean.현재, 저장여부); cuimhne_faidhlichean.현재길이 = VALUE(cuimhne_faidhlichean.현재길이, 저장여부);
        ARRAY_VALUE(셸문법.변수이름, 저장여부); ARRAY_VALUE(셸문법.변수값, 저장여부); ARRAY_VALUE(셸문법.이름길이, 저장여부); ARRAY_VALUE(셸문법.VALUE_faid, 저장여부);
        셸문법.cor_VALUE = VALUE(셸문법.cor_VALUE, 저장여부);
        ARRAY_VALUE(loidhne_deasaiche.LOG_ràgh, 저장여부); ARRAY_VALUE(loidhne_deasaiche.LOG_faid, 저장여부); ARRAY_VALUE(loidhne_deasaiche.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.loidhne, 저장여부);
        loidhne_deasaiche.LOG_COUNT = VALUE(loidhne_deasaiche.LOG_COUNT, 저장여부); loidhne_deasaiche.LOG_ràgh_crìochnaich = VALUE(loidhne_deasaiche.LOG_ràgh_crìochnaich, 저장여부);
        loidhne_deasaiche.lorg_VALUE = VALUE(loidhne_deasaiche.lorg_VALUE, 저장여부); loidhne_deasaiche.저장길이 = VALUE(loidhne_deasaiche.저장길이, 저장여부);
        loidhne_deasaiche.atharraich_am_meud = VALUE(loidhne_deasaiche.atharraich_am_meud, 저장여부); loidhne_deasaiche.cursair_VALUE = VALUE(loidhne_deasaiche.cursair_VALUE, 저장여부); loidhne_deasaiche.Start_uinneag = VALUE(loidhne_deasaiche.Start_uinneag, 저장여부);
        Ullaich[보관칸] = 1;
    }
    static void Pròiseas_VALUE_cur_a_steach() {
        int 사건번호 = bòrd.tèirmineal(12); if (사건번호 == 0) return;
        sir_suidhich(현재, true);
        for (int lùb_INDEX = 0; lùb_INDEX < 4; lùb_INDEX++) {
            if ((사건번호 & (1 << (8 + lùb_INDEX))) != 0) { bòrd.smachd_cleachdaiche_ap(32 + lùb_INDEX); Ullaich[lùb_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + lùb_INDEX))) != 0 && lùb_INDEX != 현재) Ullaich[lùb_INDEX] = 0;
        }
        int air_adhart_suidhich = (사건번호 & 15) - 1; if (air_adhart_suidhich < 0) air_adhart_suidhich = 0;
        if (Ullaich[air_adhart_suidhich] == 0) for (int lùb_INDEX = 0; lùb_INDEX < 30000; lùb_INDEX++) 보관[air_adhart_suidhich * 30000 + lùb_INDEX] = 0;
        현재 = air_adhart_suidhich; sir_suidhich(현재, false); bòrd.tèirmineal(100 + 현재); 이어읽기 = true;
        단말.sgrìobh("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (bòrd.smachd_cleachdaiche_ap(16 + 현재) == 0) return false;
        셸입출력.Ceadaich_eadar_ghnìomhach = true; 셸입출력.ruith(false, false); bòrd.입출력전환(1);
        int 처리값 = bòrd.smachd_cleachdaiche_ap(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; 셸문법.cor_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.sgrìobh("exit "); 단말.수(처리값); 단말.문자(10); bòrd.tèirmineal(3); }
        return true;
    }
}
