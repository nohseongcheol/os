// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 Shell Stato_VALORE. file 저장소는 공유하고 percorso/variabile_VALORE/LOG_riga/입력은 분리한다. */
public final class finestra_sessione {
    static int[] 보관 = new int[4 * 30000], Prepara = new int[4];
    static int Regolari_articolo, posizione;
    static boolean 이어읽기;
    static void array_VALORE(int[] dati, boolean Store_VALORE) {
        for (int Loop_INDICE = 0; Loop_INDICE < dati.length; Loop_INDICE++) { if (Store_VALORE) 보관[posizione++] = dati[Loop_INDICE]; else dati[Loop_INDICE] = 보관[posizione++]; }
    }
    static int VALORE(int dati_VALORE, boolean 저장여부) { if (저장여부) { 보관[posizione++] = dati_VALORE; return dati_VALORE; } return 보관[posizione++]; }
    static void cercare_funzione(int 보관칸, boolean 저장여부) {
        posizione = 보관칸 * 30000;
        array_VALORE(FileMemoria.Regolari_articolo, 저장여부); FileMemoria.Regolari_durata = VALORE(FileMemoria.Regolari_durata, 저장여부);
        array_VALORE(Shell_sintassi.variabile_nome, 저장여부); array_VALORE(Shell_sintassi.variabile_dati, 저장여부); array_VALORE(Shell_sintassi.이름길이, 저장여부); array_VALORE(Shell_sintassi.VALORE_durata, 저장여부);
        Shell_sintassi.Stato_VALORE = VALORE(Shell_sintassi.Stato_VALORE, 저장여부);
        array_VALORE(editor_di_righe.LOG_riga, 저장여부); array_VALORE(editor_di_righe.LOG_durata, 저장여부); array_VALORE(editor_di_righe.Store_VALORE, 저장여부); array_VALORE(InterpreteComandi.riga_di_ingresso, 저장여부);
        editor_di_righe.LOG_CONTA_NUMERI = VALORE(editor_di_righe.LOG_CONTA_NUMERI, 저장여부); editor_di_righe.LOG_riga_chiudere = VALORE(editor_di_righe.LOG_riga_chiudere, 저장여부);
        editor_di_righe.Cerca_VALORE = VALORE(editor_di_righe.Cerca_VALORE, 저장여부); editor_di_righe.저장길이 = VALORE(editor_di_righe.저장길이, 저장여부);
        editor_di_righe.Dimensione = VALORE(editor_di_righe.Dimensione, 저장여부); editor_di_righe.cursore_VALORE = VALORE(editor_di_righe.cursore_VALORE, 저장여부); editor_di_righe.START_finestra = VALORE(editor_di_righe.START_finestra, 저장여부);
        Prepara[보관칸] = 1;
    }
    static void Processi_VALORE_voce() {
        int evento_numero = scheda.terminale(12); if (evento_numero == 0) return;
        cercare_funzione(Regolari_articolo, true);
        for (int Loop_INDICE = 0; Loop_INDICE < 4; Loop_INDICE++) {
            if ((evento_numero & (1 << (8 + Loop_INDICE))) != 0) { scheda.controllo_USER_app(32 + Loop_INDICE); Prepara[Loop_INDICE] = 0; }
            if ((evento_numero & (1 << (4 + Loop_INDICE))) != 0 && Loop_INDICE != Regolari_articolo) Prepara[Loop_INDICE] = 0;
        }
        int Avanti_funzione = (evento_numero & 15) - 1; if (Avanti_funzione < 0) Avanti_funzione = 0;
        if (Prepara[Avanti_funzione] == 0) for (int Loop_INDICE = 0; Loop_INDICE < 30000; Loop_INDICE++) 보관[Avanti_funzione * 30000 + Loop_INDICE] = 0;
        Regolari_articolo = Avanti_funzione; cercare_funzione(Regolari_articolo, false); scheda.terminale(100 + Regolari_articolo); 이어읽기 = true;
        단말.Scrittura("\nTERMINAL FOCUS "); 단말.numero(Regolari_articolo + 1); 단말.문자(10);
    }
    static boolean CV_esecuzione() {
        if (scheda.controllo_USER_app(16 + Regolari_articolo) == 0) return false;
        셸입출력.Consenti_interattivo = true; 셸입출력.avvia(false, false); scheda.입출력전환(1);
        int 처리값 = scheda.controllo_USER_app(Regolari_articolo); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; Shell_sintassi.Stato_VALORE = 처리값 < 0 ? 126 : 처리값; 단말.Scrittura("exit "); 단말.numero(처리값); 단말.문자(10); scheda.terminale(3); }
        return true;
    }
}
