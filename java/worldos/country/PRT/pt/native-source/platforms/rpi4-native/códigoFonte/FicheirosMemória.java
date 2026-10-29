// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM ficheiro 64개, 파일당 16384바이트, descritor_entrada 16개. 모든 dados/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. negativo_VALOR 반환은 erro 번호다.
 */
public final class FicheirosMemória {
    static final int Arquivo_CONT_NÚM = 64;
    static int[] Nome = new int[Arquivo_CONT_NÚM * 64];
    static int[] 이름길이 = new int[Arquivo_CONT_NÚM];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Conteúdo_VALOR = new int[Arquivo_CONT_NÚM * 4096];
    static int[] duração_VALOR = new int[Arquivo_CONT_NÚM];
    static int[] Referência_CONT_NÚM = new int[Arquivo_CONT_NÚM];
    static int[] uso_VALOR = new int[16];
    static int[] meta = new int[16];
    static int[] posição = new int[16];
    static int[] método_MODO = new int[16];
    static int[] caminho = new int[64];
    static int caminho_duração;

    public static int 파일한도() { return Arquivo_CONT_NÚM; }
    static int leitura_dados(int ficheiro, int cargo_ÍNDICE) { return (Conteúdo_VALOR[ficheiro * 4096 + cargo_ÍNDICE / 4] >>> ((cargo_ÍNDICE & 3) * 8)) & 255; }
    static void gravar_dados(int ficheiro, int cargo_ÍNDICE, int VALOR) {
        int slot_entrada = ficheiro * 4096 + cargo_ÍNDICE / 4, mover_VALOR = (cargo_ÍNDICE & 3) * 8;
        Conteúdo_VALOR[slot_entrada] = (Conteúdo_VALOR[slot_entrada] & ~(255 << mover_VALOR)) | ((VALOR & 255) << mover_VALOR);
    }

