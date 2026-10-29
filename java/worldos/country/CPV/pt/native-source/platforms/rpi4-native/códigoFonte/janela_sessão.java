// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 네 터미널의 shell Estado_VALOR. ficheiro 저장소는 공유하고 caminho/variável_VALOR/LOG_linha/입력은 분리한다. */
public final class janela_sessão {
    static int[] 보관 = new int[4 * 30000], Preparar = new int[4];
    static int em_dia_item, posição;
    static boolean 이어읽기;
    static void MATRIZ_VALOR(int[] dados, boolean Store_VALOR) {
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < dados.length; Loop_ÍNDICE++) { if (Store_VALOR) 보관[posição++] = dados[Loop_ÍNDICE]; else dados[Loop_ÍNDICE] = 보관[posição++]; }
    }
    static int VALOR(int dados_VALOR, boolean 저장여부) { if (저장여부) { 보관[posição++] = dados_VALOR; return dados_VALOR; } return 보관[posição++]; }
    static void busca_cargo(int 보관칸, boolean 저장여부) {
        posição = 보관칸 * 30000;
        MATRIZ_VALOR(FicheirosMemória.em_dia_item, 저장여부); FicheirosMemória.em_dia_duração = VALOR(FicheirosMemória.em_dia_duração, 저장여부);
        MATRIZ_VALOR(shell_sintaxe.variável_nome, 저장여부); MATRIZ_VALOR(shell_sintaxe.variável_dados, 저장여부); MATRIZ_VALOR(shell_sintaxe.이름길이, 저장여부); MATRIZ_VALOR(shell_sintaxe.VALOR_duração, 저장여부);
        shell_sintaxe.Estado_VALOR = VALOR(shell_sintaxe.Estado_VALOR, 저장여부);
        MATRIZ_VALOR(editor_de_linha.LOG_linha, 저장여부); MATRIZ_VALOR(editor_de_linha.LOG_duração, 저장여부); MATRIZ_VALOR(editor_de_linha.Store_VALOR, 저장여부); MATRIZ_VALOR(InterpretadorComandos.linha_de_entrada, 저장여부);
        editor_de_linha.LOG_CONT_NÚM = VALOR(editor_de_linha.LOG_CONT_NÚM, 저장여부); editor_de_linha.LOG_linha_encerrar = VALOR(editor_de_linha.LOG_linha_encerrar, 저장여부);
        editor_de_linha.busca_VALOR = VALOR(editor_de_linha.busca_VALOR, 저장여부); editor_de_linha.저장길이 = VALOR(editor_de_linha.저장길이, 저장여부);
        editor_de_linha.Tamanho = VALOR(editor_de_linha.Tamanho, 저장여부); editor_de_linha.cursor_VALOR = VALOR(editor_de_linha.cursor_VALOR, 저장여부); editor_de_linha.START_janela = VALOR(editor_de_linha.START_janela, 저장여부);
        Preparar[보관칸] = 1;
    }
    static void Processo_VALOR_entrada() {
        int Evento_número = Quadro.terminal(12); if (Evento_número == 0) return;
        busca_cargo(em_dia_item, true);
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 4; Loop_ÍNDICE++) {
            if ((Evento_número & (1 << (8 + Loop_ÍNDICE))) != 0) { Quadro.visual_usuário_app(32 + Loop_ÍNDICE); Preparar[Loop_ÍNDICE] = 0; }
            if ((Evento_número & (1 << (4 + Loop_ÍNDICE))) != 0 && Loop_ÍNDICE != em_dia_item) Preparar[Loop_ÍNDICE] = 0;
        }
        int Avançar_cargo = (Evento_número & 15) - 1; if (Avançar_cargo < 0) Avançar_cargo = 0;
        if (Preparar[Avançar_cargo] == 0) for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 30000; Loop_ÍNDICE++) 보관[Avançar_cargo * 30000 + Loop_ÍNDICE] = 0;
        em_dia_item = Avançar_cargo; busca_cargo(em_dia_item, false); Quadro.terminal(100 + em_dia_item); 이어읽기 = true;
        단말.Escrita("\nTERMINAL FOCUS "); 단말.número(em_dia_item + 1); 단말.문자(10);
    }
    static boolean CV_execução() {
        if (Quadro.visual_usuário_app(16 + em_dia_item) == 0) return false;
        셸입출력.Permitir_interativo = true; 셸입출력.iniciar(false, false); Quadro.입출력전환(1);
        int 처리값 = Quadro.visual_usuário_app(em_dia_item); 셸입출력.끝();
        if (처리값 != -1005) { 이어읽기 = false; shell_sintaxe.Estado_VALOR = 처리값 < 0 ? 126 : 처리값; 단말.Escrita("exit "); 단말.número(처리값); 단말.문자(10); Quadro.terminal(3); }
        return true;
    }
}
