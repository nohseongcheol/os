// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 grensesnitt status_VALUE. Fil 저장소는 공유하고 STIGE/variabel_VALUE/LOG_rad/입력은 분리한다. */
public final class vindauge_økt {
    static int[] 보관 = new int[4 * 30000], Klargjer = new int[4];
    static int betalt_vare, Posisjon;
    static boolean 이어읽기;
    static void ARRAY_VALUE(int[] data, boolean Store_VALUE) {
        for (int Loop_INDEX = 0; Loop_INDEX < data.length; Loop_INDEX++) { if (Store_VALUE) 보관[Posisjon++] = data[Loop_INDEX]; else data[Loop_INDEX] = 보관[Posisjon++]; }
    }
    static int VALUE(int data_VALUE, boolean 저장여부) { if (저장여부) { 보관[Posisjon++] = data_VALUE; return data_VALUE; } return 보관[Posisjon++]; }
    static void søk_plassere(int 보관칸, boolean 저장여부) {
        Posisjon = 보관칸 * 30000;
        ARRAY_VALUE(Minne_Filer.betalt_vare, 저장여부); Minne_Filer.betalt_lengd = VALUE(Minne_Filer.betalt_lengd, 저장여부);
        ARRAY_VALUE(grensesnitt_syntaks.variabel_namn, 저장여부); ARRAY_VALUE(grensesnitt_syntaks.variabel_data, 저장여부); ARRAY_VALUE(grensesnitt_syntaks.이름길이, 저장여부); ARRAY_VALUE(grensesnitt_syntaks.VALUE_lengd, 저장여부);
        grensesnitt_syntaks.status_VALUE = VALUE(grensesnitt_syntaks.status_VALUE, 저장여부);
        ARRAY_VALUE(line_Redaktør.LOG_rad, 저장여부); ARRAY_VALUE(line_Redaktør.LOG_lengd, 저장여부); ARRAY_VALUE(line_Redaktør.Store_VALUE, 저장여부); ARRAY_VALUE(명령해석기.linje, 저장여부);
        line_Redaktør.LOG_COUNT = VALUE(line_Redaktør.LOG_COUNT, 저장여부); line_Redaktør.LOG_rad_avslutte = VALUE(line_Redaktør.LOG_rad_avslutte, 저장여부);
        line_Redaktør.Søk_VALUE = VALUE(line_Redaktør.Søk_VALUE, 저장여부); line_Redaktør.저장길이 = VALUE(line_Redaktør.저장길이, 저장여부);
        line_Redaktør.Storleik = VALUE(line_Redaktør.Storleik, 저장여부); line_Redaktør.markør_VALUE = VALUE(line_Redaktør.markør_VALUE, 저장여부); line_Redaktør.START_vindauge = VALUE(line_Redaktør.START_vindauge, 저장여부);
        Klargjer[보관칸] = 1;
    }
    static void Prosess_VALUE_oppføring() {
        int 사건번호 = Tavle.Terminal(12); if (사건번호 == 0) return;
        søk_plassere(betalt_vare, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Tavle.styring_brukar_app(32 + Loop_INDEX); Klargjer[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != betalt_vare) Klargjer[Loop_INDEX] = 0;
        }
        int Neste_plassere = (사건번호 & 15) - 1; if (Neste_plassere < 0) Neste_plassere = 0;
        if (Klargjer[Neste_plassere] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Neste_plassere * 30000 + Loop_INDEX] = 0;
        betalt_vare = Neste_plassere; søk_plassere(betalt_vare, false); Tavle.Terminal(100 + betalt_vare); 이어읽기 = true;
        단말.Skriv("\nTERMINAL FOCUS "); 단말.수(betalt_vare + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Tavle.styring_brukar_app(16 + betalt_vare) == 0) return false;
        셸입출력.Tillat_interaktiv = true; 셸입출력.Køyr_2(false, false); Tavle.입출력전환(1);
        int 처리값 = Tavle.styring_brukar_app(betalt_vare); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; grensesnitt_syntaks.status_VALUE = 처리값 < 0 ? 126 : 처리값; 단말.Skriv("exit "); 단말.수(처리값); 단말.문자(10); Tavle.Terminal(3); }
        return true;
    }
}
