// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 같은 RAM VFS와 표준 입출력을 쓰는 shell 내장 ferramentas. */
public final class shell_Ferramentas {
    static int[] dados = new int[16384];
    static int arquivo_de_entrada = -1;
    static int abrir_Arquivo(int argumento_ÍNDICE, int Processo_MODO) {
        int 처리값 = InterpretadorComandos.caminho(argumento_ÍNDICE); return 처리값 < 0 ? 처리값 : FicheirosMemória.Abrir(Processo_MODO);
    }
    static boolean Preparar_entrada(int argumento_ÍNDICE) {
        arquivo_de_entrada = -1;
        if (argumento_ÍNDICE < InterpretadorComandos.token_CONT_NÚM) {
            arquivo_de_entrada = abrir_Arquivo(argumento_ÍNDICE, 0);
            if (arquivo_de_entrada < 0) { InterpretadorComandos.erro(arquivo_de_entrada); return false; }
        }
        return true;
    }
    static int Leitura() {
        if (arquivo_de_entrada >= 3) return FicheirosMemória.Leitura(arquivo_de_entrada);
        while (true) {
            int byte_dados = Quadro.직렬읽기(); if (byte_dados == -2 || byte_dados == 4) return 256;
            if (byte_dados == 3) { InterpretadorComandos.resultado = 130; return 256; }
            if (byte_dados >= 0) return byte_dados; Quadro.LUCRO_CPU();
        }
    }
    static void Fechar() { if (arquivo_de_entrada >= 3) FicheirosMemória.Fechar(arquivo_de_entrada); arquivo_de_entrada = -1; }
    static void Exibir_VALOR() {
        int 마지막자리 = InterpretadorComandos.token_CONT_NÚM == 1 ? 2 : InterpretadorComandos.token_CONT_NÚM;
        for (int argumento_ÍNDICE = 1; argumento_ÍNDICE < 마지막자리; argumento_ÍNDICE++) {
            if (!Preparar_entrada(argumento_ÍNDICE)) continue;
            int byte_dados; while ((byte_dados = Leitura()) != 256 && byte_dados >= 0) Quadro.직렬쓰기(byte_dados);
            if (byte_dados < 0) InterpretadorComandos.erro(byte_dados); Fechar();
        }
    }
    static void Arquivo_cargo(String Ação_número) {
        if (InterpretadorComandos.token_CONT_NÚM != 2) { InterpretadorComandos.resultado = 2; 단말.Escrita("사용법: mkdir/rmdir/touch ficheiro\n"); return; }
        int 처리값 = InterpretadorComandos.caminho(1);
        if (처리값 >= 0) {
            if (Ação_número.charAt(0) == 'm') 처리값 = FicheirosMemória.Criar_Diretório();
            else if (Ação_número.charAt(0) == 'r') 처리값 = FicheirosMemória.remover_Diretório();
            else { 처리값 = FicheirosMemória.Abrir(65); if (처리값 >= 3) 처리값 = FicheirosMemória.Fechar(처리값); }
        }
        if (처리값 < 0) InterpretadorComandos.erro(처리값);
    }
    static void copiar_VALOR(boolean 이동여부) {
        if (InterpretadorComandos.token_CONT_NÚM != 3) { InterpretadorComandos.resultado = 2; 단말.Escrita("사용법: cp/mv 원본 destino_empresa (ficheiro)\n"); return; }
        int 처리값 = InterpretadorComandos.caminho(1); if (처리값 >= 0) 처리값 = FicheirosMemória.normalizar_VALOR();
        if (처리값 < 0) { InterpretadorComandos.erro(처리값); return; }
        int 원본번호 = FicheirosMemória.PROCURAR_entrada(); if (원본번호 < 0) { InterpretadorComandos.erro(-2); return; }
        int entrada_CONT_NÚM_8f7753a1 = FicheirosMemória.duração_VALOR[원본번호]; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) dados[Loop_ÍNDICE] = FicheirosMemória.leitura_dados(원본번호, Loop_ÍNDICE);
        처리값 = InterpretadorComandos.caminho(2); if (처리값 >= 0) 처리값 = FicheirosMemória.normalizar_VALOR();
        if (처리값 < 0) { InterpretadorComandos.erro(처리값); return; }
        if (FicheirosMemória.PROCURAR_entrada() == 원본번호) { if (!이동여부) InterpretadorComandos.erro(-22); return; }
        if (이동여부) { 처리값 = FicheirosMemória.Renomear_entrada(원본번호); if (처리값 < 0) InterpretadorComandos.erro(처리값); return; }
        int 열린파일번호 = FicheirosMemória.Abrir(577); if (열린파일번호 < 0) { InterpretadorComandos.erro(열린파일번호); return; }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) { 처리값 = FicheirosMemória.Escrita(열린파일번호, dados[Loop_ÍNDICE]); if (처리값 < 0) { InterpretadorComandos.erro(처리값); break; } }
        FicheirosMemória.Fechar(열린파일번호);
    }
    static int dígito_VALOR(int argumento_ÍNDICE) {
        if (argumento_ÍNDICE >= InterpretadorComandos.token_CONT_NÚM) return -1;
        int entrada_CONT_NÚM_8f7753a1 = 0; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < InterpretadorComandos.duração_VALOR[argumento_ÍNDICE]; Loop_ÍNDICE++) { int ponto_de_código = InterpretadorComandos.token_VALOR[InterpretadorComandos.시작점[argumento_ÍNDICE] + Loop_ÍNDICE]; if (ponto_de_código < '0' || ponto_de_código > '9' || entrada_CONT_NÚM_8f7753a1 > 10000) return -1; entrada_CONT_NÚM_8f7753a1 = entrada_CONT_NÚM_8f7753a1 * 10 + ponto_de_código - '0'; } return entrada_CONT_NÚM_8f7753a1;
    }
    static void 세기() {
        int argumento_ÍNDICE = 1, 선택번호 = 0;
        if (InterpretadorComandos.같음(1, "-c") || InterpretadorComandos.같음(1, "-l") || InterpretadorComandos.같음(1, "-w")) { 선택번호 = InterpretadorComandos.같음(1, "-c") ? 1 : InterpretadorComandos.같음(1, "-l") ? 2 : 3; argumento_ÍNDICE++; }
        if (InterpretadorComandos.token_CONT_NÚM > argumento_ÍNDICE + 1) { InterpretadorComandos.resultado = 2; 단말.Escrita("사용법: wc [-c|-l|-w] [ficheiro]\n"); return; }
        if (!Preparar_entrada(argumento_ÍNDICE)) return;
        int byte_CONT_NÚM = 0, 줄수 = 0, 낱말수 = 0, byte_dados; boolean 낱말 = false;
        while ((byte_dados = Leitura()) >= 0 && byte_dados != 256) { byte_CONT_NÚM++; if (byte_dados == 10) 줄수++; boolean ESPAÇO = byte_dados == 32 || byte_dados >= 9 && byte_dados <= 13; if (!ESPAÇO && !낱말) 낱말수++; 낱말 = !ESPAÇO; }
        Fechar(); if (byte_dados < 0) { InterpretadorComandos.erro(byte_dados); return; }
        if (선택번호 != 0) 단말.número(선택번호 == 1 ? byte_CONT_NÚM : 선택번호 == 2 ? 줄수 : 낱말수);
        else { 단말.número(줄수); 단말.문자(' '); 단말.número(낱말수); 단말.문자(' '); 단말.número(byte_CONT_NÚM); } 단말.문자(10);
    }
    static void PROCURAR_entrada() {
        if (InterpretadorComandos.token_CONT_NÚM < 2 || InterpretadorComandos.token_CONT_NÚM > 3) { InterpretadorComandos.resultado = 2; 단말.Escrita("사용법: grep 찾을문구 [ficheiro]\n"); return; }
        if (!Preparar_entrada(2)) return;
        int entrada_CONT_NÚM_8f7753a1 = 0, byte_dados, 일치수 = 0;
        while (true) {
            byte_dados = Leitura();
            if (byte_dados == 10 || byte_dados == 256 || byte_dados < 0) {
                boolean 찾은여부 = false;
                for (int Loop_ÍNDICE = 0; Loop_ÍNDICE <= entrada_CONT_NÚM_8f7753a1 - InterpretadorComandos.duração_VALOR[1]; Loop_ÍNDICE++) {
                    boolean 같은여부 = true; for (int interna_cargo = 0; interna_cargo < InterpretadorComandos.duração_VALOR[1]; interna_cargo++) if (dados[Loop_ÍNDICE + interna_cargo] != InterpretadorComandos.token_VALOR[InterpretadorComandos.시작점[1] + interna_cargo]) 같은여부 = false;
                    if (같은여부) 찾은여부 = true;
                }
                if (찾은여부 && (entrada_CONT_NÚM_8f7753a1 > 0 || byte_dados == 10)) { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) Quadro.직렬쓰기(dados[Loop_ÍNDICE]); 단말.문자(10); 일치수++; }
                entrada_CONT_NÚM_8f7753a1 = 0; if (byte_dados != 10) break;
            } else if (entrada_CONT_NÚM_8f7753a1 < dados.length) dados[entrada_CONT_NÚM_8f7753a1++] = byte_dados;
            else { InterpretadorComandos.erro(-28); Fechar(); return; }
        }
        Fechar(); if (byte_dados < 0) InterpretadorComandos.erro(byte_dados); else if (InterpretadorComandos.resultado == 0) InterpretadorComandos.resultado = 일치수 == 0 ? 1 : 0;
    }
    static void HEAD_VALOR(boolean 뒤쪽자리) {
        int argumento_ÍNDICE = 1, 줄수 = 10;
        if (InterpretadorComandos.같음(1, "-n")) { 줄수 = dígito_VALOR(2); argumento_ÍNDICE = 3; }
        if (줄수 < 0 || InterpretadorComandos.token_CONT_NÚM > argumento_ÍNDICE + 1) { InterpretadorComandos.resultado = 2; 단말.Escrita("사용법: head/tail [-n 줄수] [ficheiro]\n"); return; }
        if (!Preparar_entrada(argumento_ÍNDICE)) return;
        int entrada_CONT_NÚM_8f7753a1 = 0, byte_dados;
        while ((byte_dados = Leitura()) != 256 && byte_dados >= 0) { if (entrada_CONT_NÚM_8f7753a1 == dados.length) { InterpretadorComandos.erro(-28); Fechar(); return; } dados[entrada_CONT_NÚM_8f7753a1++] = byte_dados; }
        Fechar(); if (byte_dados < 0) { InterpretadorComandos.erro(byte_dados); return; }
        int local_START = 0, encerrar_cargo = entrada_CONT_NÚM_8f7753a1;
        if (줄수 == 0) return;
        if (뒤쪽자리) { int total_CONT_NÚM = 0; for (int Loop_ÍNDICE = entrada_CONT_NÚM_8f7753a1 - 2; Loop_ÍNDICE >= 0; Loop_ÍNDICE--) if (dados[Loop_ÍNDICE] == 10 && ++total_CONT_NÚM == 줄수) { local_START = Loop_ÍNDICE + 1; break; } }
        else { int total_CONT_NÚM = 0; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) if (dados[Loop_ÍNDICE] == 10 && ++total_CONT_NÚM == 줄수) { encerrar_cargo = Loop_ÍNDICE + 1; break; } }
        for (int Loop_ÍNDICE = local_START; Loop_ÍNDICE < encerrar_cargo; Loop_ÍNDICE++) Quadro.직렬쓰기(dados[Loop_ÍNDICE]);
    }
    static void gravar_Juntos() {
        boolean Acrescentar = InterpretadorComandos.같음(1, "-a"); int argumento_ÍNDICE = Acrescentar ? 2 : 1;
        if (InterpretadorComandos.token_CONT_NÚM != argumento_ÍNDICE + 1) { InterpretadorComandos.resultado = 2; 단말.Escrita("사용법: tee [-a] ficheiro\n"); return; }
        int 열린파일번호 = abrir_Arquivo(argumento_ÍNDICE, Acrescentar ? 1089 : 577); if (열린파일번호 < 0) { InterpretadorComandos.erro(열린파일번호); return; }
        arquivo_de_entrada = -1; int byte_dados;
        while ((byte_dados = Leitura()) != 256 && byte_dados >= 0) { int 처리값 = FicheirosMemória.Escrita(열린파일번호, byte_dados); if (처리값 < 0) { InterpretadorComandos.erro(처리값); break; } Quadro.직렬쓰기(byte_dados); }
        FicheirosMemória.Fechar(열린파일번호);
    }
}
