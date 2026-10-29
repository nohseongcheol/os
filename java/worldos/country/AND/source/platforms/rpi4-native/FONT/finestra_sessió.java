// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 shell Estat_VALOR. Fitxer 저장소는 공유하고 Camí/변수/LOG_fila/입력은 분리한다. */
public final class finestra_sessió {
    static int[] 보관 = new int[4 * 30000], Prepara = new int[4];
    static int 현재, Posició;
    static boolean 이어읽기;
    static void MATRIU_VALOR(int[] dades, boolean Store_VALOR) {
        for (int Loop_INDEX = 0; Loop_INDEX < dades.length; Loop_INDEX++) { if (Store_VALOR) 보관[Posició++] = dades[Loop_INDEX]; else dades[Loop_INDEX] = 보관[Posició++]; }
    }
    static int VALOR(int dades_VALOR, boolean 저장여부) { if (저장여부) { 보관[Posició++] = dades_VALOR; return dades_VALOR; } return 보관[Posició++]; }
    static void cercar_càrrec(int 보관칸, boolean 저장여부) {
        Posició = 보관칸 * 30000;
        MATRIU_VALOR(Memòria_Fitxers.현재, 저장여부); Memòria_Fitxers.현재길이 = VALOR(Memòria_Fitxers.현재길이, 저장여부);
        MATRIU_VALOR(shell_sintaxi.변수이름, 저장여부); MATRIU_VALOR(shell_sintaxi.변수값, 저장여부); MATRIU_VALOR(shell_sintaxi.이름길이, 저장여부); MATRIU_VALOR(shell_sintaxi.VALOR_durada, 저장여부);
        shell_sintaxi.Estat_VALOR = VALOR(shell_sintaxi.Estat_VALOR, 저장여부);
        MATRIU_VALOR(línia_Editor.LOG_fila, 저장여부); MATRIU_VALOR(línia_Editor.LOG_durada, 저장여부); MATRIU_VALOR(línia_Editor.Store_VALOR, 저장여부); MATRIU_VALOR(명령해석기.línia, 저장여부);
        línia_Editor.LOG_COMPT = VALOR(línia_Editor.LOG_COMPT, 저장여부); línia_Editor.LOG_fila_finalitzar = VALOR(línia_Editor.LOG_fila_finalitzar, 저장여부);
        línia_Editor.Cerca_VALOR = VALOR(línia_Editor.Cerca_VALOR, 저장여부); línia_Editor.저장길이 = VALOR(línia_Editor.저장길이, 저장여부);
        línia_Editor.Mida = VALOR(línia_Editor.Mida, 저장여부); línia_Editor.cursor_VALOR = VALOR(línia_Editor.cursor_VALOR, 저장여부); línia_Editor.Inici_finestra = VALOR(línia_Editor.Inici_finestra, 저장여부);
        Prepara[보관칸] = 1;
    }
    static void Procés_VALOR_introducció() {
        int 사건번호 = Tauler.Terminal(12); if (사건번호 == 0) return;
        cercar_càrrec(현재, true);
        for (int Loop_INDEX = 0; Loop_INDEX < 4; Loop_INDEX++) {
            if ((사건번호 & (1 << (8 + Loop_INDEX))) != 0) { Tauler.control_usuari_programa(32 + Loop_INDEX); Prepara[Loop_INDEX] = 0; }
            if ((사건번호 & (1 << (4 + Loop_INDEX))) != 0 && Loop_INDEX != 현재) Prepara[Loop_INDEX] = 0;
        }
        int Següent_càrrec = (사건번호 & 15) - 1; if (Següent_càrrec < 0) Següent_càrrec = 0;
        if (Prepara[Següent_càrrec] == 0) for (int Loop_INDEX = 0; Loop_INDEX < 30000; Loop_INDEX++) 보관[Següent_càrrec * 30000 + Loop_INDEX] = 0;
        현재 = Següent_càrrec; cercar_càrrec(현재, false); Tauler.Terminal(100 + 현재); 이어읽기 = true;
        단말.Escriptura("\nTERMINAL FOCUS "); 단말.수(현재 + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Tauler.control_usuari_programa(16 + 현재) == 0) return false;
        셸입출력.Permet_interactiu = true; 셸입출력.Executa_2(false, false); Tauler.입출력전환(1);
        int 처리값 = Tauler.control_usuari_programa(현재); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; shell_sintaxi.Estat_VALOR = 처리값 < 0 ? 126 : 처리값; 단말.Escriptura("exit "); 단말.수(처리값); 단말.문자(10); Tauler.Terminal(3); }
        return true;
    }
}
