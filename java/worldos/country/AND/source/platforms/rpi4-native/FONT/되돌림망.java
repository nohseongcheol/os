// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 capa_VALOR: 단일 nucli_VALOR 안의 IPv4/UDP 루프백 transferir_VALOR.
 * extern_VALOR IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * finalitzar_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] ús_VALOR = new int[8];
    static int[] port_VALOR = new int[8];
    static int[] Adreça = new int[8];
    static int[] frontal_VALOR = new int[8];
    static int[] element_COMPT = new int[8];
    static int[] CANTIDAD_RECIBIDA_port = new int[8];
    static int[] durada_VALOR = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] dades = new int[32 * 512];
    static int[] desviar_VALOR = new int[512];
    static int Següent_extrem = 49152;
    static int verificar(int INDEX) { return INDEX >= 32 && INDEX < 40 && ús_VALOR[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (ús_VALOR[칸] != 0 && port_VALOR[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Següent_extrem++;
            if (Següent_extrem > 65535) Següent_extrem = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Crear_introducció(int 영역, int 종류, int cas_VALOR) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (cas_VALOR != 0 && cas_VALOR != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (ús_VALOR[칸] == 0) {
            ús_VALOR[칸] = 1; port_VALOR[칸] = 0; Adreça[칸] = 0; frontal_VALOR[칸] = 0; element_COMPT[칸] = 0; CANTIDAD_RECIBIDA_port[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int enllaçar_extrem(int INDEX, int xarxa_ADREÇA, int extrem_número_de_port) {
        int 칸 = verificar(INDEX);
        if (칸 < 0) return -9;
        if (xarxa_ADREÇA != 0 && xarxa_ADREÇA != 0x7f000001) return -99;
        if (port_VALOR[칸] != 0 || extrem_número_de_port < 0 || extrem_número_de_port > 65535) return -22;
        if (extrem_número_de_port == 0) extrem_número_de_port = 임시창구();
        if (extrem_número_de_port < 0) return extrem_número_de_port;
        if (겹침(extrem_número_de_port)) return -98;
        port_VALOR[칸] = extrem_número_de_port; Adreça[칸] = xarxa_ADREÇA; return 0;
    }
    public static int 자료넣기(int INDEX, int VALOR) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        desviar_VALOR[INDEX] = VALOR & 255; return 0;
    }
    public static int tancar_dades(int INDEX) { return INDEX >= 0 && INDEX < 512 ? desviar_VALOR[INDEX] : -22; }
    public static int enviar(int INDEX, int xarxa_ADREÇA, int extrem_número_de_port, int Mida) {
        int 칸 = verificar(INDEX);
        if (칸 < 0) return -9;
        if (xarxa_ADREÇA != 0x7f000001) return -101;
        if (extrem_número_de_port < 1 || extrem_número_de_port > 65535) return -22;
        if (Mida < 0 || Mida > 512) return -90;
        if (port_VALOR[칸] == 0) {
            int RESULTAT = enllaçar_extrem(INDEX, 0x7f000001, 0);
            if (RESULTAT < 0) return RESULTAT;
        }
        int destinació_VALOR = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (ús_VALOR[후보] != 0 && port_VALOR[후보] == extrem_número_de_port) destinació_VALOR = 후보;
        if (destinació_VALOR < 0) return -111;
        if (element_COMPT[destinació_VALOR] == 4) return -11;
        int càrrec_INDEX = destinació_VALOR * 4 + (frontal_VALOR[destinació_VALOR] + element_COMPT[destinació_VALOR]) % 4;
        for (int byte_VALOR = 0; byte_VALOR < Mida; byte_VALOR++) dades[càrrec_INDEX * 512 + byte_VALOR] = desviar_VALOR[byte_VALOR];
        durada_VALOR[càrrec_INDEX] = Mida; 보낸창구[càrrec_INDEX] = port_VALOR[칸]; element_COMPT[destinació_VALOR]++;
        return Mida;
    }
    public static int rebre(int INDEX, int capacitat_VALOR) {
        int 칸 = verificar(INDEX);
        if (칸 < 0) return -9;
        if (capacitat_VALOR < 0 || capacitat_VALOR > 512) return -22;
        if (element_COMPT[칸] == 0) return -11;
        int càrrec_INDEX = 칸 * 4 + frontal_VALOR[칸];
        int Mida = durada_VALOR[càrrec_INDEX] < capacitat_VALOR ? durada_VALOR[càrrec_INDEX] : capacitat_VALOR;
        for (int byte_VALOR = 0; byte_VALOR < Mida; byte_VALOR++) desviar_VALOR[byte_VALOR] = dades[càrrec_INDEX * 512 + byte_VALOR];
        CANTIDAD_RECIBIDA_port[칸] = 보낸창구[càrrec_INDEX]; frontal_VALOR[칸] = (frontal_VALOR[칸] + 1) % 4; element_COMPT[칸]--;
        return Mida;
    }
    public static int tancar_extrem_port(int INDEX) { int 칸 = verificar(INDEX); return 칸 < 0 ? -9 : port_VALOR[칸]; }
    public static int tancar_ADREÇA(int INDEX) { int 칸 = verificar(INDEX); return 칸 < 0 ? -9 : Adreça[칸]; }
    public static int emissor_extrem(int INDEX) { int 칸 = verificar(INDEX); return 칸 < 0 ? -9 : CANTIDAD_RECIBIDA_port[칸]; }
    public static int Tanca(int INDEX) {
        int 칸 = verificar(INDEX); if (칸 < 0) return -9;
        ús_VALOR[칸] = 0; element_COMPT[칸] = 0; port_VALOR[칸] = 0; return 0;
    }
}
