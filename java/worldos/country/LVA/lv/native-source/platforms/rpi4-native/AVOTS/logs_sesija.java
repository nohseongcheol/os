// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 čaula Statuss_VALUE. Fails 저장소는 공유하고 CEĻŠ/mainīgais_VALUE/LOG_RECORD/입력은 분리한다. */
public final class logs_sesija {
    static int[] 보관 = new int[4 * 30000], Sagatavot = new int[4];
    static int pašreizējais_krājums, Novietojums;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] dati, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < dati.length; Loop_INDEX++) { if (Store_VALUE) 보관[Novietojums++] = dati[Loop_INDEX]; else dati[Loop_INDEX] = 보관[Novietojums++]; }
    }
    static int VALUE(int dati_VALUE, boolean 저장여부) { if (저장여부) { 보관[Novietojums++] = dati_VALUE; return dati_VALUE; } return 보관[Novietojums++]; }
    static void meklēt_amats(int 보관칸, boolean 저장여부) {
        Novietojums = 보관칸 * 30000;
        ARRAY_VALUE(atmiņa_Faili.pašreizējais_krājums, 저장여부); atmiņa_Faili.현재길이 = VALUE(atmiņa_Faili.현재길이, 저장여부);
        ARRAY_VALUE(čaula_sintakse.mainīgais_nosaukums, 저장여부); ARRAY_VALUE(čaula_sintakse.mainīgais_dati, 저장여부); ARRAY_VALUE(čaula_sintakse.이름길이, 저장여부); ARRAY_VALUE(čaula_sintakse.값길이, 저장여부);
        čaula_sintakse.Statuss_VALUE = VALUE(čaula_sintakse.Statuss_VALUE, 저장여부);
        ARRAY_VALUE(rindiņas_redaktors.LOG_RECORD, 저장여부); ARRAY_VALUE(rindiņas_redaktors.기록길이, 저장여부); ARRAY_VALUE(rindiņas_redaktors.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Līniju, 저장여부);
        rindiņas_redaktors.LOG_COUNT = VALUE(rindiņas_redaktors.LOG_COUNT, 저장여부); rindiņas_redaktors.LOG_RECORD_beigt_zvanu = VALUE(rindiņas_redaktors.LOG_RECORD_beigt_zvanu, 저장여부);
        rindiņas_redaktors.Meklēt_VALUE = VALUE(rindiņas_redaktors.Meklēt_VALUE, 저장여부); rindiņas_redaktors.저장길이 = VALUE(rindiņas_redaktors.저장길이, 저장여부);
        rindiņas_redaktors.Izmērs = VALUE(rindiņas_redaktors.Izmērs, 저장여부); rindiņas_redaktors.kursors_VALUE = VALUE(rindiņas_redaktors.kursors_VALUE, 저장여부); rindiņas_redaktors.Sākt_logs = VALUE(rindiņas_redaktors.Sākt_logs, 저장여부);
        Sagatavot[보관칸] = 1;
    }
    static void Process_VALUE_ievade() {
        int notikums_numurs = Panelis.Terminālis(12); if (notikums_numurs == 0) return;
        meklēt_amats(pašreizējais_krājums, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((notikums_numurs & (1 << (8 + Loop_INDEX))) != 0) { Panelis.vadība_lietotājs_programma(32 + Loop_INDEX); Sagatavot[Loop_INDEX] = 0; }
            if ((notikums_numurs & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != pašreizējais_krājums) Sagatavot[Loop_INDEX] = 0;
        }
        int Tālāk_amats = (notikums_numurs & 15) - 1; if (Tālāk_amats < 0) Tālāk_amats = 0;
        if (Sagatavot[Tālāk_amats] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Tālāk_amats * 30000 + Loop_INDEX] = 0;
        pašreizējais_krājums = Tālāk_amats; meklēt_amats(pašreizējais_krājums, false); Panelis.Terminālis(100 + pašreizējais_krājums); 이어읽기 = true;
        단말.Rakstīt("\nTERMINAL FOCUS "); 단말.numurs(pašreizējais_krājums + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Panelis.vadība_lietotājs_programma(16 + pašreizējais_krājums) == 0) return false;
        셸입출력.대화허용 = true; 셸입출력.Palaist(false, false); Panelis.입출력전환(1);
        int 처리값 = Panelis.vadība_lietotājs_programma(pašreizējais_krājums); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; čaula_sintakse.Statuss_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Rakstīt("exit "); 단말.numurs(처리값); 단말.문자(10); Panelis.Terminālis(3); }
        return true;
    }
}
