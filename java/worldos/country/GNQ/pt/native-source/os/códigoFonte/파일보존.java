// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_VALOR formato_VALOR. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, geração_número = 0;
    static int[] Arquivo_tabela = new int[1024];
    static int 바이트해시(int VALOR, int dados) { return (VALOR ^ dados) * 16777619; }
    static void limpar_dados() {
        for (int ÍNDICE = 0; ÍNDICE < 512; ÍNDICE++) dispositivo_de_armazenamento_conexão.seção_dados[ÍNDICE] = 0;
    }
    static int tabela_inteiro(int posição) {
        return Arquivo_tabela[posição] | Arquivo_tabela[posição + 1] << 8 | Arquivo_tabela[posição + 2] << 16 | Arquivo_tabela[posição + 3] << 24;
    }
    static void gravar_tabela_inteiro(int posição, int VALOR) {
        for (int ÍNDICE = 0; ÍNDICE < 4; ÍNDICE++) Arquivo_tabela[posição + ÍNDICE] = (VALOR >>> (ÍNDICE * 8)) & 255;
    }
    static boolean cheque_tabela() {
        for (int ficheiro = 0; ficheiro < 8; ficheiro++) {
            int duração_VALOR = 0;
            for (int slot_entrada = 0; slot_entrada < 64; slot_entrada++) Memória_sistema_de_arquivos.Nome[slot_entrada] = Arquivo_tabela[ficheiro * 72 + slot_entrada];
            while (duração_VALOR < 64 && Memória_sistema_de_arquivos.Nome[duração_VALOR] != 0) duração_VALOR++;
            if (duração_VALOR == 0) continue;
            if (!Memória_sistema_de_arquivos.cheque_nome(Memória_sistema_de_arquivos.Nome, duração_VALOR)
                || tabela_inteiro(ficheiro * 72 + 64) < 0 || tabela_inteiro(ficheiro * 72 + 64) > 16384) return false;
            for (int câmera_frontal_VALOR = 0; câmera_frontal_VALOR < ficheiro; câmera_frontal_VALOR++) {
                boolean 같음 = Arquivo_tabela[câmera_frontal_VALOR * 72 + duração_VALOR] == 0;
                for (int slot_entrada = 0; slot_entrada < duração_VALOR; slot_entrada++) if (Arquivo_tabela[câmera_frontal_VALOR * 72 + slot_entrada] != Memória_sistema_de_arquivos.Nome[slot_entrada]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int START_seção = 1 + 보존본 * 259;
        if (dispositivo_de_armazenamento_conexão.Leitura(START_seção) < 0 || dispositivo_de_armazenamento_conexão.analisar_inteiro(0) != 0x4a4b534e) return -1;
        int geração_VALOR = dispositivo_de_armazenamento_conexão.analisar_inteiro(4), soma_de_verificação = dispositivo_de_armazenamento_conexão.analisar_inteiro(8);
        if (geração_VALOR < 1 || dispositivo_de_armazenamento_conexão.analisar_inteiro(12) != (geração_VALOR ^ soma_de_verificação ^ 0x4a4b534e)) return -1;
        int hash_Arquivo = 0x811c9dc5;
        for (int seção_VALOR = 0; seção_VALOR < 258; seção_VALOR++) {
            if (dispositivo_de_armazenamento_conexão.Leitura(START_seção + 1 + seção_VALOR) < 0) return -1;
            for (int slot_entrada = 0; slot_entrada < 512; slot_entrada++) {
                int VALOR = dispositivo_de_armazenamento_conexão.seção_dados[slot_entrada];
                hash_Arquivo = 바이트해시(hash_Arquivo, VALOR);
                if (seção_VALOR < 2) Arquivo_tabela[seção_VALOR * 512 + slot_entrada] = VALOR;
            }
        }
        return hash_Arquivo == soma_de_verificação && cheque_tabela() ? geração_VALOR : -1;
    }
    static int carregarFonte(int 보존본) {
        int START_seção = 1 + 보존본 * 259;
        for (int seção_VALOR = 0; seção_VALOR < 2; seção_VALOR++) {
            if (dispositivo_de_armazenamento_conexão.Leitura(START_seção + 1 + seção_VALOR) < 0) return -5;
            for (int slot_entrada = 0; slot_entrada < 512; slot_entrada++) Arquivo_tabela[seção_VALOR * 512 + slot_entrada] = dispositivo_de_armazenamento_conexão.seção_dados[slot_entrada];
        }
        for (int ficheiro = 0; ficheiro < 8; ficheiro++) {
            for (int slot_entrada = 0; slot_entrada < 64; slot_entrada++) Memória_sistema_de_arquivos.이름들[ficheiro * 64 + slot_entrada] = Arquivo_tabela[ficheiro * 72 + slot_entrada];
            Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro] = Arquivo_tabela[ficheiro * 72] == 0 ? 0 : tabela_inteiro(ficheiro * 72 + 64);
            Memória_sistema_de_arquivos.허가들[ficheiro] = tabela_inteiro(ficheiro * 72 + 68) & 511;
            for (int seção_VALOR = 0; seção_VALOR < 32; seção_VALOR++) {
                if (dispositivo_de_armazenamento_conexão.Leitura(START_seção + 3 + ficheiro * 32 + seção_VALOR) < 0) return -5;
                int Endereço = celular_VALOR.Arquivo_Memória() + ficheiro * 16384 + seção_VALOR * 512;
                for (int slot_entrada = 0; slot_entrada < 512; slot_entrada++) celular_VALOR.gravar_Memória(Endereço + slot_entrada, dispositivo_de_armazenamento_conexão.seção_dados[slot_entrada]);
            }
        }
        return 0;
    }
    static void Preparar() {
        if (dispositivo_de_armazenamento_conexão.Leitura(0) < 0 || dispositivo_de_armazenamento_conexão.analisar_inteiro(0) != 0x54534b4a
            || dispositivo_de_armazenamento_conexão.analisar_inteiro(4) != 0x3145524f || dispositivo_de_armazenamento_conexão.analisar_inteiro(8) != 2048
            || dispositivo_de_armazenamento_conexão.analisar_inteiro(12) != 0x3153464a) {
            SMS_Terminal.Escrita("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        dispositivo_de_armazenamento_conexão.TI_Ativo_9e72441a = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { SMS_Terminal.Escrita("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; geração_número = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (carregarFonte(현재보존본) < 0) {
            SMS_Terminal.Escrita("STORE read failed; halted to preserve files\n"); celular_VALOR.정지();
        }
        SMS_Terminal.Escrita("STORE restored generation "); SMS_Terminal.gravar_número(geração_número); SMS_Terminal.문자(10);
    }
    static int sincronizar() {
        if (!dispositivo_de_armazenamento_conexão.TI_Ativo_9e72441a) return -19;
        if (geração_número == 2147483647) return -75;
        int Avançar_item = 현재보존본 == 0 ? 1 : 0, START_seção = 1 + Avançar_item * 259;
        // 새 본문보다 먼저 Anterior_item commit을 무효화하고 celular_VALOR 캐시를 비운다.
        limpar_dados();
        if (dispositivo_de_armazenamento_conexão.Escrita(START_seção) < 0 || dispositivo_de_armazenamento_conexão.liberar_saída() < 0) return -5;
        for (int slot_entrada = 0; slot_entrada < 1024; slot_entrada++) Arquivo_tabela[slot_entrada] = 0;
        for (int ficheiro = 0; ficheiro < 8; ficheiro++) if (Memória_sistema_de_arquivos.이름들[ficheiro * 64] != 0) {
            for (int slot_entrada = 0; slot_entrada < 64; slot_entrada++) Arquivo_tabela[ficheiro * 72 + slot_entrada] = Memória_sistema_de_arquivos.이름들[ficheiro * 64 + slot_entrada];
            gravar_tabela_inteiro(ficheiro * 72 + 64, Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro]);
            gravar_tabela_inteiro(ficheiro * 72 + 68, Memória_sistema_de_arquivos.허가들[ficheiro]);
        }
        int hash_Arquivo = 0x811c9dc5;
        for (int seção_VALOR = 0; seção_VALOR < 258; seção_VALOR++) {
            for (int slot_entrada = 0; slot_entrada < 512; slot_entrada++) {
                int VALOR = 0;
                if (seção_VALOR < 2) VALOR = Arquivo_tabela[seção_VALOR * 512 + slot_entrada];
                else {
                    int ficheiro = (seção_VALOR - 2) / 32, posição = (seção_VALOR - 2) % 32 * 512 + slot_entrada;
                    if (Arquivo_tabela[ficheiro * 72] != 0 && posição < Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro])
                        VALOR = celular_VALOR.leitura_Memória(celular_VALOR.Arquivo_Memória() + ficheiro * 16384 + posição);
                }
                dispositivo_de_armazenamento_conexão.seção_dados[slot_entrada] = VALOR; hash_Arquivo = 바이트해시(hash_Arquivo, VALOR);
            }
            if (dispositivo_de_armazenamento_conexão.Escrita(START_seção + 1 + seção_VALOR) < 0) return -5;
        }
        if (dispositivo_de_armazenamento_conexão.liberar_saída() < 0) return -5;
        limpar_dados(); dispositivo_de_armazenamento_conexão.gravar_inteiro_VALOR(0, 0x4a4b534e);
        dispositivo_de_armazenamento_conexão.gravar_inteiro_VALOR(4, geração_número + 1); dispositivo_de_armazenamento_conexão.gravar_inteiro_VALOR(8, hash_Arquivo);
        dispositivo_de_armazenamento_conexão.gravar_inteiro_VALOR(12, (geração_número + 1) ^ hash_Arquivo ^ 0x4a4b534e);
        if (dispositivo_de_armazenamento_conexão.Escrita(START_seção) < 0 || dispositivo_de_armazenamento_conexão.liberar_saída() < 0) return -5;
        현재보존본 = Avançar_item; geração_número++;
        return 0;
    }
}
