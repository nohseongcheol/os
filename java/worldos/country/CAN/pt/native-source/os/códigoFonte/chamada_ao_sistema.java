// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 espaço_do_utilizador ponteiro/길이는 acesso_entrada 전에 검사한다. */
public final class chamada_ao_sistema {
    static int[] 임시자료 = new int[1024];

    static int MATRIZ_duração(int Endereço) {
        if (!execução_gerente.recortar(Endereço, 4)) return -14;
        int duração_VALOR = execução_gerente.número(Endereço);
        if (duração_VALOR < 0 || duração_VALOR > (execução_gerente.usuário_encerrar - Endereço - 4) / 4) return -14;
        return duração_VALOR;
    }

    public static int Processo_VALOR_entrada(int ÍNDICE, int 가, int SEGUNDO_operando, int 다, int 라, int 마) {
        if (ÍNDICE == 30) return Arquivo_descritor_gerente.abrir_Arquivo(가, SEGUNDO_operando, 다);
        if (ÍNDICE == 31) return Arquivo_descritor_gerente.leitura_Arquivo(가, SEGUNDO_operando, 다);
        if (ÍNDICE == 32) return Arquivo_descritor_gerente.gravar_Arquivo(가, SEGUNDO_operando, 다);
        if (ÍNDICE == 33) return Arquivo_descritor_gerente.Close_Arquivo(가);
        if (ÍNDICE == 34) return Arquivo_descritor_gerente.busca_Arquivo(가, SEGUNDO_operando, 다);
        if (ÍNDICE == 35) return Arquivo_descritor_gerente.Duplicar_descritor(가, 0, false, 0);
        if (ÍNDICE == 36) return Arquivo_descritor_gerente.Duplicar_descritor(가, SEGUNDO_operando, true, 0);
        if (ÍNDICE == 37) return Arquivo_descritor_gerente.leitura_Arquivo_Status(가, SEGUNDO_operando);
        if (ÍNDICE == 38) return Arquivo_descritor_gerente.remover_Arquivo_entrada_nome(가);
        if (ÍNDICE == 39) return Arquivo_descritor_gerente.set_Arquivo_duração(가, SEGUNDO_operando);
        if (ÍNDICE == 40) return Arquivo_descritor_gerente.visual_descritor(가, SEGUNDO_operando, 다);
        if (ÍNDICE == 41) return Arquivo_descritor_gerente.Criar_empresa(가, SEGUNDO_operando, 다);
        if (ÍNDICE == 42) return Arquivo_descritor_gerente.BIND_email(가, SEGUNDO_operando, 다);
        if (ÍNDICE == 43) return Arquivo_descritor_gerente.enviar_datagrama_dados(가, SEGUNDO_operando, 다, 라, 마);
        if (ÍNDICE == 44) return Arquivo_descritor_gerente.receber_datagrama_dados(가, SEGUNDO_operando, 다, 라, 마);
        if (ÍNDICE == 45) return Arquivo_descritor_gerente.leitura_soquete_email(가, SEGUNDO_operando, 다);
        if (ÍNDICE == 46) return Arquivo_descritor_gerente.set_receber_TEMPOLIMITE(가, SEGUNDO_operando);
        if (ÍNDICE == 47) {
            int descritor_VALOR = Arquivo_descritor_gerente.PROCURAR_descritor(가);
            if (descritor_VALOR < 0) return -9;
            if (Arquivo_descritor_gerente.Tipo_VALOR[descritor_VALOR] != 2) return -22;
            return 파일보존.sincronizar();
        }
        if (ÍNDICE == 1) {
            int duração_VALOR = MATRIZ_duração(가);
            if (duração_VALOR < 0) return duração_VALOR;
            if (duração_VALOR > 4096) return -90;
            for (int caractere_VALOR = 0; caractere_VALOR < duração_VALOR; caractere_VALOR++) SMS_Terminal.문자(execução_gerente.número(가 + 4 + caractere_VALOR * 4) & 65535);
            return duração_VALOR;
        }
        if (ÍNDICE == 2) return execução_gerente.argumento_CONT_NÚM;
        if (ÍNDICE == 3) return 가 >= 0 && 가 < execução_gerente.argumento_CONT_NÚM ? execução_gerente.argumento_email[가] : 0;
        if (ÍNDICE == 10) return rede_pilha.Abrir(가);
        if (ÍNDICE == 11) {
            int duração_VALOR = MATRIZ_duração(라);
            if (duração_VALOR < 0) return duração_VALOR;
            if (마 < 0 || 마 > duração_VALOR || 마 > 1024) return -90;
            for (int posição = 0; posição < 마; posição++) 임시자료[posição] = execução_gerente.número(라 + 4 + posição * 4) & 255;
            return rede_pilha.enviar(가, SEGUNDO_operando, 다, 임시자료, 마);
        }
        if (ÍNDICE == 12) {
            int duração_VALOR = MATRIZ_duração(SEGUNDO_operando);
            if (duração_VALOR < 0) return duração_VALOR;
            if (다 < 0 || 다 > 2000) return -22;
            int resultado = rede_pilha.receber(가, 임시자료, duração_VALOR < 1024 ? duração_VALOR : 1024, 다);
            if (resultado >= 0) for (int posição = 0; posição < resultado; posição++) execução_gerente.gravar_número(SEGUNDO_operando + 4 + posição * 4, 임시자료[posição]);
            return resultado;
        }
        if (ÍNDICE == 13) return rede_pilha.Fechar(가);
        if (ÍNDICE == 14) return rede_pilha.내주소;
        if (ÍNDICE == 15) return rede_pilha.par_email(가);
        if (ÍNDICE == 16) return rede_pilha.par_número_da_porta(가);
        if (ÍNDICE == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (ÍNDICE == 20 || ÍNDICE == 21) {
            int nome_dimensionar = MATRIZ_duração(가), dados_dimensionar = MATRIZ_duração(SEGUNDO_operando);
            if (nome_dimensionar < 0 || dados_dimensionar < 0) return -14;
            if (nome_dimensionar < 1 || nome_dimensionar > 64) return -22;
            int duração_VALOR = 0;
            while (duração_VALOR < nome_dimensionar && execução_gerente.número(가 + 4 + duração_VALOR * 4) != 0) {
                Memória_sistema_de_arquivos.Nome[duração_VALOR] = execução_gerente.número(가 + 4 + duração_VALOR * 4);
                duração_VALOR++;
            }
            if (!Memória_sistema_de_arquivos.cheque_nome(Memória_sistema_de_arquivos.Nome, duração_VALOR)) return -22;
            if (ÍNDICE == 20) {
                int ficheiro = Memória_sistema_de_arquivos.PROCURAR_entrada(Memória_sistema_de_arquivos.Nome, duração_VALOR);
                if (ficheiro < 0) return ficheiro;
                int Tamanho = Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro];
                if (Tamanho > dados_dimensionar) return -90;
                int Endereço = celular_VALOR.Arquivo_Memória() + ficheiro * Memória_sistema_de_arquivos.최대크기;
                for (int número = 0; número < Tamanho; número++) execução_gerente.gravar_número(SEGUNDO_operando + 4 + número * 4, celular_VALOR.leitura_Memória(Endereço + número));
                return Tamanho;
            }
            if (다 < 0 || 다 > dados_dimensionar) return -22;
            if (다 > Memória_sistema_de_arquivos.최대크기) return -90;
            for (int número = 0; número < 다; número++) Memória_sistema_de_arquivos.Editar_VALOR[número] = execução_gerente.número(SEGUNDO_operando + 4 + número * 4) & 255;
            return Memória_sistema_de_arquivos.Store_VALOR(Memória_sistema_de_arquivos.Nome, duração_VALOR, Memória_sistema_de_arquivos.Editar_VALOR, 다);
        }
        return -38;
    }
}
