// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 dop stand_VALUE. Lêer 저장소는 공유하고 Pad/변수/LOG_ry/입력은 분리한다. */
public final class venster_sessie {
    static int[] 보관 = new int[4 * 30000], Maak_gereed = new int[4];
    static int 현재, Posisie;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] data, boolean bêre_VALUE) {
        for (int lus_INDEX = 0; lus_INDEX < data.length; lus_INDEX++) { if (bêre_VALUE) 보관[Posisie++] = data[lus_INDEX]; else data[lus_INDEX] = 보관[Posisie++]; }
    }
    static int VALUE(int data_VALUE, boolean 저장여부) { if (저장여부) { 보관[Posisie++] = data_VALUE; return data_VALUE; } return 보관[Posisie++]; }
    static void soek_plaas(int 보관칸, boolean 저장여부) {
        Posisie = 보관칸 * 30000;
        ARRAY_VALUE(Geheue_Lêers.현재, 저장여부); Geheue_Lêers.현재길이 = VALUE(Geheue_Lêers.현재길이, 저장여부);
        ARRAY_VALUE(dop_sintaksis.변수이름, 저장여부); ARRAY_VALUE(dop_sintaksis.변수값, 저장여부); ARRAY_VALUE(dop_sintaksis.이름길이, 저장여부); ARRAY_VALUE(dop_sintaksis.VALUE_lengte, 저장여부);
        dop_sintaksis.stand_VALUE = VALUE(dop_sintaksis.stand_VALUE, 저장여부);
        ARRAY_VALUE(lyn_Redigeerder.LOG_ry, 저장여부); ARRAY_VALUE(lyn_Redigeerder.LOG_lengte, 저장여부); ARRAY_VALUE(lyn_Redigeerder.bêre_VALUE, 저장여부); ARRAY_VALUE(명령해석기.lyn, 저장여부);
        lyn_Redigeerder.LOG_COUNT = VALUE(lyn_Redigeerder.LOG_COUNT, 저장여부); lyn_Redigeerder.LOG_ry_beëindig = VALUE(lyn_Redigeerder.LOG_ry_beëindig, 저장여부);
        lyn_Redigeerder.Soek_VALUE = VALUE(lyn_Redigeerder.Soek_VALUE, 저장여부); lyn_Redigeerder.저장길이 = VALUE(lyn_Redigeerder.저장길이, 저장여부);
        lyn_Redigeerder.Grootte = VALUE(lyn_Redigeerder.Grootte, 저장여부); lyn_Redigeerder.loper_VALUE = VALUE(lyn_Redigeerder.loper_VALUE, 저장여부); lyn_Redigeerder.BEGIN_venster = VALUE(lyn_Redigeerder.BEGIN_venster, 저장여부);
        Maak_gereed[보관칸] = 1;
    }
    static void Proses_VALUE_inskrywing() {
        int 사건번호 = bord.Terminaal(12); if (사건번호 == 0) return;
        soek_plaas(현재, true);
        for (int lus_INDEX = 0; lus_INDEX < 4; lus_INDEX++) {
            if ((사건번호 & (1 << (8 + lus_INDEX))) != 0) { bord.kontrole_gebruiker_program(32 + lus_INDEX); Maak_gereed[lus_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + lus_INDEX))) != 0 && lus_INDEX != 현재) Maak_gereed[lus_INDEX] = 0;
        }
        int Volgende_plaas = (사건번호 & 15) - 1; if (Volgende_plaas < 0) Volgende_plaas = 0;
        if (Maak_gereed[Volgende_plaas] == 0) for (int lus_INDEX = 0; lus_INDEX < 30000; lus_INDEX++) 보관[Volgende_plaas * 30000 + lus_INDEX] = 0;
        현재 = Volgende_plaas; soek_plaas(현재, false); bord.Terminaal(100 + 현재); 이어읽기 = true;
        단말.Skryf("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (bord.kontrole_gebruiker_program(16 + 현재) == 0) return false;
        셸입출력.toelaat_interaktief = true; 셸입출력.Loop(false, false); bord.입출력전환(1);
        int 처리값 = bord.kontrole_gebruiker_program(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; dop_sintaksis.stand_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Skryf("exit "); 단말.수(처리값); 단말.문자(10); bord.Terminaal(3); }
        return true;
    }
}
