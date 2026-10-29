// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 파이프는 16 KiB씩 순서대로 실행한다. 프로세스/동시 파이프를 흉내 내지 않는다. */
public final class 셸입출력 {
    static int[] entrada_dados = new int[16384], saída_dados = new int[16384];
    static int entrada_duração, entrada_cargo, saída_duração, arquivo_de_entrada = -1, arquivo_de_saída = -1;
    static boolean pipe_entrada, pipe_saída;
    static int falha_VALOR;
    static boolean Permitir_interativo = true;
    public static int TI_interativo() { return Permitir_interativo && arquivo_de_entrada < 3 && arquivo_de_saída < 3 && !pipe_entrada && !pipe_saída ? 1 : 0; }
    public static int saídaTexto(int Canal_VALOR, int VALOR) {
        if (Canal_VALOR != 1) return 0;
        if (arquivo_de_saída >= 3) { int 처리값 = FicheirosMemória.Escrita(arquivo_de_saída, VALOR); if (처리값 < 0) falha_VALOR = 처리값; return 1; }
        if (!pipe_saída) return 0;
        if (saída_duração == saída_dados.length) falha_VALOR = -28;
        else saída_dados[saída_duração++] = VALOR;
        return 1;
    }
    public static int entrada_VALOR() {
        if (arquivo_de_entrada >= 3) { int 처리값 = FicheirosMemória.Leitura(arquivo_de_entrada); return 처리값 == 256 ? -2 : 처리값; }
        if (pipe_entrada) return entrada_cargo < entrada_duração ? entrada_dados[entrada_cargo++] : -2;
        return -3; // UART로 Avançar_VALOR
    }
    static void iniciar(boolean entrelinhamento_pipe, boolean à_direita_pipe) {
        pipe_entrada = entrelinhamento_pipe; pipe_saída = à_direita_pipe;
        entrada_cargo = 0; saída_duração = 0; arquivo_de_entrada = -1; arquivo_de_saída = -1; falha_VALOR = 0;
    }
    static void 끝() {
        Quadro.입출력전환(0);
        if (arquivo_de_entrada >= 3) FicheirosMemória.Fechar(arquivo_de_entrada);
        if (arquivo_de_saída >= 3) FicheirosMemória.Fechar(arquivo_de_saída);
        if (pipe_saída) { entrada_duração = saída_duração; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < saída_duração; Loop_ÍNDICE++) entrada_dados[Loop_ÍNDICE] = saída_dados[Loop_ÍNDICE]; }
        arquivo_de_entrada = -1; arquivo_de_saída = -1; pipe_entrada = false; pipe_saída = false;
    }
}
