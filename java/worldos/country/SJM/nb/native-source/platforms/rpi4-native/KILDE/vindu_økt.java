// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 Shell status_VERDI. Fil 저장소는 공유하고 Sti/variabel_VERDI/LOG_POST/입력은 분리한다. */
public final class vindu_økt {
    static int[] 보관 = new int[4 * 30000], Forbered = new int[4];
    static int betalt_vare, Posisjon;
    static boolean 이어읽기;
    static void MATRISE_VERDI(int[] data, boolean Store_VERDI) {
        for (int Loop_INDEKS = 0; Loop_INDEKS < data.length; Loop_INDEKS++) { if (Store_VERDI) 보관[Posisjon++] = data[Loop_INDEKS]; else data[Loop_INDEKS] = 보관[Posisjon++]; }
    }
    static int VERDI(int data_VERDI, boolean 저장여부) { if (저장여부) { 보관[Posisjon++] = data_VERDI; return data_VERDI; } return 보관[Posisjon++]; }
    static void søk_plassere(int 보관칸, boolean 저장여부) {
        Posisjon = 보관칸 * 30000;
        MATRISE_VERDI(Minne_Filer.betalt_vare, 저장여부); Minne_Filer.betalt_lengde = VERDI(Minne_Filer.betalt_lengde, 저장여부);
        MATRISE_VERDI(Shell_syntaks.variabel_navn, 저장여부); MATRISE_VERDI(Shell_syntaks.variabel_data, 저장여부); MATRISE_VERDI(Shell_syntaks.이름길이, 저장여부); MATRISE_VERDI(Shell_syntaks.VERDI_lengde, 저장여부);
        Shell_syntaks.status_VERDI = VERDI(Shell_syntaks.status_VERDI, 저장여부);
        MATRISE_VERDI(linje_Redaktør.LOG_POST, 저장여부); MATRISE_VERDI(linje_Redaktør.LOG_lengde, 저장여부); MATRISE_VERDI(linje_Redaktør.Store_VERDI, 저장여부); MATRISE_VERDI(명령해석기.Linje, 저장여부);
        linje_Redaktør.LOG_ANTALL = VERDI(linje_Redaktør.LOG_ANTALL, 저장여부); linje_Redaktør.LOG_POST_avslutte_en_samtale = VERDI(linje_Redaktør.LOG_POST_avslutte_en_samtale, 저장여부);
        linje_Redaktør.SØK_VERDI = VERDI(linje_Redaktør.SØK_VERDI, 저장여부); linje_Redaktør.저장길이 = VERDI(linje_Redaktør.저장길이, 저장여부);
        linje_Redaktør.Størrelse = VERDI(linje_Redaktør.Størrelse, 저장여부); linje_Redaktør.markør_VERDI = VERDI(linje_Redaktør.markør_VERDI, 저장여부); linje_Redaktør.START_vindu = VERDI(linje_Redaktør.START_vindu, 저장여부);
        Forbered[보관칸] = 1;
    }
    static void Prosess_VERDI_oppføring() {
        int hendelse_nummer = Tavle.Terminal(12); if (hendelse_nummer == 0) return;
        søk_plassere(betalt_vare, true);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 4; Loop_INDEKS++) {
            if ((hendelse_nummer & (1 << (8 + Loop_INDEKS))) != 0) { Tavle.kontroll_bruker_app(32 + Loop_INDEKS); Forbered[Loop_INDEKS] = 0; }
            if ((hendelse_nummer & (1 << (4 + Loop_INDEKS))) != 0 && Loop_INDEKS != betalt_vare) Forbered[Loop_INDEKS] = 0;
        }
        int Neste_plassere = (hendelse_nummer & 15) - 1; if (Neste_plassere < 0) Neste_plassere = 0;
        if (Forbered[Neste_plassere] == 0) for (int Loop_INDEKS = 0; Loop_INDEKS < 30000; Loop_INDEKS++) 보관[Neste_plassere * 30000 + Loop_INDEKS] = 0;
        betalt_vare = Neste_plassere; søk_plassere(betalt_vare, false); Tavle.Terminal(100 + betalt_vare); 이어읽기 = true;
        단말.Skriv("\nTERMINAL FOCUS "); 단말.nummer(betalt_vare + 1); 단말.문자(10);
    }
    static boolean CV_kjøring() {
        if (Tavle.kontroll_bruker_app(16 + betalt_vare) == 0) return false;
        셸입출력.Tillat_interaktiv = true; 셸입출력.Kjør_2(false, false); Tavle.입출력전환(1);
        int 처리값 = Tavle.kontroll_bruker_app(betalt_vare); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; Shell_syntaks.status_VERDI = 처리값 < 0 ? 126 : 처리값; 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); Tavle.Terminal(3); }
        return true;
    }
}
