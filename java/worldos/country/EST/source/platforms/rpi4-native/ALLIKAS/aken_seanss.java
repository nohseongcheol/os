// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 kest Olek_VALUE. Fail 저장소는 공유하고 RADA/변수/LOG_kirje/입력은 분리한다. */
public final class aken_seanss {
    static int[] 보관 = new int[4 * 30000], Ettevalmistamine = new int[4];
    static int tähtaja_piires_kaup, Asukoht;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] andmed, boolean salv_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < andmed.length; Loop_INDEX++) { if (salv_VALUE) 보관[Asukoht++] = andmed[Loop_INDEX]; else andmed[Loop_INDEX] = 보관[Asukoht++]; }
    }
    static int VALUE(int andmed_VALUE, boolean 저장여부) { if (저장여부) { 보관[Asukoht++] = andmed_VALUE; return andmed_VALUE; } return 보관[Asukoht++]; }
    static void otsima_ametikoht(int 보관칸, boolean 저장여부) {
        Asukoht = 보관칸 * 30000;
        ARRAY_VALUE(Mälu_Failid.tähtaja_piires_kaup, 저장여부); Mälu_Failid.현재길이 = VALUE(Mälu_Failid.현재길이, 저장여부);
        ARRAY_VALUE(kest_süntaks.변수이름, 저장여부); ARRAY_VALUE(kest_süntaks.변수값, 저장여부); ARRAY_VALUE(kest_süntaks.이름길이, 저장여부); ARRAY_VALUE(kest_süntaks.값길이, 저장여부);
        kest_süntaks.Olek_VALUE = VALUE(kest_süntaks.Olek_VALUE, 저장여부);
        ARRAY_VALUE(rearedaktor.LOG_kirje, 저장여부); ARRAY_VALUE(rearedaktor.기록길이, 저장여부); ARRAY_VALUE(rearedaktor.salv_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Joon, 저장여부);
        rearedaktor.LOG_COUNT = VALUE(rearedaktor.LOG_COUNT, 저장여부); rearedaktor.LOG_kirje_lõpeta_kõne = VALUE(rearedaktor.LOG_kirje_lõpeta_kõne, 저장여부);
        rearedaktor.Otsi_VALUE = VALUE(rearedaktor.Otsi_VALUE, 저장여부); rearedaktor.저장길이 = VALUE(rearedaktor.저장길이, 저장여부);
        rearedaktor.Suurus = VALUE(rearedaktor.Suurus, 저장여부); rearedaktor.kursor_VALUE = VALUE(rearedaktor.kursor_VALUE, 저장여부); rearedaktor.START_aken = VALUE(rearedaktor.START_aken, 저장여부);
        Ettevalmistamine[보관칸] = 1;
    }
    static void Joonis_VALUE_kirje() {
        int sündmus_number = Tahvel.terminal(12); if (sündmus_number == 0) return;
        otsima_ametikoht(tähtaja_piires_kaup, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((sündmus_number & (1 << (8 + Loop_INDEX))) != 0) { Tahvel.meede_kasutaja_programm(32 + Loop_INDEX); Ettevalmistamine[Loop_INDEX] = 0; }
            if ((sündmus_number & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != tähtaja_piires_kaup) Ettevalmistamine[Loop_INDEX] = 0;
        }
        int Edasi_ametikoht = (sündmus_number & 15) - 1; if (Edasi_ametikoht < 0) Edasi_ametikoht = 0;
        if (Ettevalmistamine[Edasi_ametikoht] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Edasi_ametikoht * 30000 + Loop_INDEX] = 0;
        tähtaja_piires_kaup = Edasi_ametikoht; otsima_ametikoht(tähtaja_piires_kaup, false); Tahvel.terminal(100 + tähtaja_piires_kaup); 이어읽기 = true;
        단말.Kirjutamine("\nTERMINAL FOCUS "); 단말.number(tähtaja_piires_kaup + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Tahvel.meede_kasutaja_programm(16 + tähtaja_piires_kaup) == 0) return false;
        셸입출력.대화허용 = true; 셸입출력.Käivita_2(false, false); Tahvel.입출력전환(1);
        int 처리값 = Tahvel.meede_kasutaja_programm(tähtaja_piires_kaup); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; kest_süntaks.Olek_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Kirjutamine("exit "); 단말.number(처리값); 단말.문자(10); Tahvel.terminal(3); }
        return true;
    }
}
