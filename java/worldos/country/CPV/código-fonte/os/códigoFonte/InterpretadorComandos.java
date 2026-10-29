// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 디스크 Escrita 없이 동작하는 작은 직렬/PS2 InterpretadorComandos. */
public final class InterpretadorComandos {
    static int[] entrada_VALOR = new int[128];
    static int duração_VALOR = 0;
    static boolean 앞줄복귀 = false;
    static boolean linha_estouro = false;

    static boolean comando(String Nome) {
        if (duração_VALOR < Nome.length()) return false;
        for (int ÍNDICE = 0; ÍNDICE < Nome.length(); ÍNDICE++)
            if (entrada_VALOR[ÍNDICE] != Nome.charAt(ÍNDICE)) return false;
        return duração_VALOR == Nome.length() || entrada_VALOR[Nome.length()] == ' ';
    }

    static void mostrar_ajuda() {
        SMS_Terminal.Escrita("help | info | mem | alloc | free N | echo TEXT | clear | test | halt\n");
        SMS_Terminal.Escrita("apps | run NAME [ARGS] | net\n");
        SMS_Terminal.Escrita("ls | cat FILE | edit FILE | rm FILE | javac FILE.java | java CLASS [ARGS]\n");
        SMS_Terminal.Escrita("sync (연결된 JKSTORE1 Store_VALOR 장치에 ficheiro 보존)\n");
    }

    static void Processo_VALOR_entrada() {
        if (duração_VALOR == 0) return;
        if (comando("help")) mostrar_ajuda();
        else if (comando("sync")) {
            int resultado = 파일보존.sincronizar();
            SMS_Terminal.Escrita("Sync: "); SMS_Terminal.gravar_número(resultado); SMS_Terminal.문자(10);
        }
        else if (comando("ls")) Memória_sistema_de_arquivos.entrada_Lista_f07b3200();
        else if (comando("edit")) Memória_sistema_de_arquivos.comando(entrada_VALOR, 4, duração_VALOR, 0);
        else if (comando("cat")) Memória_sistema_de_arquivos.comando(entrada_VALOR, 3, duração_VALOR, 1);
        else if (comando("rm")) Memória_sistema_de_arquivos.comando(entrada_VALOR, 2, duração_VALOR, 2);
        else if (comando("java") || comando("javac")) {
            int resultado = execução_gerente.Executar_comando(entrada_VALOR, 0, duração_VALOR);
            SMS_Terminal.Escrita("Exit: "); SMS_Terminal.gravar_número(resultado); SMS_Terminal.문자(10);
        }
        else if (comando("apps")) execução_gerente.entrada_Lista_f07b3200();
        else if (comando("net")) rede_pilha.Estado_VALOR();
        else if (comando("run")) {
            int resultado = execução_gerente.Executar_comando(entrada_VALOR, 3, duração_VALOR);
            SMS_Terminal.Escrita("Exit: "); SMS_Terminal.gravar_número(resultado); SMS_Terminal.Escrita("\n");
        } else if (comando("info")) {
            SMS_Terminal.Escrita("JKOROS: Java AOT / x86 32-bit / embedded subset JVM / polling kernel\n");
        } else if (comando("mem")) {
            SMS_Terminal.Escrita("위쪽 Memória_VALOR email_região(KiB): "); SMS_Terminal.gravar_número(Memória_região.MAIÚSCULA_Memória_dimensionar());
            SMS_Terminal.Escrita("\n배열 동적 Memória_VALOR email_região(byte_VALOR): "); SMS_Terminal.gravar_número(celular_VALOR.MATRIZ_uso());
            SMS_Terminal.Escrita(" / 262144\n작업 email_região seção_VALOR: "); SMS_Terminal.gravar_número(Memória_região.사용개수());
            SMS_Terminal.Escrita(" / 8 (각 4096바이트)\n");
        } else if (comando("alloc")) {
            int ÍNDICE = Memória_região.alocar_Armazenamento();
            SMS_Terminal.Escrita("seção_VALOR ÍNDICE: "); SMS_Terminal.gravar_número(ÍNDICE); SMS_Terminal.Escrita("\n");
        } else if (comando("free")) {
            if (duração_VALOR == 6 && entrada_VALOR[4] == ' ' && entrada_VALOR[5] >= '0' && entrada_VALOR[5] <= '7') {
                SMS_Terminal.Escrita(Memória_região.devolver_RC(entrada_VALOR[5] - '0') ? "반환됨\n" : "할당되지 않은 seção_VALOR\n");
            } else SMS_Terminal.Escrita("사용법: free 0..7\n");
        } else if (comando("echo")) {
            for (int ÍNDICE = 5; ÍNDICE < duração_VALOR; ÍNDICE++) SMS_Terminal.문자(entrada_VALOR[ÍNDICE]);
            SMS_Terminal.문자(10);
        } else if (comando("clear")) SMS_Terminal.apagar_entrada();
        else if (comando("test")) Núcleo.testes();
        else if (comando("halt")) {
            SMS_Terminal.Escrita("HALTED\n");
            celular_VALOR.정지();
        } else SMS_Terminal.Escrita("알 número 없는 명령입니다. help를 입력하세요.\n");
    }

    static void aceitar_E_gravar(int VALOR) {
        if (VALOR == 10 && 앞줄복귀) { 앞줄복귀 = false; return; }
        앞줄복귀 = VALOR == 13;
        if (VALOR == 10 || VALOR == 13) {
            SMS_Terminal.문자(10);
            if (Memória_sistema_de_arquivos.편집중) Memória_sistema_de_arquivos.Editado_linha(entrada_VALOR, duração_VALOR, linha_estouro);
            else Processo_VALOR_entrada();
            duração_VALOR = 0;
            linha_estouro = false;
            SMS_Terminal.Escrita(Memória_sistema_de_arquivos.편집중 ? "...> " : "jkoros> ");
        } else if (VALOR == 8 || VALOR == 127) {
            if (duração_VALOR > 0) {
                duração_VALOR--;
                SMS_Terminal.직렬바이트(8); SMS_Terminal.직렬바이트(32); SMS_Terminal.직렬바이트(8);
                SMS_Terminal.tela_caractere(8);
            }
        } else if (VALOR >= 32 && VALOR < 127 && duração_VALOR < entrada_VALOR.length) {
            entrada_VALOR[duração_VALOR++] = VALOR;
            SMS_Terminal.문자(VALOR);
        } else if (VALOR >= 32 && VALOR < 127) linha_estouro = true;
    }

    static void iniciar() {
        mostrar_ajuda();
        SMS_Terminal.Escrita("READY\njkoros> ");
        while (true) {
            int VALOR = SMS_Terminal.직렬읽기();
            if (VALOR < 0) VALOR = teclado.Leitura();
            if (VALOR >= 0) aceitar_E_gravar(VALOR);
            else { rede_pilha.verificar(); celular_VALOR.잠시양보(); }
        }
    }
}
