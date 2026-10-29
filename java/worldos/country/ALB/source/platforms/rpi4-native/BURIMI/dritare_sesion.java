// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 pasues status_VALUE. Kartelë 저장소는 공유하고 POZICIONI/변수/LOG_RECORD/입력은 분리한다. */
public final class dritare_sesion {
    static int[] 보관 = new int[4 * 30000], Përgatit = new int[4];
    static int 현재, Pozicioni;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] të_dhëna, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < të_dhëna.length; Loop_INDEX++) { if (Store_VALUE) 보관[Pozicioni++] = të_dhëna[Loop_INDEX]; else të_dhëna[Loop_INDEX] = 보관[Pozicioni++]; }
    }
    static int VALUE(int të_dhëna_VALUE, boolean 저장여부) { if (저장여부) { 보관[Pozicioni++] = të_dhëna_VALUE; return të_dhëna_VALUE; } return 보관[Pozicioni++]; }
    static void kërko_pozicioni(int 보관칸, boolean 저장여부) {
        Pozicioni = 보관칸 * 30000;
        ARRAY_VALUE(Memorie_Skedarët.현재, 저장여부); Memorie_Skedarët.현재길이 = VALUE(Memorie_Skedarët.현재길이, 저장여부);
        ARRAY_VALUE(pasues_sintaksë.변수이름, 저장여부); ARRAY_VALUE(pasues_sintaksë.변수값, 저장여부); ARRAY_VALUE(pasues_sintaksë.이름길이, 저장여부); ARRAY_VALUE(pasues_sintaksë.VALUE_gjatësi, 저장여부);
        pasues_sintaksë.status_VALUE = VALUE(pasues_sintaksë.status_VALUE, 저장여부);
        ARRAY_VALUE(linjë_Redaktori.LOG_RECORD, 저장여부); ARRAY_VALUE(linjë_Redaktori.LOG_gjatësi, 저장여부); ARRAY_VALUE(linjë_Redaktori.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.linjë, 저장여부);
        linjë_Redaktori.LOG_COUNT = VALUE(linjë_Redaktori.LOG_COUNT, 저장여부); linjë_Redaktori.LOG_RECORD_mbaroj = VALUE(linjë_Redaktori.LOG_RECORD_mbaroj, 저장여부);
        linjë_Redaktori.Kërkim_VALUE = VALUE(linjë_Redaktori.Kërkim_VALUE, 저장여부); linjë_Redaktori.저장길이 = VALUE(linjë_Redaktori.저장길이, 저장여부);
        linjë_Redaktori.Madhësi = VALUE(linjë_Redaktori.Madhësi, 저장여부); linjë_Redaktori.kursor_VALUE = VALUE(linjë_Redaktori.kursor_VALUE, 저장여부); linjë_Redaktori.nis_dritare = VALUE(linjë_Redaktori.nis_dritare, 저장여부);
        Përgatit[보관칸] = 1;
    }
    static void Proces_VALUE_futje() {
        int 사건번호 = panel.Terminali(12); if (사건번호 == 0) return;
        kërko_pozicioni(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { panel.kontroll_përdorues_program(32 + Loop_INDEX); Përgatit[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Përgatit[Loop_INDEX] = 0;
        }
        int Tjetër_pozicioni = (사건번호 & 15) - 1; if (Tjetër_pozicioni < 0) Tjetër_pozicioni = 0;
        if (Përgatit[Tjetër_pozicioni] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Tjetër_pozicioni * 30000 + Loop_INDEX] = 0;
        현재 = Tjetër_pozicioni; kërko_pozicioni(현재, false); panel.Terminali(100 + 현재); 이어읽기 = true;
        단말.Shkrimi("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (panel.kontroll_përdorues_program(16 + 현재) == 0) return false;
        셸입출력.Lejoj_ndërvepruese = true; 셸입출력.Ekzekuto(false, false); panel.입출력전환(1);
        int 처리값 = panel.kontroll_përdorues_program(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; pasues_sintaksë.status_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Shkrimi("exit "); 단말.수(처리값); 단말.문자(10); panel.Terminali(3); }
        return true;
    }
}
