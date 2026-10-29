// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 단일 espaço_do_utilizador 과정의 파일서술자와 열린 ficheiro 기술을 분리한다. 호출 번호는 POSIX ABI 문서에 기록한다. */
public final class Arquivo_descritor_gerente {
    static final int 서술자한도 = 32;
    static final int de_leitura_gravação_sinalizar = 2, Criar_entrada = 64, 독점생성 = 128, limpar_Sumário = 512;
    static final int 이어쓰기 = 1024, 기다리지않기 = 2048, 실행시닫기 = 524288;
    static int[] abrir_alça = new int[서술자한도], set_descritor = new int[서술자한도];
    static int[] Tipo_VALOR = new int[서술자한도], meta = new int[서술자한도];
    static int[] Arquivo_cargo_2aa21a9a = new int[서술자한도], abrir_Configurações = new int[서술자한도], Referência_CONT_NÚM = new int[서술자한도];
    static int[] rede_alça = new int[서술자한도], 수신대기밀리초 = new int[서술자한도];
    static int[] caminho_nome = new int[64], Transferir_dados = new int[1024];

    static int PROCURAR_descritor(int Arquivo_descritor) {
        if (Arquivo_descritor < 0 || Arquivo_descritor >= 서술자한도) return -9;
        return abrir_alça[Arquivo_descritor] - 1;
    }
    static int vazio_descritor(int iniciar) {
        for (int ÍNDICE = iniciar; ÍNDICE < 서술자한도; ÍNDICE++) if (abrir_alça[ÍNDICE] == 0) return ÍNDICE;
        return -24;
    }
    static int vazio_alça() {
        for (int ÍNDICE = 0; ÍNDICE < 서술자한도; ÍNDICE++) if (Referência_CONT_NÚM[ÍNDICE] == 0) return ÍNDICE;
        return -24;
    }
    static int Ligar(int descritor_entrada, int descritor_VALOR, int Arquivo_Tipo, int Arquivo_meta, int Definições) {
        abrir_alça[descritor_entrada] = descritor_VALOR + 1; set_descritor[descritor_entrada] = (Definições & 실행시닫기) != 0 ? 1 : 0;
        Tipo_VALOR[descritor_VALOR] = Arquivo_Tipo; meta[descritor_VALOR] = Arquivo_meta; Referência_CONT_NÚM[descritor_VALOR] = 1;
        abrir_Configurações[descritor_VALOR] = Definições & (3 | 이어쓰기 | 기다리지않기); Arquivo_cargo_2aa21a9a[descritor_VALOR] = 0;
        rede_alça[descritor_VALOR] = 0; 수신대기밀리초[descritor_VALOR] = 0;
        return descritor_entrada;
    }
    static void START_Processo() {
        TIRAR_Processo();
        for (int ÍNDICE = 0; ÍNDICE < 3; ÍNDICE++) Ligar(ÍNDICE, ÍNDICE, 1, ÍNDICE, ÍNDICE == 0 ? 0 : 1);
    }
    static void TIRAR_Processo() {
        for (int ÍNDICE = 0; ÍNDICE < 서술자한도; ÍNDICE++) if (abrir_alça[ÍNDICE] != 0) Close_Arquivo(ÍNDICE);
    }
    static int Close_Arquivo(int descritor_entrada) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return -9;
        abrir_alça[descritor_entrada] = 0; set_descritor[descritor_entrada] = 0;
        Referência_CONT_NÚM[descritor_VALOR]--;
        if (Referência_CONT_NÚM[descritor_VALOR] == 0) {
            if (Tipo_VALOR[descritor_VALOR] == 2) Memória_sistema_de_arquivos.abrir_CONT_NÚM[meta[descritor_VALOR]]--;
            if (Tipo_VALOR[descritor_VALOR] == 3 && rede_alça[descritor_VALOR] != 0) rede_pilha.Fechar(rede_alça[descritor_VALOR]);
            Tipo_VALOR[descritor_VALOR] = 0;
        }
        return 0;
    }
    // C 경로는 NUL 끝 byte_VALOR 문자열이다. 루트의 한 이름만 지원한다.
    static int leitura_caminho(int Endereço) {
        if (!execução_gerente.recortar(Endereço, 1)) return -14;
        int posição = celular_VALOR.leitura_Memória(Endereço) == '/' ? 1 : 0;
        for (int duração_VALOR = 0; duração_VALOR < 64; duração_VALOR++) {
            if (!execução_gerente.recortar(Endereço + posição + duração_VALOR, 1)) return -14;
            int VALOR = celular_VALOR.leitura_Memória(Endereço + posição + duração_VALOR);
            caminho_nome[duração_VALOR] = VALOR;
            if (VALOR == 0) return duração_VALOR == 0 ? -2 : (Memória_sistema_de_arquivos.cheque_nome(caminho_nome, duração_VALOR) ? duração_VALOR : -22);
            if (VALOR == '/') return -20;
        }
        return -36;
    }
    static int abrir_Arquivo(int nome_email, int Definições, int concessão_Permissão) {
        int duração_VALOR = leitura_caminho(nome_email);
        if (duração_VALOR < 0) return duração_VALOR;
        if ((Definições & ~(3 | Criar_entrada | 독점생성 | limpar_Sumário | 이어쓰기 | 기다리지않기 | 실행시닫기)) != 0) return -95;
        if ((Definições & 3) == 3 || ((Definições & limpar_Sumário) != 0 && (Definições & 3) == 0)) return -22;
        int ficheiro = Memória_sistema_de_arquivos.PROCURAR_entrada(caminho_nome, duração_VALOR);
        if (ficheiro >= 0 && (Definições & (Criar_entrada | 독점생성)) == (Criar_entrada | 독점생성)) return -17;
        if (ficheiro == -2 && (Definições & Criar_entrada) == 0) return -2;
        int descritor_entrada = vazio_descritor(0), descritor_VALOR = vazio_alça();
        if (descritor_entrada < 0 || descritor_VALOR < 0) return -24;
        if (ficheiro == -2) {
            int resultado = Memória_sistema_de_arquivos.Store_VALOR(caminho_nome, duração_VALOR, caminho_nome, 0);
            if (resultado < 0) return resultado;
            ficheiro = Memória_sistema_de_arquivos.PROCURAR_entrada(caminho_nome, duração_VALOR);
            Memória_sistema_de_arquivos.허가들[ficheiro] = concessão_Permissão & 511;
        }
        if (ficheiro < 0) return ficheiro;
        if ((Definições & limpar_Sumário) != 0) Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro] = 0;
        Memória_sistema_de_arquivos.abrir_CONT_NÚM[ficheiro]++;
        return Ligar(descritor_entrada, descritor_VALOR, 2, ficheiro, Definições);
    }
    static int leitura_Arquivo(int descritor_entrada, int dados_email, int duração_VALOR) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0 || (abrir_Configurações[descritor_VALOR] & 3) == 1) return -9;
        if (duração_VALOR < 0) return -22;
        if (duração_VALOR == 0) return 0;
        if (!execução_gerente.recortar(dados_email, duração_VALOR)) return -14;
        if (Tipo_VALOR[descritor_VALOR] == 3) return receber_datagrama_dados(descritor_entrada, dados_email, duração_VALOR, 0, 0);
        if (Tipo_VALOR[descritor_VALOR] == 1) {
            int RECEBER_CONT_NÚM = 0;
            while (RECEBER_CONT_NÚM < duração_VALOR) {
                int VALOR = SMS_Terminal.직렬읽기();
                if (VALOR < 0) VALOR = teclado.Leitura();
                if (VALOR < 0) {
                    if (RECEBER_CONT_NÚM > 0) return RECEBER_CONT_NÚM;
                    if ((abrir_Configurações[descritor_VALOR] & 기다리지않기) != 0) return -11;
                    if (celular_VALOR.사용자남은밀리초() <= 10) return -11;
                    rede_pilha.verificar(); celular_VALOR.잠시양보();
                } else {
                    celular_VALOR.gravar_Memória(dados_email + RECEBER_CONT_NÚM, VALOR); RECEBER_CONT_NÚM++;
                }
            }
            return RECEBER_CONT_NÚM;
        }
        int ficheiro = meta[descritor_VALOR], posição = Arquivo_cargo_2aa21a9a[descritor_VALOR];
        if (posição >= Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro]) return 0;
        if (duração_VALOR > Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro] - posição) duração_VALOR = Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro] - posição;
        int 원본주소 = celular_VALOR.Arquivo_Memória() + ficheiro * Memória_sistema_de_arquivos.최대크기 + posição;
        for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) celular_VALOR.gravar_Memória(dados_email + ÍNDICE, celular_VALOR.leitura_Memória(원본주소 + ÍNDICE));
        Arquivo_cargo_2aa21a9a[descritor_VALOR] += duração_VALOR;
        return duração_VALOR;
    }
    static int gravar_Arquivo(int descritor_entrada, int dados_email, int duração_VALOR) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0 || (abrir_Configurações[descritor_VALOR] & 3) == 0) return -9;
        if (duração_VALOR < 0) return -22;
        if (duração_VALOR == 0) return 0;
        if (!execução_gerente.recortar(dados_email, duração_VALOR)) return -14;
        if (Tipo_VALOR[descritor_VALOR] == 3) return -89; // 연결하지 않은 자료전문 종단점에는 destino_VALOR 주소가 필요하다.
        if (Tipo_VALOR[descritor_VALOR] == 1) {
            if (duração_VALOR > 16384) duração_VALOR = 16384;
            for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) {
                int VALOR = celular_VALOR.leitura_Memória(dados_email + ÍNDICE);
                SMS_Terminal.직렬바이트(VALOR); SMS_Terminal.tela_caractere(VALOR);
            }
            return duração_VALOR;
        }
        int ficheiro = meta[descritor_VALOR], Tamanho = Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro];
        int posição = (abrir_Configurações[descritor_VALOR] & 이어쓰기) != 0 ? Tamanho : Arquivo_cargo_2aa21a9a[descritor_VALOR];
        if (posição >= Memória_sistema_de_arquivos.최대크기) return -27;
        if (duração_VALOR > Memória_sistema_de_arquivos.최대크기 - posição) duração_VALOR = Memória_sistema_de_arquivos.최대크기 - posição;
        int destino_email = celular_VALOR.Arquivo_Memória() + ficheiro * Memória_sistema_de_arquivos.최대크기;
        for (int ÍNDICE = Tamanho; ÍNDICE < posição; ÍNDICE++) celular_VALOR.gravar_Memória(destino_email + ÍNDICE, 0);
        for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) celular_VALOR.gravar_Memória(destino_email + posição + ÍNDICE, celular_VALOR.leitura_Memória(dados_email + ÍNDICE));
        Arquivo_cargo_2aa21a9a[descritor_VALOR] = posição + duração_VALOR;
        if (posição + duração_VALOR > Tamanho) Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro] = posição + duração_VALOR;
        return duração_VALOR;
    }
    static int busca_Arquivo(int descritor_entrada, int DESLOC_VALOR, int ação_raiz) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return -9;
        if (Tipo_VALOR[descritor_VALOR] != 2) return -29;
        if (ação_raiz < 0 || ação_raiz > 2) return -22;
        int Tela_de_fundo_VALOR = ação_raiz == 0 ? 0 : (ação_raiz == 1 ? Arquivo_cargo_2aa21a9a[descritor_VALOR] : Memória_sistema_de_arquivos.dimensionar_Lista[meta[descritor_VALOR]]);
        if (DESLOC_VALOR > 0 && Tela_de_fundo_VALOR > 2147483647 - DESLOC_VALOR) return -75;
        if (DESLOC_VALOR < 0 && DESLOC_VALOR < -Tela_de_fundo_VALOR) return -22;
        Arquivo_cargo_2aa21a9a[descritor_VALOR] = Tela_de_fundo_VALOR + DESLOC_VALOR;
        return Arquivo_cargo_2aa21a9a[descritor_VALOR];
    }
    static int Duplicar_descritor(int descritor_entrada, int 새서술자, boolean ceder_VALOR, int Definições) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return -9;
        if (새서술자 < 0 || 새서술자 >= 서술자한도) return ceder_VALOR ? -9 : -22;
        if (ceder_VALOR && descritor_entrada == 새서술자) return 새서술자;
        if (ceder_VALOR) { if (abrir_alça[새서술자] != 0) Close_Arquivo(새서술자); }
        else { 새서술자 = vazio_descritor(새서술자); if (새서술자 < 0) return 새서술자; }
        abrir_alça[새서술자] = descritor_VALOR + 1; set_descritor[새서술자] = Definições; Referência_CONT_NÚM[descritor_VALOR]++;
        return 새서술자;
    }
    static int remover_Arquivo_entrada_nome(int nome_email) {
        int duração_VALOR = leitura_caminho(nome_email);
        if (duração_VALOR < 0) return duração_VALOR;
        int ficheiro = Memória_sistema_de_arquivos.PROCURAR_entrada(caminho_nome, duração_VALOR);
        if (ficheiro < 0) return ficheiro;
        Memória_sistema_de_arquivos.이름들[ficheiro * 64] = 0;
        return 0;
    }
    static int set_Arquivo_duração(int descritor_entrada, int duração_VALOR) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return -9;
        if (Tipo_VALOR[descritor_VALOR] != 2 || (abrir_Configurações[descritor_VALOR] & 3) == 0 || duração_VALOR < 0) return -22;
        if (duração_VALOR > Memória_sistema_de_arquivos.최대크기) return -27;
        int ficheiro = meta[descritor_VALOR], Endereço = celular_VALOR.Arquivo_Memória() + ficheiro * Memória_sistema_de_arquivos.최대크기;
        for (int ÍNDICE = Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro]; ÍNDICE < duração_VALOR; ÍNDICE++) celular_VALOR.gravar_Memória(Endereço + ÍNDICE, 0);
        Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro] = duração_VALOR;
        return 0;
    }
    static int leitura_Arquivo_Status(int descritor_entrada, int Endereço) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return -9;
        if (!execução_gerente.recortar(Endereço, 48)) return -14;
        for (int ÍNDICE = 0; ÍNDICE < 12; ÍNDICE++) execução_gerente.gravar_número(Endereço + ÍNDICE * 4, 0);
        int ficheiro = meta[descritor_VALOR], Tamanho = Tipo_VALOR[descritor_VALOR] == 2 ? Memória_sistema_de_arquivos.dimensionar_Lista[ficheiro] : 0;
        int concessão_Permissão = Tipo_VALOR[descritor_VALOR] == 2 ? Memória_sistema_de_arquivos.허가들[ficheiro] : 438;
        execução_gerente.gravar_número(Endereço, 1);
        execução_gerente.gravar_número(Endereço + 4, Tipo_VALOR[descritor_VALOR] == 2 ? ficheiro + 1 : 100 + descritor_VALOR);
        execução_gerente.gravar_número(Endereço + 8, (Tipo_VALOR[descritor_VALOR] == 2 ? 32768 : (Tipo_VALOR[descritor_VALOR] == 1 ? 8192 : 49152)) | concessão_Permissão);
        execução_gerente.gravar_número(Endereço + 12, Tipo_VALOR[descritor_VALOR] == 2 && Memória_sistema_de_arquivos.이름들[ficheiro * 64] == 0 ? 0 : 1);
        execução_gerente.gravar_número(Endereço + 28, Tamanho); execução_gerente.gravar_número(Endereço + 32, 512);
        execução_gerente.gravar_número(Endereço + 36, (Tamanho + 511) / 512);
        return 0;
    }
    static int visual_descritor(int descritor_entrada, int comando, int VALOR) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return -9;
        if (comando == 0 || comando == 1030) return Duplicar_descritor(descritor_entrada, VALOR, false, comando == 1030 ? 1 : 0);
        if (comando == 1) return set_descritor[descritor_entrada];
        if (comando == 2) { if ((VALOR & ~1) != 0) return -22; set_descritor[descritor_entrada] = VALOR; return 0; }
        if (comando == 3) return abrir_Configurações[descritor_VALOR];
        if (comando == 4) {
            if ((VALOR & ~(3 | 이어쓰기 | 기다리지않기)) != 0) return -95;
            abrir_Configurações[descritor_VALOR] = (abrir_Configurações[descritor_VALOR] & 3) | (VALOR & (이어쓰기 | 기다리지않기)); return 0;
        }
        return -95;
    }
    static int Criar_empresa(int 주소체계, int rede_Tipo, int contrato_número) {
        if (주소체계 != 2) return -97;
        if (rede_Tipo != 2) return -93;
        if (contrato_número != 0 && contrato_número != 17) return -93;
        int descritor_entrada = vazio_descritor(0), descritor_VALOR = vazio_alça();
        if (descritor_entrada < 0 || descritor_VALOR < 0) return -24;
        return Ligar(descritor_entrada, descritor_VALOR, 3, 0, de_leitura_gravação_sinalizar);
    }
    static int empresa_descritor(int descritor_entrada) {
        int descritor_VALOR = PROCURAR_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return -9;
        return Tipo_VALOR[descritor_VALOR] == 3 ? descritor_VALOR : -88;
    }
    static int email_32(int Endereço) {
        return celular_VALOR.leitura_Memória(Endereço) << 24 | celular_VALOR.leitura_Memória(Endereço + 1) << 16
            | celular_VALOR.leitura_Memória(Endereço + 2) << 8 | celular_VALOR.leitura_Memória(Endereço + 3);
    }
    static int cheque_email(int Endereço, int duração_VALOR) {
        if (duração_VALOR < 16) return -22;
        if (!execução_gerente.recortar(Endereço, 16)) return -14;
        return execução_gerente.짧은수(Endereço) == 2 ? 0 : -97;
    }
    static int BIND_email(int descritor_entrada, int Endereço, int duração_VALOR) {
        int descritor_VALOR = empresa_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return descritor_VALOR;
        int resultado = cheque_email(Endereço, duração_VALOR);
        if (resultado < 0) return resultado;
        if (rede_alça[descritor_VALOR] != 0) return -22;
        int ID_de_rede = email_32(Endereço + 4);
        if (ID_de_rede != 0 && ID_de_rede != rede_pilha.내주소) return -99;
        int número_da_porta = celular_VALOR.leitura_Memória(Endereço + 2) << 8 | celular_VALOR.leitura_Memória(Endereço + 3);
        resultado = rede_pilha.Abrir(número_da_porta);
        if (resultado < 0) return resultado;
        rede_alça[descritor_VALOR] = resultado; meta[descritor_VALOR] = ID_de_rede;
        return 0;
    }
    static int Automático_BIND(int descritor_VALOR) {
        if (rede_alça[descritor_VALOR] != 0) return 0;
        int resultado = rede_pilha.Abrir(0);
        if (resultado < 0) return resultado;
        rede_alça[descritor_VALOR] = resultado;
        return 0;
    }
    // sendto/recvfrom의 마지막 두 인자는 8바이트 solicitação 구조체로 전달한다.
    static int enviar_datagrama_dados(int descritor_entrada, int dados_email, int duração_VALOR, int Definições, int solicitado_email) {
        int descritor_VALOR = empresa_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return descritor_VALOR;
        if (Definições != 0) return -95;
        if (duração_VALOR < 0 || duração_VALOR > 1024) return -90;
        if (duração_VALOR != 0 && !execução_gerente.recortar(dados_email, duração_VALOR)) return -14;
        if (!execução_gerente.recortar(solicitado_email, 8)) return -14;
        int Endereço = execução_gerente.número(solicitado_email);
        int resultado = cheque_email(Endereço, execução_gerente.número(solicitado_email + 4));
        if (resultado < 0) return resultado;
        int número_da_porta = celular_VALOR.leitura_Memória(Endereço + 2) << 8 | celular_VALOR.leitura_Memória(Endereço + 3);
        if (número_da_porta == 0) return -22;
        resultado = Automático_BIND(descritor_VALOR);
        if (resultado < 0) return resultado;
        for (int ÍNDICE = 0; ÍNDICE < duração_VALOR; ÍNDICE++) Transferir_dados[ÍNDICE] = celular_VALOR.leitura_Memória(dados_email + ÍNDICE);
        return rede_pilha.enviar(rede_alça[descritor_VALOR], email_32(Endereço + 4), número_da_porta, Transferir_dados, duração_VALOR);
    }
    static void gravar_email(int Endereço, int duração_VALOR, int ID_de_rede, int número_da_porta) {
        for (int ÍNDICE = 0; ÍNDICE < duração_VALOR && ÍNDICE < 16; ÍNDICE++) {
            int VALOR = 0;
            if (ÍNDICE == 0) VALOR = 2;
            if (ÍNDICE == 2) VALOR = número_da_porta >>> 8;
            if (ÍNDICE == 3) VALOR = número_da_porta;
            if (ÍNDICE >= 4 && ÍNDICE < 8) VALOR = ID_de_rede >>> (56 - ÍNDICE * 8);
            celular_VALOR.gravar_Memória(Endereço + ÍNDICE, VALOR & 255);
        }
    }
    static int receber_datagrama_dados(int descritor_entrada, int dados_email, int duração_VALOR, int Definições, int solicitado_email) {
        int descritor_VALOR = empresa_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return descritor_VALOR;
        if ((Definições & ~64) != 0) return -95;
        if (duração_VALOR < 0) return -22;
        if (duração_VALOR != 0 && !execução_gerente.recortar(dados_email, duração_VALOR)) return -14;
        int Endereço = 0, email_duração_email = 0, email_duração = 0;
        if (solicitado_email != 0) {
            if (!execução_gerente.recortar(solicitado_email, 8)) return -14;
            Endereço = execução_gerente.número(solicitado_email); email_duração_email = execução_gerente.número(solicitado_email + 4);
            if (Endereço != 0) {
                if (!execução_gerente.recortar(email_duração_email, 4)) return -14;
                email_duração = execução_gerente.número(email_duração_email);
                if (email_duração < 0) return -22;
                if (!execução_gerente.recortar(Endereço, email_duração < 16 ? email_duração : 16)) return -14;
            }
        }
        int resultado = Automático_BIND(descritor_VALOR);
        if (resultado < 0) return resultado;
        int iniciar = celular_VALOR.밀리초();
        while (true) {
            resultado = rede_pilha.receber(rede_alça[descritor_VALOR], Transferir_dados, 1024, 0);
            if (resultado != -11) break;
            if ((Definições & 64) != 0 || (abrir_Configurações[descritor_VALOR] & 기다리지않기) != 0) return -11;
            if (수신대기밀리초[descritor_VALOR] > 0 && celular_VALOR.밀리초() - iniciar >= 수신대기밀리초[descritor_VALOR]) return -11;
            if (celular_VALOR.사용자남은밀리초() <= 10) return -11;
            celular_VALOR.잠시양보();
        }
        if (resultado < 0) return resultado;
        if (resultado > duração_VALOR) resultado = duração_VALOR;
        for (int ÍNDICE = 0; ÍNDICE < resultado; ÍNDICE++) celular_VALOR.gravar_Memória(dados_email + ÍNDICE, Transferir_dados[ÍNDICE]);
        if (Endereço != 0) {
            gravar_email(Endereço, email_duração, rede_pilha.par_email(rede_alça[descritor_VALOR]), rede_pilha.par_número_da_porta(rede_alça[descritor_VALOR]));
            execução_gerente.gravar_número(email_duração_email, 16);
        }
        return resultado;
    }
    static int leitura_soquete_email(int descritor_entrada, int Endereço, int duração_email) {
        int descritor_VALOR = empresa_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return descritor_VALOR;
        if (!execução_gerente.recortar(duração_email, 4)) return -14;
        int duração_VALOR = execução_gerente.número(duração_email);
        if (duração_VALOR < 0) return -22;
        if (!execução_gerente.recortar(Endereço, duração_VALOR < 16 ? duração_VALOR : 16)) return -14;
        int slot_entrada = rede_pilha.ÍNDICE(rede_alça[descritor_VALOR]);
        gravar_email(Endereço, duração_VALOR, meta[descritor_VALOR], slot_entrada < 0 ? 0 : rede_pilha.접속번호들[slot_entrada]);
        execução_gerente.gravar_número(duração_email, 16);
        return 0;
    }
    static int set_receber_TEMPOLIMITE(int descritor_entrada, int 밀리초) {
        int descritor_VALOR = empresa_descritor(descritor_entrada);
        if (descritor_VALOR < 0) return descritor_VALOR;
        if (밀리초 < 0 || 밀리초 > 2000) return -22;
        수신대기밀리초[descritor_VALOR] = 밀리초;
        return 0;
    }
}
