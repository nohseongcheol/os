// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 skel staða_VALUE_e10195a1. Skrá 저장소는 공유하고 SLÓÐ/변수/LOG_lína/입력은 분리한다. */
public final class gluggi_lota {
    static int[] 보관 = new int[4 * 30000], Undirbúa = new int[4];
    static int 현재, Staðsetning;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] gögn, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < gögn.length; Loop_INDEX++) { if (Store_VALUE) 보관[Staðsetning++] = gögn[Loop_INDEX]; else gögn[Loop_INDEX] = 보관[Staðsetning++]; }
    }
    static int VALUE(int gögn_VALUE, boolean 저장여부) { if (저장여부) { 보관[Staðsetning++] = gögn_VALUE; return gögn_VALUE; } return 보관[Staðsetning++]; }
    static void leita_staða(int 보관칸, boolean 저장여부) {
        Staðsetning = 보관칸 * 30000;
        ARRAY_VALUE(Minni_Skrár.현재, 저장여부); Minni_Skrár.현재길이 = VALUE(Minni_Skrár.현재길이, 저장여부);
        ARRAY_VALUE(skel_málskipan.변수이름, 저장여부); ARRAY_VALUE(skel_málskipan.변수값, 저장여부); ARRAY_VALUE(skel_málskipan.이름길이, 저장여부); ARRAY_VALUE(skel_málskipan.VALUE_lengd, 저장여부);
        skel_málskipan.staða_VALUE_e10195a1 = VALUE(skel_málskipan.staða_VALUE_e10195a1, 저장여부);
        ARRAY_VALUE(lína_ritill.LOG_lína, 저장여부); ARRAY_VALUE(lína_ritill.LOG_lengd, 저장여부); ARRAY_VALUE(lína_ritill.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Lína, 저장여부);
        lína_ritill.LOG_COUNT = VALUE(lína_ritill.LOG_COUNT, 저장여부); lína_ritill.LOG_lína_ljúka = VALUE(lína_ritill.LOG_lína_ljúka, 저장여부);
        lína_ritill.Leit_VALUE = VALUE(lína_ritill.Leit_VALUE, 저장여부); lína_ritill.저장길이 = VALUE(lína_ritill.저장길이, 저장여부);
        lína_ritill.Stærð = VALUE(lína_ritill.Stærð, 저장여부); lína_ritill.bendill_VALUE = VALUE(lína_ritill.bendill_VALUE, 저장여부); lína_ritill.Opna_gluggi = VALUE(lína_ritill.Opna_gluggi, 저장여부);
        Undirbúa[보관칸] = 1;
    }
    static void Ferli_VALUE_færsla() {
        int atvik_númer = bretti.Skjáhermir(12); if (atvik_númer == 0) return;
        leita_staða(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((atvik_númer & (1 << (8 + Loop_INDEX))) != 0) { bretti.stýring_notandi_forrit(32 + Loop_INDEX); Undirbúa[Loop_INDEX] = 0; }
            if ((atvik_númer & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Undirbúa[Loop_INDEX] = 0;
        }
        int Áfram_staða = (atvik_númer & 15) - 1; if (Áfram_staða < 0) Áfram_staða = 0;
        if (Undirbúa[Áfram_staða] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Áfram_staða * 30000 + Loop_INDEX] = 0;
        현재 = Áfram_staða; leita_staða(현재, false); bretti.Skjáhermir(100 + 현재); 이어읽기 = true;
        단말.Skrift("\nTERMINAL FOCUS "); 단말.númer(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (bretti.stýring_notandi_forrit(16 + 현재) == 0) return false;
        셸입출력.leyfa_gagnvirkur = true; 셸입출력.Keyra_2(false, false); bretti.입출력전환(1);
        int 처리값 = bretti.stýring_notandi_forrit(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; skel_málskipan.staða_VALUE_e10195a1 = 처리값 < 0 ? 126 : 처리값; 단말.Skrift("exit "); 단말.númer(처리값); 단말.문자(10); bretti.Skjáhermir(3); }
        return true;
    }
}
