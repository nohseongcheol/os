// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 laag_WAARDE: 단일 kernel_WAARDE 안의 IPv4/UDP 루프백 transfer_WAARDE.
 * extern_WAARDE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * beëindigen_punt 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class loopback_net {
    static int[] gebruik_WAARDE = new int[8];
    static int[] poort_WAARDE = new int[8];
    static int[] ADRES = new int[8];
    static int[] voorkant_WAARDE = new int[8];
    static int[] item_AANTAL = new int[8];
    static int[] OPBRENGST_poort = new int[8];
    static int[] tijdsduur_WAARDE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] gegevens = new int[32 * 512];
    static int[] Vooruit_WAARDE = new int[512];
    static int Volgende_eindpunt = 49152;
    static int bevestigen(int INDEX) { return INDEX >= 32 && INDEX < 40 && gebruik_WAARDE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int sleuf_invoer = 0; sleuf_invoer < 8; sleuf_invoer++) if (gebruik_WAARDE[sleuf_invoer] != 0 && poort_WAARDE[sleuf_invoer] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int sollicitant = Volgende_eindpunt++;
            if (Volgende_eindpunt > 65535) Volgende_eindpunt = 49152;
            if (!겹침(sollicitant)) return sollicitant;
        }
        return -98;
    }
    public static int maken_invoer(int regio_WAARDE, int soort_WAARDE, int contractwaarde) {
        if (regio_WAARDE != 2) return -97;
        if (soort_WAARDE != 2 || (contractwaarde != 0 && contractwaarde != 17)) return -93;
        for (int sleuf_invoer = 0; sleuf_invoer < 8; sleuf_invoer++) if (gebruik_WAARDE[sleuf_invoer] == 0) {
            gebruik_WAARDE[sleuf_invoer] = 1; poort_WAARDE[sleuf_invoer] = 0; ADRES[sleuf_invoer] = 0; voorkant_WAARDE[sleuf_invoer] = 0; item_AANTAL[sleuf_invoer] = 0; OPBRENGST_poort[sleuf_invoer] = 0;
            return sleuf_invoer + 32;
        }
        return -24;
    }
    public static int BIND_eindpunt(int INDEX, int netwerk_id, int eindpunt_poortnummer) {
        int sleuf_invoer = bevestigen(INDEX);
        if (sleuf_invoer < 0) return -9;
        if (netwerk_id != 0 && netwerk_id != 0x7f000001) return -99;
        if (poort_WAARDE[sleuf_invoer] != 0 || eindpunt_poortnummer < 0 || eindpunt_poortnummer > 65535) return -22;
        if (eindpunt_poortnummer == 0) eindpunt_poortnummer = 임시창구();
        if (eindpunt_poortnummer < 0) return eindpunt_poortnummer;
        if (겹침(eindpunt_poortnummer)) return -98;
        poort_WAARDE[sleuf_invoer] = eindpunt_poortnummer; ADRES[sleuf_invoer] = netwerk_id; return 0;
    }
    public static int 자료넣기(int INDEX, int WAARDE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Vooruit_WAARDE[INDEX] = WAARDE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Vooruit_WAARDE[INDEX] : -22; }
    public static int e_mailen(int INDEX, int netwerk_id, int eindpunt_poortnummer, int Grootte) {
        int sleuf_invoer = bevestigen(INDEX);
        if (sleuf_invoer < 0) return -9;
        if (netwerk_id != 0x7f000001) return -101;
        if (eindpunt_poortnummer < 1 || eindpunt_poortnummer > 65535) return -22;
        if (Grootte < 0 || Grootte > 512) return -90;
        if (poort_WAARDE[sleuf_invoer] == 0) {
            int resultaat = BIND_eindpunt(INDEX, 0x7f000001, 0);
            if (resultaat < 0) return resultaat;
        }
        int doel_WAARDE = -1;
        for (int sollicitant = 0; sollicitant < 8; sollicitant++) if (gebruik_WAARDE[sollicitant] != 0 && poort_WAARDE[sollicitant] == eindpunt_poortnummer) doel_WAARDE = sollicitant;
        if (doel_WAARDE < 0) return -111;
        if (item_AANTAL[doel_WAARDE] == 4) return -11;
        int plaatsingsindex = doel_WAARDE * 4 + (voorkant_WAARDE[doel_WAARDE] + item_AANTAL[doel_WAARDE]) % 4;
        for (int byte_WAARDE = 0; byte_WAARDE < Grootte; byte_WAARDE++) gegevens[plaatsingsindex * 512 + byte_WAARDE] = Vooruit_WAARDE[byte_WAARDE];
        tijdsduur_WAARDE[plaatsingsindex] = Grootte; 보낸창구[plaatsingsindex] = poort_WAARDE[sleuf_invoer]; item_AANTAL[doel_WAARDE]++;
        return Grootte;
    }
    public static int ontvangen(int INDEX, int capaciteit_WAARDE) {
        int sleuf_invoer = bevestigen(INDEX);
        if (sleuf_invoer < 0) return -9;
        if (capaciteit_WAARDE < 0 || capaciteit_WAARDE > 512) return -22;
        if (item_AANTAL[sleuf_invoer] == 0) return -11;
        int plaatsingsindex = sleuf_invoer * 4 + voorkant_WAARDE[sleuf_invoer];
        int Grootte = tijdsduur_WAARDE[plaatsingsindex] < capaciteit_WAARDE ? tijdsduur_WAARDE[plaatsingsindex] : capaciteit_WAARDE;
        for (int byte_WAARDE = 0; byte_WAARDE < Grootte; byte_WAARDE++) Vooruit_WAARDE[byte_WAARDE] = gegevens[plaatsingsindex * 512 + byte_WAARDE];
        OPBRENGST_poort[sleuf_invoer] = 보낸창구[plaatsingsindex]; voorkant_WAARDE[sleuf_invoer] = (voorkant_WAARDE[sleuf_invoer] + 1) % 4; item_AANTAL[sleuf_invoer]--;
        return Grootte;
    }
    public static int 창구읽기(int INDEX) { int sleuf_invoer = bevestigen(INDEX); return sleuf_invoer < 0 ? -9 : poort_WAARDE[sleuf_invoer]; }
    public static int 주소읽기(int INDEX) { int sleuf_invoer = bevestigen(INDEX); return sleuf_invoer < 0 ? -9 : ADRES[sleuf_invoer]; }
    public static int afzender_eindpunt(int INDEX) { int sleuf_invoer = bevestigen(INDEX); return sleuf_invoer < 0 ? -9 : OPBRENGST_poort[sleuf_invoer]; }
    public static int Sluiten(int INDEX) {
        int sleuf_invoer = bevestigen(INDEX); if (sleuf_invoer < 0) return -9;
        gebruik_WAARDE[sleuf_invoer] = 0; item_AANTAL[sleuf_invoer] = 0; poort_WAARDE[sleuf_invoer] = 0; return 0;
    }
}
