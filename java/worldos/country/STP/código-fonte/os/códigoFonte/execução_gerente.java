// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Leitura 전용 Executar_comando 묶음의 ELF32 validar, argumentos Avançar_VALOR, 한 번에 한 espaço_do_utilizador Processo_VALOR Executar_comando. */
public final class execução_gerente {
    static final int START_usuário_app = 0x04000000;
    static final int usuário_encerrar = 0x04400000;
    static final int foto_endereço_final = 0x04200000;
    static final int argumento_START = 0x04300000;
    static int argumento_CONT_NÚM = 0;
    static int[] argumento_email = new int[16];

    static boolean recortar(int Endereço, int duração_VALOR) {
        return Endereço >= START_usuário_app && Endereço < usuário_encerrar && duração_VALOR >= 0 && duração_VALOR <= usuário_encerrar - Endereço;
    }

    static int número(int Endereço) { return Memória_região.analisar_inteiro(Endereço); }
    static int 짧은수(int Endereço) { return celular_VALOR.leitura_Memória(Endereço) | celular_VALOR.leitura_Memória(Endereço + 1) << 8; }
    static void gravar_número(int Endereço, int VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) celular_VALOR.gravar_Memória(Endereço + ÍNDICE, VALOR >>> (ÍNDICE * 8));
    }

    static int Grupo_CONT_NÚM() {
        int Endereço = celular_VALOR.executável_grupo();
        int Tamanho = celular_VALOR.executável_grupo_dimensionar();
        if (Tamanho < 8 || número(Endereço) != 0x50414b4a) return 0;
        int item_CONT_NÚM = número(Endereço + 4);
        return item_CONT_NÚM >= 0 && item_CONT_NÚM <= 32 && item_CONT_NÚM <= (Tamanho - 8) / 24 ? item_CONT_NÚM : 0;
    }

    static void entrada_Lista_f07b3200() {
        for (int ÍNDICE = 0; ÍNDICE < Grupo_CONT_NÚM(); ÍNDICE++) {
            int entrada_VALOR_962f286b = celular_VALOR.executável_grupo() + 8 + ÍNDICE * 24;
            for (int caractere_VALOR = 0; caractere_VALOR < 16 && celular_VALOR.leitura_Memória(entrada_VALOR_962f286b + caractere_VALOR) != 0; caractere_VALOR++)
                SMS_Terminal.문자(celular_VALOR.leitura_Memória(entrada_VALOR_962f286b + caractere_VALOR));
            SMS_Terminal.Escrita("\n");
        }
    }

    static int PROCURAR_entrada(int[] entrada_VALOR, int iniciar, int duração_VALOR) {
        if (duração_VALOR <= 0 || duração_VALOR >= 16) return 0;
        for (int ÍNDICE = 0; ÍNDICE < Grupo_CONT_NÚM(); ÍNDICE++) {
            int entrada_VALOR_962f286b = celular_VALOR.executável_grupo() + 8 + ÍNDICE * 24;
            boolean 같음 = celular_VALOR.leitura_Memória(entrada_VALOR_962f286b + duração_VALOR) == 0;
            for (int caractere_VALOR = 0; caractere_VALOR < duração_VALOR; caractere_VALOR++)
                if (entrada_VALOR[iniciar + caractere_VALOR] != celular_VALOR.leitura_Memória(entrada_VALOR_962f286b + caractere_VALOR)) 같음 = false;
            if (같음) return entrada_VALOR_962f286b;
        }
        return 0;
    }

    static int validar(int ficheiro, int duração_VALOR) {
        if (duração_VALOR < 52 || número(ficheiro) != 0x464c457f || celular_VALOR.leitura_Memória(ficheiro + 4) != 1
            || celular_VALOR.leitura_Memória(ficheiro + 5) != 1 || celular_VALOR.leitura_Memória(ficheiro + 6) != 1
            || 짧은수(ficheiro + 16) != 2 || 짧은수(ficheiro + 18) != 3 || número(ficheiro + 20) != 1
            || 짧은수(ficheiro + 40) != 52 || 짧은수(ficheiro + 42) != 32) return -8;
        int ponto_de_entrada_VALOR = número(ficheiro + 24);
        int tabela_cargo = número(ficheiro + 28);
        int item_CONT_NÚM = 짧은수(ficheiro + 44);
        if (item_CONT_NÚM == 0 || item_CONT_NÚM > 16 || tabela_cargo < 52 || tabela_cargo > duração_VALOR - item_CONT_NÚM * 32) return -8;
        boolean TI_executável = false;
        for (int ÍNDICE = 0; ÍNDICE < item_CONT_NÚM; ÍNDICE++) {
            int tabela_de_pesquisa = ficheiro + tabela_cargo + ÍNDICE * 32;
            int Tipo_VALOR = número(tabela_de_pesquisa);
            if (Tipo_VALOR == 2 || Tipo_VALOR == 3) return -8; // 동적 Ligar/analisador_48ee4b1b 미지원
            if (Tipo_VALOR != 1) continue;
            int posição = número(tabela_de_pesquisa + 4), Endereço = número(tabela_de_pesquisa + 8), tamanho_do_arquivo = número(tabela_de_pesquisa + 16), Memória_dimensionar = número(tabela_de_pesquisa + 20);
            int alinhar_VALOR = número(tabela_de_pesquisa + 28);
            if (Endereço < START_usuário_app || Endereço >= foto_endereço_final || Memória_dimensionar < 0 || Memória_dimensionar > foto_endereço_final - Endereço
                || tamanho_do_arquivo < 0 || tamanho_do_arquivo > Memória_dimensionar || posição < 0 || (tamanho_do_arquivo > 0 && posição > duração_VALOR - tamanho_do_arquivo)
                || (alinhar_VALOR != 0 && (alinhar_VALOR < 0 || (alinhar_VALOR & (alinhar_VALOR - 1)) != 0
                    || ((Endereço - posição) & (alinhar_VALOR - 1)) != 0))) return -8;
            for (int câmera_frontal_VALOR = 0; câmera_frontal_VALOR < ÍNDICE; câmera_frontal_VALOR++) {
                int Anterior_item = ficheiro + tabela_cargo + câmera_frontal_VALOR * 32;
                if (número(Anterior_item) == 1 && Memória_dimensionar > 0 && número(Anterior_item + 20) > 0
                    && Endereço < número(Anterior_item + 8) + número(Anterior_item + 20) && número(Anterior_item + 8) < Endereço + Memória_dimensionar) return -8;
            }
            if ((número(tabela_de_pesquisa + 24) & 1) != 0 && ponto_de_entrada_VALOR >= Endereço && ponto_de_entrada_VALOR - Endereço < tamanho_do_arquivo) TI_executável = true;
        }
        return TI_executável ? ponto_de_entrada_VALOR : -8;
    }

    static int Executar_comando(int[] entrada_VALOR, int iniciar, int duração_VALOR) {
        while (iniciar < duração_VALOR && entrada_VALOR[iniciar] == ' ') iniciar++;
        int 끝 = iniciar;
        while (끝 < duração_VALOR && entrada_VALOR[끝] != ' ') 끝++;
        int entrada_VALOR_962f286b = PROCURAR_entrada(entrada_VALOR, iniciar, 끝 - iniciar);
        if (entrada_VALOR_962f286b == 0) return -2;
        int posição = número(entrada_VALOR_962f286b + 16), Tamanho = número(entrada_VALOR_962f286b + 20);
        if (posição < 8 + Grupo_CONT_NÚM() * 24 || Tamanho < 52 || posição > celular_VALOR.executável_grupo_dimensionar() - Tamanho) return -8;
        int ficheiro = celular_VALOR.executável_grupo() + posição;
        int ponto_de_entrada_VALOR = validar(ficheiro, Tamanho);
        if (ponto_de_entrada_VALOR < 0) return ponto_de_entrada_VALOR;
        celular_VALOR.usuário_limpar_Sumário();
        int tabela_cargo = número(ficheiro + 28), item_CONT_NÚM = 짧은수(ficheiro + 44);
        for (int ÍNDICE = 0; ÍNDICE < item_CONT_NÚM; ÍNDICE++) {
            int tabela_de_pesquisa = ficheiro + tabela_cargo + ÍNDICE * 32;
            if (número(tabela_de_pesquisa) != 1) continue;
            int 원본 = ficheiro + número(tabela_de_pesquisa + 4), destino_VALOR = número(tabela_de_pesquisa + 8), tamanho_do_arquivo = número(tabela_de_pesquisa + 16);
            for (int byte_VALOR = 0; byte_VALOR < tamanho_do_arquivo; byte_VALOR++) celular_VALOR.gravar_Memória(destino_VALOR + byte_VALOR, celular_VALOR.leitura_Memória(원본 + byte_VALOR));
        }
        argumento_CONT_NÚM = 0;
        int Store_VALOR = argumento_START;
        while (끝 < duração_VALOR) {
            while (끝 < duração_VALOR && entrada_VALOR[끝] == ' ') 끝++;
            if (끝 == duração_VALOR) break;
            if (argumento_CONT_NÚM == argumento_email.length) return -22;
            iniciar = 끝;
            while (끝 < duração_VALOR && entrada_VALOR[끝] != ' ') 끝++;
            argumento_email[argumento_CONT_NÚM++] = Store_VALOR;
            gravar_número(Store_VALOR, 끝 - iniciar);
            for (int caractere_VALOR = iniciar; caractere_VALOR < 끝; caractere_VALOR++) gravar_número(Store_VALOR + 4 + (caractere_VALOR - iniciar) * 4, entrada_VALOR[caractere_VALOR]);
            Store_VALOR += 4 + (끝 - iniciar) * 4;
        }
        rede_pilha.TIRAR_Processo();
        Arquivo_descritor_gerente.START_Processo();
        int resultado = celular_VALOR.executar_usuário_app(ponto_de_entrada_VALOR, usuário_encerrar - 16);
        Arquivo_descritor_gerente.TIRAR_Processo();
        rede_pilha.TIRAR_Processo();
        return resultado;
    }
}