    public static int caminho_START(int Tamanho) {
        caminho_duração = 0;
        if (Tamanho < 1 || Tamanho > 63) return -36;
        caminho_duração = Tamanho;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamanho; Loop_ÍNDICE++) caminho[Loop_ÍNDICE] = 0;
        return 0;
    }
    public static int caminho_byte(int ÍNDICE, int VALOR) {
        if (ÍNDICE < 0 || ÍNDICE >= caminho_duração || VALOR < 1 || VALOR > 255) return -22;
        caminho[ÍNDICE] = VALOR; return 0;
    }
    static int PROCURAR_entrada() {
        for (int Arquivo_ÍNDICE = 0; Arquivo_ÍNDICE < Arquivo_CONT_NÚM; Arquivo_ÍNDICE++) if (이름길이[Arquivo_ÍNDICE] > 0 && 이름길이[Arquivo_ÍNDICE] == Canonical_duração && 접두(Nome, Arquivo_ÍNDICE * 64, 이름길이[Arquivo_ÍNDICE], Canonical_VALOR, Canonical_duração)) return Arquivo_ÍNDICE;
        return -1;
    }
    public static int Abrir(int 플래그) {
        if (caminho_duração == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < caminho_duração; Loop_ÍNDICE++) if (caminho[Loop_ÍNDICE] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int resultado = normalizar_VALOR(); if (resultado < 0) return resultado;
        if (PROCURAR_Diretório(Canonical_duração) >= 0) return -21;
        resultado = cheque_pai(); if (resultado < 0) return resultado;
        int ficheiro = PROCURAR_entrada();
        if (ficheiro >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (ficheiro < 0 && (플래그 & 0x40) == 0) return -2;
        int descritor_entrada = -1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (uso_VALOR[Loop_ÍNDICE] == 0) { descritor_entrada = Loop_ÍNDICE; break; }
        if (descritor_entrada < 0) return -24;
        if (ficheiro < 0) {
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Arquivo_CONT_NÚM; Loop_ÍNDICE++) if (이름길이[Loop_ÍNDICE] == 0 && Referência_CONT_NÚM[Loop_ÍNDICE] == 0) { ficheiro = Loop_ÍNDICE; break; }
            if (ficheiro < 0) return -28;
            이름길이[ficheiro] = Canonical_duração;
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Canonical_duração; Loop_ÍNDICE++) Nome[ficheiro * 64 + Loop_ÍNDICE] = Canonical_VALOR[Loop_ÍNDICE];
            duração_VALOR[ficheiro] = 0;
        }
        if ((플래그 & 0x200) != 0) duração_VALOR[ficheiro] = 0;
        uso_VALOR[descritor_entrada] = 1; meta[descritor_entrada] = ficheiro; posição[descritor_entrada] = 0; método_MODO[descritor_entrada] = 플래그;
        Referência_CONT_NÚM[ficheiro]++;
        return descritor_entrada + 3;
    }
    static int verificar(int descritor_entrada) {
        return descritor_entrada >= 3 && descritor_entrada < 19 && uso_VALOR[descritor_entrada - 3] != 0 ? descritor_entrada - 3 : -1;
    }
    public static int Leitura(int descritor_entrada) {
        int slot_entrada = verificar(descritor_entrada);
        if (slot_entrada < 0 || (método_MODO[slot_entrada] & 3) == 1) return -9;
        int ficheiro = meta[slot_entrada];
        if (posição[slot_entrada] >= duração_VALOR[ficheiro]) return 256; // EOF와 real_dados 0x00..0xff 구별
        return leitura_dados(ficheiro, posição[slot_entrada]++);
    }
    public static int Escrita(int descritor_entrada, int VALOR) {
        int slot_entrada = verificar(descritor_entrada);
        if (slot_entrada < 0 || (método_MODO[slot_entrada] & 3) == 0) return -9;
        int ficheiro = meta[slot_entrada];
        if ((método_MODO[slot_entrada] & 0x400) != 0) posição[slot_entrada] = duração_VALOR[ficheiro];
        if (posição[slot_entrada] >= 16384) return -28;
        while (duração_VALOR[ficheiro] < posição[slot_entrada]) gravar_dados(ficheiro, duração_VALOR[ficheiro]++, 0);
        gravar_dados(ficheiro, posição[slot_entrada]++, VALOR);
        if (duração_VALOR[ficheiro] < posição[slot_entrada]) duração_VALOR[ficheiro] = posição[slot_entrada];
        return 1;
    }
    public static int busca_cargo(int descritor_entrada, int 거리, int ação_raiz) {
        int slot_entrada = verificar(descritor_entrada);
        if (slot_entrada < 0) return -9;
        if (ação_raiz < 0 || ação_raiz > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (ação_raiz == 0 ? 0 : ação_raiz == 1 ? posição[slot_entrada] : duração_VALOR[meta[slot_entrada]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        posição[slot_entrada] = 새위치; return 새위치;
    }
    public static int Fechar(int descritor_entrada) {
        int slot_entrada = verificar(descritor_entrada);
        if (slot_entrada < 0) return -9;
        Referência_CONT_NÚM[meta[slot_entrada]]--; uso_VALOR[slot_entrada] = 0; return 0;
    }
    public static int Tamanho(int descritor_entrada) {
        int slot_entrada = verificar(descritor_entrada); return slot_entrada < 0 ? -9 : duração_VALOR[meta[slot_entrada]];
    }
    public static int set_duração(int descritor_entrada, int Tamanho) {
        int slot_entrada = verificar(descritor_entrada);
        if (slot_entrada < 0 || (método_MODO[slot_entrada] & 3) == 0) return -9;
        if (Tamanho < 0 || Tamanho > 16384) return -22;
        int ficheiro = meta[slot_entrada];
        while (duração_VALOR[ficheiro] < Tamanho) gravar_dados(ficheiro, duração_VALOR[ficheiro]++, 0);
        duração_VALOR[ficheiro] = Tamanho; return 0;
    }
    public static int apagar_entrada() {
        if (caminho_duração == 0) return -22;
        int resultado = normalizar_VALOR(); if (resultado < 0) return resultado;
        if (PROCURAR_Diretório(Canonical_duração) >= 0) return -21;
        resultado = cheque_pai(); if (resultado < 0) return resultado;
        int ficheiro = PROCURAR_entrada();
        if (ficheiro < 0) return -2;
        이름길이[ficheiro] = 0; return 0; // 열려 있는 파일은 마지막 close까지 reter_VALOR
    }
    static void entrada_Lista_f07b3200() {
        caminho_START(1); caminho_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int ÍNDICE) {
        if (ÍNDICE < 0 || ÍNDICE >= Arquivo_CONT_NÚM || 이름길이[ÍNDICE] == 0) return 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 이름길이[ÍNDICE]; Loop_ÍNDICE++) if (Nome[ÍNDICE * 64 + Loop_ÍNDICE] == '/') return 0;
        return 이름길이[ÍNDICE];
    }
    public static int 공개이름바이트(int ÍNDICE, int cargo_ÍNDICE) {
        return ÍNDICE >= 0 && ÍNDICE < Arquivo_CONT_NÚM && cargo_ÍNDICE >= 0 && cargo_ÍNDICE < 이름길이[ÍNDICE] ? Nome[ÍNDICE * 64 + cargo_ÍNDICE] : -22;
    }
    public static int 공개파일크기(int ÍNDICE) { return ÍNDICE >= 0 && ÍNDICE < Arquivo_CONT_NÚM ? duração_VALOR[ÍNDICE] : -22; }
    static int[] Canonical_VALOR = new int[64], em_dia_item = new int[64], Diretório_nome = new int[16 * 64], Diretório_duração = new int[16];
    static int Canonical_duração, em_dia_duração;
    static boolean 접두(int[] 이름들, int iniciar, int caminho_VALOR, int[] câmera_frontal_VALOR, int entrelinhamento_caminho) {
        if (caminho_VALOR < entrelinhamento_caminho) return false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < entrelinhamento_caminho; Loop_ÍNDICE++) if (이름들[iniciar + Loop_ÍNDICE] != câmera_frontal_VALOR[Loop_ÍNDICE]) return false;
        return true;
    }
    static int normalizar_VALOR() {
        if (caminho_duração == 0) return -22;
        Canonical_duração = caminho[0] == '/' ? 0 : em_dia_duração;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Canonical_duração; Loop_ÍNDICE++) Canonical_VALOR[Loop_ÍNDICE] = em_dia_item[Loop_ÍNDICE];
        int leitura_cursor = 0;
        while (leitura_cursor < caminho_duração) {
            while (leitura_cursor < caminho_duração && caminho[leitura_cursor] == '/') leitura_cursor++;
            int START_cargo = leitura_cursor; while (leitura_cursor < caminho_duração && caminho[leitura_cursor] != '/') { if (caminho[leitura_cursor] == 0) return -22; leitura_cursor++; }
            int entrada_CONT_NÚM_8f7753a1 = leitura_cursor - START_cargo; if (entrada_CONT_NÚM_8f7753a1 == 0 || entrada_CONT_NÚM_8f7753a1 == 1 && caminho[START_cargo] == '.') continue;
            if (entrada_CONT_NÚM_8f7753a1 == 2 && caminho[START_cargo] == '.' && caminho[START_cargo + 1] == '.') {
                while (Canonical_duração > 0 && Canonical_VALOR[Canonical_duração - 1] != '/') Canonical_duração--;
                if (Canonical_duração > 0) Canonical_duração--;
                continue;
            }
            if (Canonical_duração + entrada_CONT_NÚM_8f7753a1 + (Canonical_duração == 0 ? 0 : 1) > 63) return -36;
            if (Canonical_duração > 0) Canonical_VALOR[Canonical_duração++] = '/';
            for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < leitura_cursor; Loop_ÍNDICE++) Canonical_VALOR[Canonical_duração++] = caminho[Loop_ÍNDICE];
        }
        return 0;
    }
    static int PROCURAR_Diretório(int entrada_CONT_NÚM_8f7753a1) {
        if (entrada_CONT_NÚM_8f7753a1 == 0) return 0;
        for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (Diretório_duração[Loop_ÍNDICE] == entrada_CONT_NÚM_8f7753a1 && 접두(Diretório_nome, Loop_ÍNDICE * 64, entrada_CONT_NÚM_8f7753a1, Canonical_VALOR, entrada_CONT_NÚM_8f7753a1)) return Loop_ÍNDICE;
        return -1;
    }
    static int cheque_pai() {
        int entrada_CONT_NÚM_8f7753a1 = Canonical_duração; while (entrada_CONT_NÚM_8f7753a1 > 0 && Canonical_VALOR[entrada_CONT_NÚM_8f7753a1 - 1] != '/') entrada_CONT_NÚM_8f7753a1--;
        return PROCURAR_Diretório(entrada_CONT_NÚM_8f7753a1 == 0 ? 0 : entrada_CONT_NÚM_8f7753a1 - 1) < 0 ? -2 : 0;
    }
    public static int Criar_Diretório() {
        int 처리값 = normalizar_VALOR(); if (처리값 < 0) return 처리값;
        if (PROCURAR_Diretório(Canonical_duração) >= 0 || PROCURAR_entrada() >= 0) return -17;
        처리값 = cheque_pai(); if (처리값 < 0) return 처리값;
        for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (Diretório_duração[Loop_ÍNDICE] == 0) {
            Diretório_duração[Loop_ÍNDICE] = Canonical_duração; for (int interna_cargo = 0; interna_cargo < Canonical_duração; interna_cargo++) Diretório_nome[Loop_ÍNDICE * 64 + interna_cargo] = Canonical_VALOR[interna_cargo]; return 0;
        }
        return -28;
    }
    public static int entrada_Tipo() {
        int 처리값 = normalizar_VALOR(); if (처리값 < 0) return 처리값;
        if (PROCURAR_Diretório(Canonical_duração) >= 0) return 2;
        return PROCURAR_entrada() >= 0 ? 1 : 0;
    }
    public static int alterar_Diretório() {
        int 처리값 = normalizar_VALOR(); if (처리값 < 0) return 처리값;
        if (PROCURAR_Diretório(Canonical_duração) < 0) return -2;
        em_dia_duração = Canonical_duração; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < em_dia_duração; Loop_ÍNDICE++) em_dia_item[Loop_ÍNDICE] = Canonical_VALOR[Loop_ÍNDICE]; return 0;
    }
    public static int remover_Diretório() {
        int 처리값 = normalizar_VALOR(); if (처리값 < 0) return 처리값;
        int Diretório_número = PROCURAR_Diretório(Canonical_duração); if (Diretório_número < 0) return -2; if (Diretório_número == 0) return -16;
        if (em_dia_duração == Canonical_duração && 접두(em_dia_item, 0, em_dia_duração, Canonical_VALOR, Canonical_duração)) return -16;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Arquivo_CONT_NÚM; Loop_ÍNDICE++) {
            if (이름길이[Loop_ÍNDICE] > Canonical_duração && 접두(Nome, Loop_ÍNDICE * 64, 이름길이[Loop_ÍNDICE], Canonical_VALOR, Canonical_duração) && Nome[Loop_ÍNDICE * 64 + Canonical_duração] == '/') return -39;
        }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) {
            if (Diretório_duração[Loop_ÍNDICE] > Canonical_duração && 접두(Diretório_nome, Loop_ÍNDICE * 64, Diretório_duração[Loop_ÍNDICE], Canonical_VALOR, Canonical_duração) && Diretório_nome[Loop_ÍNDICE * 64 + Canonical_duração] == '/') return -39;
        }
        Diretório_duração[Diretório_número] = 0; return 0;
    }
    public static int Renomear_entrada(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Arquivo_CONT_NÚM || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizar_VALOR(); if (처리값 < 0) return 처리값;
        if (PROCURAR_Diretório(Canonical_duração) >= 0) return -21;
        처리값 = cheque_pai(); if (처리값 < 0) return 처리값;
        int Anterior_VALOR = PROCURAR_entrada(); if (Anterior_VALOR == 원본번호) return 0;
        if (Anterior_VALOR >= 0) 이름길이[Anterior_VALOR] = 0;
        이름길이[원본번호] = Canonical_duração; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Canonical_duração; Loop_ÍNDICE++) Nome[원본번호 * 64 + Loop_ÍNDICE] = Canonical_VALOR[Loop_ÍNDICE]; return 0;
    }
    static int entrada_START(int[] dados_MATRIZ, int 시작점, int entrada_CONT_NÚM_8f7753a1) {
        if (!접두(dados_MATRIZ, 시작점, entrada_CONT_NÚM_8f7753a1, Canonical_VALOR, Canonical_duração)) return -1;
        int START_cargo = Canonical_duração;
        if (START_cargo > 0) { if (entrada_CONT_NÚM_8f7753a1 <= START_cargo || dados_MATRIZ[시작점 + START_cargo] != '/') return -1; START_cargo++; }
        if (entrada_CONT_NÚM_8f7753a1 <= START_cargo) return -1;
        for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < entrada_CONT_NÚM_8f7753a1; Loop_ÍNDICE++) if (dados_MATRIZ[시작점 + Loop_ÍNDICE] == '/') return -1;
        return START_cargo;
    }
    static void em_dia_gravar() { 단말.문자('/'); for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < em_dia_duração; Loop_ÍNDICE++) Quadro.직렬쓰기(em_dia_item[Loop_ÍNDICE]); }
    static int 경로목록() {
        int 처리값 = normalizar_VALOR(); if (처리값 < 0) return 처리값;
        int Arquivo_meta = PROCURAR_entrada();
        if (Arquivo_meta >= 0) { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Canonical_duração; Loop_ÍNDICE++) Quadro.직렬쓰기(Canonical_VALOR[Loop_ÍNDICE]); 단말.Escrita("  "); 단말.número(duração_VALOR[Arquivo_meta]); 단말.Escrita("byte_VALOR(주기억 ficheiro)\n"); return 0; }
        if (PROCURAR_Diretório(Canonical_duração) < 0) return -2;
        for (int à_direita_VALOR = 1; à_direita_VALOR < 16; à_direita_VALOR++) if (Diretório_duração[à_direita_VALOR] > 0) {
            int START_cargo = entrada_START(Diretório_nome, à_direita_VALOR * 64, Diretório_duração[à_direita_VALOR]); if (START_cargo < 0) continue;
            for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < Diretório_duração[à_direita_VALOR]; Loop_ÍNDICE++) Quadro.직렬쓰기(Diretório_nome[à_direita_VALOR * 64 + Loop_ÍNDICE]); 단말.Escrita("/\n");
        }
        for (int Arquivo_ÍNDICE = 0; Arquivo_ÍNDICE < Arquivo_CONT_NÚM; Arquivo_ÍNDICE++) if (이름길이[Arquivo_ÍNDICE] > 0) {
            int START_cargo = entrada_START(Nome, Arquivo_ÍNDICE * 64, 이름길이[Arquivo_ÍNDICE]); if (START_cargo < 0) continue;
            for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < 이름길이[Arquivo_ÍNDICE]; Loop_ÍNDICE++) Quadro.직렬쓰기(Nome[Arquivo_ÍNDICE * 64 + Loop_ÍNDICE]);
            단말.Escrita("  "); 단말.número(duração_VALOR[Arquivo_ÍNDICE]); 단말.Escrita("byte_VALOR(주기억 ficheiro)\n");
        }
        return 0;
    }
}
