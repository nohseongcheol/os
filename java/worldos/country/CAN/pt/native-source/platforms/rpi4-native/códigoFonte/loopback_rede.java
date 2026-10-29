// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 camada_VALOR: 단일 kernel_VALOR 안의 IPv4/UDP 루프백 Transferir_VALOR.
 * externo_VALOR IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * encerrar_ponto 8개, 끝점당 datagrama 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class loopback_rede {
    static int[] uso_VALOR = new int[8];
    static int[] porta_VALOR = new int[8];
    static int[] Endereço = new int[8];
    static int[] câmera_frontal_VALOR = new int[8];
    static int[] item_CONT_NÚM = new int[8];
    static int[] RECEBER_porta = new int[8];
    static int[] duração_VALOR = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] dados = new int[32 * 512];
    static int[] Avançar_VALOR = new int[512];
    static int Avançar_empresa = 49152;
    static int verificar(int ÍNDICE) { return ÍNDICE >= 32 && ÍNDICE < 40 && uso_VALOR[ÍNDICE - 32] != 0 ? ÍNDICE - 32 : -1; }
    static boolean 겹침(int ÍNDICE) {
        for (int slot_entrada = 0; slot_entrada < 8; slot_entrada++) if (uso_VALOR[slot_entrada] != 0 && porta_VALOR[slot_entrada] == ÍNDICE) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int candidato = Avançar_empresa++;
            if (Avançar_empresa > 65535) Avançar_empresa = 49152;
            if (!겹침(candidato)) return candidato;
        }
        return -98;
    }
    public static int Criar_entrada(int região_VALOR, int Tipo_VALOR, int valor_do_contrato) {
        if (região_VALOR != 2) return -97;
        if (Tipo_VALOR != 2 || (valor_do_contrato != 0 && valor_do_contrato != 17)) return -93;
        for (int slot_entrada = 0; slot_entrada < 8; slot_entrada++) if (uso_VALOR[slot_entrada] == 0) {
            uso_VALOR[slot_entrada] = 1; porta_VALOR[slot_entrada] = 0; Endereço[slot_entrada] = 0; câmera_frontal_VALOR[slot_entrada] = 0; item_CONT_NÚM[slot_entrada] = 0; RECEBER_porta[slot_entrada] = 0;
            return slot_entrada + 32;
        }
        return -24;
    }
    public static int BIND_empresa(int ÍNDICE, int ID_de_rede, int empresa_número_da_porta) {
        int slot_entrada = verificar(ÍNDICE);
        if (slot_entrada < 0) return -9;
        if (ID_de_rede != 0 && ID_de_rede != 0x7f000001) return -99;
        if (porta_VALOR[slot_entrada] != 0 || empresa_número_da_porta < 0 || empresa_número_da_porta > 65535) return -22;
        if (empresa_número_da_porta == 0) empresa_número_da_porta = 임시창구();
        if (empresa_número_da_porta < 0) return empresa_número_da_porta;
        if (겹침(empresa_número_da_porta)) return -98;
        porta_VALOR[slot_entrada] = empresa_número_da_porta; Endereço[slot_entrada] = ID_de_rede; return 0;
    }
    public static int 자료넣기(int ÍNDICE, int VALOR) {
        if (ÍNDICE < 0 || ÍNDICE >= 512) return -22;
        Avançar_VALOR[ÍNDICE] = VALOR & 255; return 0;
    }
    public static int leitura_dados(int ÍNDICE) { return ÍNDICE >= 0 && ÍNDICE < 512 ? Avançar_VALOR[ÍNDICE] : -22; }
    public static int enviar(int ÍNDICE, int ID_de_rede, int empresa_número_da_porta, int Tamanho) {
        int slot_entrada = verificar(ÍNDICE);
        if (slot_entrada < 0) return -9;
        if (ID_de_rede != 0x7f000001) return -101;
        if (empresa_número_da_porta < 1 || empresa_número_da_porta > 65535) return -22;
        if (Tamanho < 0 || Tamanho > 512) return -90;
        if (porta_VALOR[slot_entrada] == 0) {
            int resultado = BIND_empresa(ÍNDICE, 0x7f000001, 0);
            if (resultado < 0) return resultado;
        }
        int destino_VALOR = -1;
        for (int candidato = 0; candidato < 8; candidato++) if (uso_VALOR[candidato] != 0 && porta_VALOR[candidato] == empresa_número_da_porta) destino_VALOR = candidato;
        if (destino_VALOR < 0) return -111;
        if (item_CONT_NÚM[destino_VALOR] == 4) return -11;
        int cargo_ÍNDICE = destino_VALOR * 4 + (câmera_frontal_VALOR[destino_VALOR] + item_CONT_NÚM[destino_VALOR]) % 4;
        for (int byte_VALOR = 0; byte_VALOR < Tamanho; byte_VALOR++) dados[cargo_ÍNDICE * 512 + byte_VALOR] = Avançar_VALOR[byte_VALOR];
        duração_VALOR[cargo_ÍNDICE] = Tamanho; 보낸창구[cargo_ÍNDICE] = porta_VALOR[slot_entrada]; item_CONT_NÚM[destino_VALOR]++;
        return Tamanho;
    }
    public static int receber(int ÍNDICE, int capacidade_VALOR) {
        int slot_entrada = verificar(ÍNDICE);
        if (slot_entrada < 0) return -9;
        if (capacidade_VALOR < 0 || capacidade_VALOR > 512) return -22;
        if (item_CONT_NÚM[slot_entrada] == 0) return -11;
        int cargo_ÍNDICE = slot_entrada * 4 + câmera_frontal_VALOR[slot_entrada];
        int Tamanho = duração_VALOR[cargo_ÍNDICE] < capacidade_VALOR ? duração_VALOR[cargo_ÍNDICE] : capacidade_VALOR;
        for (int byte_VALOR = 0; byte_VALOR < Tamanho; byte_VALOR++) Avançar_VALOR[byte_VALOR] = dados[cargo_ÍNDICE * 512 + byte_VALOR];
        RECEBER_porta[slot_entrada] = 보낸창구[cargo_ÍNDICE]; câmera_frontal_VALOR[slot_entrada] = (câmera_frontal_VALOR[slot_entrada] + 1) % 4; item_CONT_NÚM[slot_entrada]--;
        return Tamanho;
    }
    public static int leitura_empresa_porta(int ÍNDICE) { int slot_entrada = verificar(ÍNDICE); return slot_entrada < 0 ? -9 : porta_VALOR[slot_entrada]; }
    public static int leitura_email(int ÍNDICE) { int slot_entrada = verificar(ÍNDICE); return slot_entrada < 0 ? -9 : Endereço[slot_entrada]; }
    public static int remetente_empresa(int ÍNDICE) { int slot_entrada = verificar(ÍNDICE); return slot_entrada < 0 ? -9 : RECEBER_porta[slot_entrada]; }
    public static int Fechar(int ÍNDICE) {
        int slot_entrada = verificar(ÍNDICE); if (slot_entrada < 0) return -9;
        uso_VALOR[slot_entrada] = 0; item_CONT_NÚM[slot_entrada] = 0; porta_VALOR[slot_entrada] = 0; return 0;
    }
}
