// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 Shell status_värde. filnamn 저장소는 공유하고 sökväg_2/variabel_värde/LOG_POST/입력은 분리한다. */
public final class fönster_session {
    static int[] 보관 = new int[4 * 30000], Förbereda = new int[4];
    static int aktuellt_objekt, position;
    static boolean 이어읽기;
    static void MATRIS_värde(int[] data, boolean Store_värde) {
        for (int Loop_INDEX = 0; Loop_INDEX < data.length; Loop_INDEX++) { if (Store_värde) 보관[position++] = data[Loop_INDEX]; else data[Loop_INDEX] = 보관[position++]; }
    }
    static int värde(int data_värde, boolean 저장여부) { if (저장여부) { 보관[position++] = data_värde; return data_värde; } return 보관[position++]; }
    static void söka_placera(int 보관칸, boolean 저장여부) {
        position = 보관칸 * 30000;
        MATRIS_värde(Minne_Filer.aktuellt_objekt, 저장여부); Minne_Filer.aktuellt_längd = värde(Minne_Filer.aktuellt_längd, 저장여부);
        MATRIS_värde(Shell_syntax.variabel_namn, 저장여부); MATRIS_värde(Shell_syntax.variabel_data, 저장여부); MATRIS_värde(Shell_syntax.이름길이, 저장여부); MATRIS_värde(Shell_syntax.värde_längd, 저장여부);
        Shell_syntax.status_värde = värde(Shell_syntax.status_värde, 저장여부);
        MATRIS_värde(radredigerare.LOG_POST, 저장여부); MATRIS_värde(radredigerare.LOG_längd, 저장여부); MATRIS_värde(radredigerare.Store_värde, 저장여부); MATRIS_värde(명령해석기.inmatningsrad, 저장여부);
        radredigerare.LOG_ANTAL = värde(radredigerare.LOG_ANTAL, 저장여부); radredigerare.LOG_POST_avsluta = värde(radredigerare.LOG_POST_avsluta, 저장여부);
        radredigerare.SÖK_värde = värde(radredigerare.SÖK_värde, 저장여부); radredigerare.저장길이 = värde(radredigerare.저장길이, 저장여부);
        radredigerare.Storlek = värde(radredigerare.Storlek, 저장여부); radredigerare.markör_värde_04ee3e20 = värde(radredigerare.markör_värde_04ee3e20, 저장여부); radredigerare.START_fönster = värde(radredigerare.START_fönster, 저장여부);
        Förbereda[보관칸] = 1;
    }
    static void Process_värde_post() {
        int händelse_nummer = Tavla.kommandotolk(12); if (händelse_nummer == 0) return;
        söka_placera(aktuellt_objekt, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((händelse_nummer & (1 << (8 + Loop_INDEX))) != 0) { Tavla.kontroll_användare_app(32 + Loop_INDEX); Förbereda[Loop_INDEX] = 0; }
            if ((händelse_nummer & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != aktuellt_objekt) Förbereda[Loop_INDEX] = 0;
        }
        int Nästa_placera = (händelse_nummer & 15) - 1; if (Nästa_placera < 0) Nästa_placera = 0;
        if (Förbereda[Nästa_placera] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Nästa_placera * 30000 + Loop_INDEX] = 0;
        aktuellt_objekt = Nästa_placera; söka_placera(aktuellt_objekt, false); Tavla.kommandotolk(100 + aktuellt_objekt); 이어읽기 = true;
        단말.Skriv("\nTERMINAL FOCUS "); 단말.nummer(aktuellt_objekt + 1); 단말.문자(10);
    }
    static boolean CV_körning() {
        if (Tavla.kontroll_användare_app(16 + aktuellt_objekt) == 0) return false;
        셸입출력.Tillåt_interaktiv = true; 셸입출력.Kör(false, false); Tavla.입출력전환(1);
        int 처리값 = Tavla.kontroll_användare_app(aktuellt_objekt); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; Shell_syntax.status_värde = 처리값 < 0 ? 126 : 처리값; 단말.Skriv("exit "); 단말.nummer(처리값); 단말.문자(10); Tavla.kommandotolk(3); }
        return true;
    }
}
