// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 capa_VALOR: 단일 kernel_VALOR 안의 IPv4/UDP 루프백 Transferir_VALOR.
 * externo_VALOR IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * finalizar_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] porto_VALOR = new int[8];
    static int[] ENDEREZO = new int[8];
    static int[] frontal_VALOR = new int[8];
    static int[] elemento_CONTAR = new int[8];
    static int[] RECIBIDO_porto = new int[8];
    static int[] duración_VALOR = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] datos = new int[32 * 512];
    static int[] Adiante_VALOR = new int[512];
    static int Seguinte_extremo = 49152;
    static int verificar(int ÍNDICE) { return ÍNDICE >= 32 && ÍNDICE < 40 && 사용[ÍNDICE - 32] != 0 ? ÍNDICE - 32 : -1; }
    static boolean 겹침(int ÍNDICE) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] != 0 && porto_VALOR[칸] == ÍNDICE) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Seguinte_extremo++;
            if (Seguinte_extremo > 65535) Seguinte_extremo = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int crear_introdución(int 영역, int 종류, int caso_VALOR) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (caso_VALOR != 0 && caso_VALOR != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] == 0) {
            사용[칸] = 1; porto_VALOR[칸] = 0; ENDEREZO[칸] = 0; frontal_VALOR[칸] = 0; elemento_CONTAR[칸] = 0; RECIBIDO_porto[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int ligar_extremo(int ÍNDICE, int Rede_ENDEREZO, int extremo_número_do_porto) {
        int 칸 = verificar(ÍNDICE);
        if (칸 < 0) return -9;
        if (Rede_ENDEREZO != 0 && Rede_ENDEREZO != 0x7f000001) return -99;
        if (porto_VALOR[칸] != 0 || extremo_número_do_porto < 0 || extremo_número_do_porto > 65535) return -22;
        if (extremo_número_do_porto == 0) extremo_número_do_porto = 임시창구();
        if (extremo_número_do_porto < 0) return extremo_número_do_porto;
        if (겹침(extremo_número_do_porto)) return -98;
        porto_VALOR[칸] = extremo_número_do_porto; ENDEREZO[칸] = Rede_ENDEREZO; return 0;
    }
    public static int 자료넣기(int ÍNDICE, int VALOR) {
        if (ÍNDICE < 0 || ÍNDICE >= 512) return -22;
        Adiante_VALOR[ÍNDICE] = VALOR & 255; return 0;
    }
    public static int 자료읽기(int ÍNDICE) { return ÍNDICE >= 0 && ÍNDICE < 512 ? Adiante_VALOR[ÍNDICE] : -22; }
    public static int enviar(int ÍNDICE, int Rede_ENDEREZO, int extremo_número_do_porto, int Tamaño) {
        int 칸 = verificar(ÍNDICE);
        if (칸 < 0) return -9;
        if (Rede_ENDEREZO != 0x7f000001) return -101;
        if (extremo_número_do_porto < 1 || extremo_número_do_porto > 65535) return -22;
        if (Tamaño < 0 || Tamaño > 512) return -90;
        if (porto_VALOR[칸] == 0) {
            int RESULTANTE = ligar_extremo(ÍNDICE, 0x7f000001, 0);
            if (RESULTANTE < 0) return RESULTANTE;
        }
        int destino_VALOR = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && porto_VALOR[후보] == extremo_número_do_porto) destino_VALOR = 후보;
        if (destino_VALOR < 0) return -111;
        if (elemento_CONTAR[destino_VALOR] == 4) return -11;
        int cargo_ÍNDICE = destino_VALOR * 4 + (frontal_VALOR[destino_VALOR] + elemento_CONTAR[destino_VALOR]) % 4;
        for (int byte_VALOR = 0; byte_VALOR < Tamaño; byte_VALOR++) datos[cargo_ÍNDICE * 512 + byte_VALOR] = Adiante_VALOR[byte_VALOR];
        duración_VALOR[cargo_ÍNDICE] = Tamaño; 보낸창구[cargo_ÍNDICE] = porto_VALOR[칸]; elemento_CONTAR[destino_VALOR]++;
        return Tamaño;
    }
    public static int 받기(int ÍNDICE, int capacidade_VALOR) {
        int 칸 = verificar(ÍNDICE);
        if (칸 < 0) return -9;
        if (capacidade_VALOR < 0 || capacidade_VALOR > 512) return -22;
        if (elemento_CONTAR[칸] == 0) return -11;
        int cargo_ÍNDICE = 칸 * 4 + frontal_VALOR[칸];
        int Tamaño = duración_VALOR[cargo_ÍNDICE] < capacidade_VALOR ? duración_VALOR[cargo_ÍNDICE] : capacidade_VALOR;
        for (int byte_VALOR = 0; byte_VALOR < Tamaño; byte_VALOR++) Adiante_VALOR[byte_VALOR] = datos[cargo_ÍNDICE * 512 + byte_VALOR];
        RECIBIDO_porto[칸] = 보낸창구[cargo_ÍNDICE]; frontal_VALOR[칸] = (frontal_VALOR[칸] + 1) % 4; elemento_CONTAR[칸]--;
        return Tamaño;
    }
    public static int 창구읽기(int ÍNDICE) { int 칸 = verificar(ÍNDICE); return 칸 < 0 ? -9 : porto_VALOR[칸]; }
    public static int 주소읽기(int ÍNDICE) { int 칸 = verificar(ÍNDICE); return 칸 < 0 ? -9 : ENDEREZO[칸]; }
    public static int remitente_extremo(int ÍNDICE) { int 칸 = verificar(ÍNDICE); return 칸 < 0 ? -9 : RECIBIDO_porto[칸]; }
    public static int Pechar(int ÍNDICE) {
        int 칸 = verificar(ÍNDICE); if (칸 < 0) return -9;
        사용[칸] = 0; elemento_CONTAR[칸] = 0; porto_VALOR[칸] = 0; return 0;
    }
}
