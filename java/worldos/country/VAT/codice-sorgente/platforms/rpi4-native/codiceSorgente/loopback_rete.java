// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 layer_VALORE: 단일 kernel_VALORE 안의 IPv4/UDP 루프백 trasferire_VALORE.
 * esterno_VALORE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * chiudere_p 8개, 끝점당 datagramma 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class loopback_rete {
    static int[] usare_VALORE = new int[8];
    static int[] porta_VALORE = new int[8];
    static int[] e_mail = new int[8];
    static int[] frontale_VALORE = new int[8];
    static int[] articolo_CONTA_NUMERI = new int[8];
    static int[] RICEV_SCAD_porta = new int[8];
    static int[] durata_VALORE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] dati = new int[32 * 512];
    static int[] Avanti_VALORE = new int[512];
    static int Avanti_endpoint = 49152;
    static int verificare(int INDICE) { return INDICE >= 32 && INDICE < 40 && usare_VALORE[INDICE - 32] != 0 ? INDICE - 32 : -1; }
    static boolean 겹침(int INDICE) {
        for (int slot_voce = 0; slot_voce < 8; slot_voce++) if (usare_VALORE[slot_voce] != 0 && porta_VALORE[slot_voce] == INDICE) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int candidato = Avanti_endpoint++;
            if (Avanti_endpoint > 65535) Avanti_endpoint = 49152;
            if (!겹침(candidato)) return candidato;
        }
        return -98;
    }
    public static int Crea_voce(int area_VALORE, int Kind_VALORE, int valore_di_contratto) {
        if (area_VALORE != 2) return -97;
        if (Kind_VALORE != 2 || (valore_di_contratto != 0 && valore_di_contratto != 17)) return -93;
        for (int slot_voce = 0; slot_voce < 8; slot_voce++) if (usare_VALORE[slot_voce] == 0) {
            usare_VALORE[slot_voce] = 1; porta_VALORE[slot_voce] = 0; e_mail[slot_voce] = 0; frontale_VALORE[slot_voce] = 0; articolo_CONTA_NUMERI[slot_voce] = 0; RICEV_SCAD_porta[slot_voce] = 0;
            return slot_voce + 32;
        }
        return -24;
    }
    public static int BIND_endpoint(int INDICE, int ID_rete, int endpoint_numero_di_porta) {
        int slot_voce = verificare(INDICE);
        if (slot_voce < 0) return -9;
        if (ID_rete != 0 && ID_rete != 0x7f000001) return -99;
        if (porta_VALORE[slot_voce] != 0 || endpoint_numero_di_porta < 0 || endpoint_numero_di_porta > 65535) return -22;
        if (endpoint_numero_di_porta == 0) endpoint_numero_di_porta = 임시창구();
        if (endpoint_numero_di_porta < 0) return endpoint_numero_di_porta;
        if (겹침(endpoint_numero_di_porta)) return -98;
        porta_VALORE[slot_voce] = endpoint_numero_di_porta; e_mail[slot_voce] = ID_rete; return 0;
    }
    public static int 자료넣기(int INDICE, int VALORE) {
        if (INDICE < 0 || INDICE >= 512) return -22;
        Avanti_VALORE[INDICE] = VALORE & 255; return 0;
    }
    public static int 자료읽기(int INDICE) { return INDICE >= 0 && INDICE < 512 ? Avanti_VALORE[INDICE] : -22; }
    public static int inviare(int INDICE, int ID_rete, int endpoint_numero_di_porta, int Dimensione) {
        int slot_voce = verificare(INDICE);
        if (slot_voce < 0) return -9;
        if (ID_rete != 0x7f000001) return -101;
        if (endpoint_numero_di_porta < 1 || endpoint_numero_di_porta > 65535) return -22;
        if (Dimensione < 0 || Dimensione > 512) return -90;
        if (porta_VALORE[slot_voce] == 0) {
            int risultato = BIND_endpoint(INDICE, 0x7f000001, 0);
            if (risultato < 0) return risultato;
        }
        int meta_VALORE = -1;
        for (int candidato = 0; candidato < 8; candidato++) if (usare_VALORE[candidato] != 0 && porta_VALORE[candidato] == endpoint_numero_di_porta) meta_VALORE = candidato;
        if (meta_VALORE < 0) return -111;
        if (articolo_CONTA_NUMERI[meta_VALORE] == 4) return -11;
        int funzione_INDICE = meta_VALORE * 4 + (frontale_VALORE[meta_VALORE] + articolo_CONTA_NUMERI[meta_VALORE]) % 4;
        for (int byte_VALORE = 0; byte_VALORE < Dimensione; byte_VALORE++) dati[funzione_INDICE * 512 + byte_VALORE] = Avanti_VALORE[byte_VALORE];
        durata_VALORE[funzione_INDICE] = Dimensione; 보낸창구[funzione_INDICE] = porta_VALORE[slot_voce]; articolo_CONTA_NUMERI[meta_VALORE]++;
        return Dimensione;
    }
    public static int ricevere(int INDICE, int capacità_VALORE) {
        int slot_voce = verificare(INDICE);
        if (slot_voce < 0) return -9;
        if (capacità_VALORE < 0 || capacità_VALORE > 512) return -22;
        if (articolo_CONTA_NUMERI[slot_voce] == 0) return -11;
        int funzione_INDICE = slot_voce * 4 + frontale_VALORE[slot_voce];
        int Dimensione = durata_VALORE[funzione_INDICE] < capacità_VALORE ? durata_VALORE[funzione_INDICE] : capacità_VALORE;
        for (int byte_VALORE = 0; byte_VALORE < Dimensione; byte_VALORE++) Avanti_VALORE[byte_VALORE] = dati[funzione_INDICE * 512 + byte_VALORE];
        RICEV_SCAD_porta[slot_voce] = 보낸창구[funzione_INDICE]; frontale_VALORE[slot_voce] = (frontale_VALORE[slot_voce] + 1) % 4; articolo_CONTA_NUMERI[slot_voce]--;
        return Dimensione;
    }
    public static int 창구읽기(int INDICE) { int slot_voce = verificare(INDICE); return slot_voce < 0 ? -9 : porta_VALORE[slot_voce]; }
    public static int 주소읽기(int INDICE) { int slot_voce = verificare(INDICE); return slot_voce < 0 ? -9 : e_mail[slot_voce]; }
    public static int sender_endpoint(int INDICE) { int slot_voce = verificare(INDICE); return slot_voce < 0 ? -9 : RICEV_SCAD_porta[slot_voce]; }
    public static int Chiudi(int INDICE) {
        int slot_voce = verificare(INDICE); if (slot_voce < 0) return -9;
        usare_VALORE[slot_voce] = 0; articolo_CONTA_NUMERI[slot_voce] = 0; porta_VALORE[slot_voce] = 0; return 0;
    }
}
