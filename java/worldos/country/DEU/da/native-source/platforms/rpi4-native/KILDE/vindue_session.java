// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 Shell status_VÆRDI. Fil 저장소는 공유하고 Sti/variabel_VÆRDI/LOG_post/입력은 분리한다. */
public final class vindue_session {
    static int[] 보관 = new int[4 * 30000], Tilrettelæg = new int[4];
    static int aktuel_vare, Placering;
    static boolean 이어읽기;
    static void MATRIX_VÆRDI(int[] data, boolean Store_VÆRDI) {
        for (int Loop_INDEKS = 0; Loop_INDEKS < data.length; Loop_INDEKS++) { if (Store_VÆRDI) 보관[Placering++] = data[Loop_INDEKS]; else data[Loop_INDEKS] = 보관[Placering++]; }
    }
    static int VÆRDI(int data_VÆRDI, boolean 저장여부) { if (저장여부) { 보관[Placering++] = data_VÆRDI; return data_VÆRDI; } return 보관[Placering++]; }
    static void søge_placere(int 보관칸, boolean 저장여부) {
        Placering = 보관칸 * 30000;
        MATRIX_VÆRDI(Hukommelse_Filer.aktuel_vare, 저장여부); Hukommelse_Filer.aktuel_varighed = VÆRDI(Hukommelse_Filer.aktuel_varighed, 저장여부);
        MATRIX_VÆRDI(Shell_syntaks.variabel_navn, 저장여부); MATRIX_VÆRDI(Shell_syntaks.variabel_data, 저장여부); MATRIX_VÆRDI(Shell_syntaks.이름길이, 저장여부); MATRIX_VÆRDI(Shell_syntaks.VÆRDI_varighed, 저장여부);
        Shell_syntaks.status_VÆRDI = VÆRDI(Shell_syntaks.status_VÆRDI, 저장여부);
        MATRIX_VÆRDI(linjeeditor.LOG_post, 저장여부); MATRIX_VÆRDI(linjeeditor.LOG_varighed, 저장여부); MATRIX_VÆRDI(linjeeditor.Store_VÆRDI, 저장여부); MATRIX_VÆRDI(명령해석기.Linje, 저장여부);
        linjeeditor.LOG_TÆL = VÆRDI(linjeeditor.LOG_TÆL, 저장여부); linjeeditor.LOG_post_afslutte_et_opkald = VÆRDI(linjeeditor.LOG_post_afslutte_et_opkald, 저장여부);
        linjeeditor.SØG_VÆRDI = VÆRDI(linjeeditor.SØG_VÆRDI, 저장여부); linjeeditor.저장길이 = VÆRDI(linjeeditor.저장길이, 저장여부);
        linjeeditor.Størrelse = VÆRDI(linjeeditor.Størrelse, 저장여부); linjeeditor.markør_VÆRDI = VÆRDI(linjeeditor.markør_VÆRDI, 저장여부); linjeeditor.START_vindue = VÆRDI(linjeeditor.START_vindue, 저장여부);
        Tilrettelæg[보관칸] = 1;
    }
    static void Proces_VÆRDI_post() {
        int hændelse_tal = Tavle.Terminal(12); if (hændelse_tal == 0) return;
        søge_placere(aktuel_vare, true);
        for (int Loop_INDEKS = 0; Loop_INDEKS < 4; Loop_INDEKS++) {
            if ((hændelse_tal & (1 << (8 + Loop_INDEKS))) != 0) { Tavle.kontrol_bruger_app(32 + Loop_INDEKS); Tilrettelæg[Loop_INDEKS] = 0; }
            if ((hændelse_tal & (1 << (4 + Loop_INDEKS))) != 0 && Loop_INDEKS != aktuel_vare) Tilrettelæg[Loop_INDEKS] = 0;
        }
        int Næste_placere = (hændelse_tal & 15) - 1; if (Næste_placere < 0) Næste_placere = 0;
        if (Tilrettelæg[Næste_placere] == 0) for (int Loop_INDEKS = 0; Loop_INDEKS < 30000; Loop_INDEKS++) 보관[Næste_placere * 30000 + Loop_INDEKS] = 0;
        aktuel_vare = Næste_placere; søge_placere(aktuel_vare, false); Tavle.Terminal(100 + aktuel_vare); 이어읽기 = true;
        단말.Skrive("\nTERMINAL FOCUS "); 단말.tal(aktuel_vare + 1); 단말.문자(10);
    }
    static boolean CV_udførelse() {
        if (Tavle.kontrol_bruger_app(16 + aktuel_vare) == 0) return false;
        셸입출력.Tillad_interaktiv = true; 셸입출력.Kør_2(false, false); Tavle.입출력전환(1);
        int 처리값 = Tavle.kontrol_bruger_app(aktuel_vare); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; Shell_syntaks.status_VÆRDI = 처리값 < 0 ? 126 : 처리값; 단말.Skrive("exit "); 단말.tal(처리값); 단말.문자(10); Tavle.Terminal(3); }
        return true;
    }
}
