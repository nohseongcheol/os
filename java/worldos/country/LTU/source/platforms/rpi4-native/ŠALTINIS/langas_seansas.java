// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 apvalkalas Būsena_VALUE. Failas 저장소는 공유하고 KELIAS/kintamasis_VALUE/LOG_RECORD/입력은 분리한다. */
public final class langas_seansas {
    static int[] 보관 = new int[4 * 30000], Parengti = new int[4];
    static int dabartinis_prekė, Pozicija;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] duomenys, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < duomenys.length; Loop_INDEX++) { if (Store_VALUE) 보관[Pozicija++] = duomenys[Loop_INDEX]; else duomenys[Loop_INDEX] = 보관[Pozicija++]; }
    }
    static int VALUE(int duomenys_VALUE, boolean 저장여부) { if (저장여부) { 보관[Pozicija++] = duomenys_VALUE; return duomenys_VALUE; } return 보관[Pozicija++]; }
    static void ieškoti_padėtis(int 보관칸, boolean 저장여부) {
        Pozicija = 보관칸 * 30000;
        ARRAY_VALUE(atmintis_Failai.dabartinis_prekė, 저장여부); atmintis_Failai.현재길이 = VALUE(atmintis_Failai.현재길이, 저장여부);
        ARRAY_VALUE(apvalkalas_sintaksė.kintamasis_pavadinimas, 저장여부); ARRAY_VALUE(apvalkalas_sintaksė.kintamasis_duomenys, 저장여부); ARRAY_VALUE(apvalkalas_sintaksė.이름길이, 저장여부); ARRAY_VALUE(apvalkalas_sintaksė.값길이, 저장여부);
        apvalkalas_sintaksė.Būsena_VALUE = VALUE(apvalkalas_sintaksė.Būsena_VALUE, 저장여부);
        ARRAY_VALUE(eilutinė_rengyklė.LOG_RECORD, 저장여부); ARRAY_VALUE(eilutinė_rengyklė.기록길이, 저장여부); ARRAY_VALUE(eilutinė_rengyklė.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.Eilutė, 저장여부);
        eilutinė_rengyklė.LOG_COUNT = VALUE(eilutinė_rengyklė.LOG_COUNT, 저장여부); eilutinė_rengyklė.LOG_RECORD_baigti_pokalbį = VALUE(eilutinė_rengyklė.LOG_RECORD_baigti_pokalbį, 저장여부);
        eilutinė_rengyklė.Ieška_VALUE = VALUE(eilutinė_rengyklė.Ieška_VALUE, 저장여부); eilutinė_rengyklė.저장길이 = VALUE(eilutinė_rengyklė.저장길이, 저장여부);
        eilutinė_rengyklė.Dydis = VALUE(eilutinė_rengyklė.Dydis, 저장여부); eilutinė_rengyklė.žymiklis_VALUE = VALUE(eilutinė_rengyklė.žymiklis_VALUE, 저장여부); eilutinė_rengyklė.Start_langas = VALUE(eilutinė_rengyklė.Start_langas, 저장여부);
        Parengti[보관칸] = 1;
    }
    static void Procesas_VALUE_įrašas() {
        int įvykis_numeris = Lenta.Terminalas(12); if (įvykis_numeris == 0) return;
        ieškoti_padėtis(dabartinis_prekė, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((įvykis_numeris & (1 << (8 + Loop_INDEX))) != 0) { Lenta.valdymas_naudotojas_programa(32 + Loop_INDEX); Parengti[Loop_INDEX] = 0; }
            if ((įvykis_numeris & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != dabartinis_prekė) Parengti[Loop_INDEX] = 0;
        }
        int toliau_padėtis = (įvykis_numeris & 15) - 1; if (toliau_padėtis < 0) toliau_padėtis = 0;
        if (Parengti[toliau_padėtis] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[toliau_padėtis * 30000 + Loop_INDEX] = 0;
        dabartinis_prekė = toliau_padėtis; ieškoti_padėtis(dabartinis_prekė, false); Lenta.Terminalas(100 + dabartinis_prekė); 이어읽기 = true;
        단말.Rašymas("\nTERMINAL FOCUS "); 단말.numeris(dabartinis_prekė + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Lenta.valdymas_naudotojas_programa(16 + dabartinis_prekė) == 0) return false;
        셸입출력.대화허용 = true; 셸입출력.Paleisti(false, false); Lenta.입출력전환(1);
        int 처리값 = Lenta.valdymas_naudotojas_programa(dabartinis_prekė); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; apvalkalas_sintaksė.Būsena_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Rašymas("exit "); 단말.numeris(처리값); 단말.문자(10); Lenta.Terminalas(3); }
        return true;
    }
}
