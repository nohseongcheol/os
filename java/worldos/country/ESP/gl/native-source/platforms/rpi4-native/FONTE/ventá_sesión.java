// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 shell Estado_VALOR. Ficheiro 저장소는 공유하고 CAMIÑO/변수/LOG_fila/입력은 분리한다. */
public final class ventá_sesión {
    static int[] 보관 = new int[4 * 30000], 준비 = new int[4];
    static int ao_corrente_elemento, Posición;
    static boolean 이어읽기;
    static void MATRIZ_VALOR(int[] datos, boolean Store_VALOR) {
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < datos.length; Loop_ÍNDICE++) { if (Store_VALOR) 보관[Posición++] = datos[Loop_ÍNDICE]; else datos[Loop_ÍNDICE] = 보관[Posición++]; }
    }
    static int VALOR(int datos_VALOR, boolean 저장여부) { if (저장여부) { 보관[Posición++] = datos_VALOR; return datos_VALOR; } return 보관[Posición++]; }
    static void buscar_cargo(int 보관칸, boolean 저장여부) {
        Posición = 보관칸 * 30000;
        MATRIZ_VALOR(Memoria_Ficheiros.ao_corrente_elemento, 저장여부); Memoria_Ficheiros.ao_corrente_duración = VALOR(Memoria_Ficheiros.ao_corrente_duración, 저장여부);
        MATRIZ_VALOR(shell_sintaxe.변수이름, 저장여부); MATRIZ_VALOR(shell_sintaxe.변수값, 저장여부); MATRIZ_VALOR(shell_sintaxe.이름길이, 저장여부); MATRIZ_VALOR(shell_sintaxe.VALOR_duración, 저장여부);
        shell_sintaxe.Estado_VALOR = VALOR(shell_sintaxe.Estado_VALOR, 저장여부);
        MATRIZ_VALOR(liña_Editor.LOG_fila, 저장여부); MATRIZ_VALOR(liña_Editor.LOG_duración, 저장여부); MATRIZ_VALOR(liña_Editor.Store_VALOR, 저장여부); MATRIZ_VALOR(명령해석기.Liña, 저장여부);
        liña_Editor.LOG_CONTAR = VALOR(liña_Editor.LOG_CONTAR, 저장여부); liña_Editor.LOG_fila_finalizar = VALOR(liña_Editor.LOG_fila_finalizar, 저장여부);
        liña_Editor.ACHAR_VALOR = VALOR(liña_Editor.ACHAR_VALOR, 저장여부); liña_Editor.저장길이 = VALOR(liña_Editor.저장길이, 저장여부);
        liña_Editor.Tamaño = VALOR(liña_Editor.Tamaño, 저장여부); liña_Editor.cursor_VALOR = VALOR(liña_Editor.cursor_VALOR, 저장여부); liña_Editor.START_ventá = VALOR(liña_Editor.START_ventá, 저장여부);
        준비[보관칸] = 1;
    }
    static void Proceso_VALOR_introdución() {
        int 사건번호 = Panel.Terminal(12); if (사건번호 == 0) return;
        buscar_cargo(ao_corrente_elemento, true);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 4; Loop_ÍNDICE++) {
            if ((사건번호 & (1 << (8 + Loop_ÍNDICE))) != 0) { Panel.control_usuario_apl(32 + Loop_ÍNDICE); 준비[Loop_ÍNDICE] = 0; }
            if ((사건번호 & (1 << (4 + Loop_ÍNDICE))) != 0 && Loop_ÍNDICE != ao_corrente_elemento) 준비[Loop_ÍNDICE] = 0;
        }
        int Seguinte_cargo = (사건번호 & 15) - 1; if (Seguinte_cargo < 0) Seguinte_cargo = 0;
        if (준비[Seguinte_cargo] == 0) for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 30000; Loop_ÍNDICE++) 보관[Seguinte_cargo * 30000 + Loop_ÍNDICE] = 0;
        ao_corrente_elemento = Seguinte_cargo; buscar_cargo(ao_corrente_elemento, false); Panel.Terminal(100 + ao_corrente_elemento); 이어읽기 = true;
        단말.Escritura("\nTERMINAL FOCUS "); 단말.수(ao_corrente_elemento + 1); 단말.문자(10);
    }
    static boolean 재개() {
        if (Panel.control_usuario_apl(16 + ao_corrente_elemento) == 0) return false;
        셸입출력.Permitir_interactivo = true; 셸입출력.Executar_2(false, false); Panel.입출력전환(1);
        int 처리값 = Panel.control_usuario_apl(ao_corrente_elemento); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; shell_sintaxe.Estado_VALOR = 처리값 < 0 ? 126 : 처리값; 단말.Escritura("exit "); 단말.수(처리값); 단말.문자(10); Panel.Terminal(3); }
        return true;
    }
}
