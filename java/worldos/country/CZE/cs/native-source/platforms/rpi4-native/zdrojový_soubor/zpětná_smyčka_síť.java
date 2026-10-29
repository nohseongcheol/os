// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 vrstva_HODNOTA: 단일 jádro_HODNOTA 안의 IPv4/UDP 루프백 přenos_HODNOTA.
 * externí_HODNOTA IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * konec_bod 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class zpětná_smyčka_síť {
    static int[] použít_HODNOTA = new int[8];
    static int[] port_HODNOTA = new int[8];
    static int[] Adresa = new int[8];
    static int[] přední_fotoaparát_HODNOTA = new int[8];
    static int[] zboží_POČET = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] délka_HODNOTA = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] Vpřed_HODNOTA = new int[512];
    static int Další_účastník = 49152;
    static int ověřit(int INDEX) { return INDEX >= 32 && INDEX < 40 && použít_HODNOTA[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int přihrádka_položka = 0; přihrádka_položka < 8; přihrádka_položka++) if (použít_HODNOTA[přihrádka_položka] != 0 && port_HODNOTA[přihrádka_položka] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Další_účastník++;
            if (Další_účastník > 65535) Další_účastník = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Create_položka(int oblast_HODNOTA_0e9a97ab, int Druh_HODNOTA, int hodnota_smlouvy) {
        if (oblast_HODNOTA_0e9a97ab != 2) return -97;
        if (Druh_HODNOTA != 2 || (hodnota_smlouvy != 0 && hodnota_smlouvy != 17)) return -93;
        for (int přihrádka_položka = 0; přihrádka_položka < 8; přihrádka_položka++) if (použít_HODNOTA[přihrádka_položka] == 0) {
            použít_HODNOTA[přihrádka_položka] = 1; port_HODNOTA[přihrádka_položka] = 0; Adresa[přihrádka_položka] = 0; přední_fotoaparát_HODNOTA[přihrádka_položka] = 0; zboží_POČET[přihrádka_položka] = 0; RECEIVED_port[přihrádka_položka] = 0;
            return přihrádka_položka + 32;
        }
        return -24;
    }
    public static int vázat_účastník(int INDEX, int ID_sítě, int účastník_číslo_portu) {
        int přihrádka_položka = ověřit(INDEX);
        if (přihrádka_položka < 0) return -9;
        if (ID_sítě != 0 && ID_sítě != 0x7f000001) return -99;
        if (port_HODNOTA[přihrádka_položka] != 0 || účastník_číslo_portu < 0 || účastník_číslo_portu > 65535) return -22;
        if (účastník_číslo_portu == 0) účastník_číslo_portu = 임시창구();
        if (účastník_číslo_portu < 0) return účastník_číslo_portu;
        if (겹침(účastník_číslo_portu)) return -98;
        port_HODNOTA[přihrádka_položka] = účastník_číslo_portu; Adresa[přihrádka_položka] = ID_sítě; return 0;
    }
    public static int 자료넣기(int INDEX, int HODNOTA) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Vpřed_HODNOTA[INDEX] = HODNOTA & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Vpřed_HODNOTA[INDEX] : -22; }
    public static int poslat(int INDEX, int ID_sítě, int účastník_číslo_portu, int Velikost) {
        int přihrádka_položka = ověřit(INDEX);
        if (přihrádka_položka < 0) return -9;
        if (ID_sítě != 0x7f000001) return -101;
        if (účastník_číslo_portu < 1 || účastník_číslo_portu > 65535) return -22;
        if (Velikost < 0 || Velikost > 512) return -90;
        if (port_HODNOTA[přihrádka_položka] == 0) {
            int VÝSLEDEK = vázat_účastník(INDEX, 0x7f000001, 0);
            if (VÝSLEDEK < 0) return VÝSLEDEK;
        }
        int cíl_HODNOTA = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (použít_HODNOTA[후보] != 0 && port_HODNOTA[후보] == účastník_číslo_portu) cíl_HODNOTA = 후보;
        if (cíl_HODNOTA < 0) return -111;
        if (zboží_POČET[cíl_HODNOTA] == 4) return -11;
        int poziční_index = cíl_HODNOTA * 4 + (přední_fotoaparát_HODNOTA[cíl_HODNOTA] + zboží_POČET[cíl_HODNOTA]) % 4;
        for (int bajt_HODNOTA = 0; bajt_HODNOTA < Velikost; bajt_HODNOTA++) data[poziční_index * 512 + bajt_HODNOTA] = Vpřed_HODNOTA[bajt_HODNOTA];
        délka_HODNOTA[poziční_index] = Velikost; 보낸창구[poziční_index] = port_HODNOTA[přihrádka_položka]; zboží_POČET[cíl_HODNOTA]++;
        return Velikost;
    }
    public static int dostat(int INDEX, int kapacita_HODNOTA) {
        int přihrádka_položka = ověřit(INDEX);
        if (přihrádka_položka < 0) return -9;
        if (kapacita_HODNOTA < 0 || kapacita_HODNOTA > 512) return -22;
        if (zboží_POČET[přihrádka_položka] == 0) return -11;
        int poziční_index = přihrádka_položka * 4 + přední_fotoaparát_HODNOTA[přihrádka_položka];
        int Velikost = délka_HODNOTA[poziční_index] < kapacita_HODNOTA ? délka_HODNOTA[poziční_index] : kapacita_HODNOTA;
        for (int bajt_HODNOTA = 0; bajt_HODNOTA < Velikost; bajt_HODNOTA++) Vpřed_HODNOTA[bajt_HODNOTA] = data[poziční_index * 512 + bajt_HODNOTA];
        RECEIVED_port[přihrádka_položka] = 보낸창구[poziční_index]; přední_fotoaparát_HODNOTA[přihrádka_položka] = (přední_fotoaparát_HODNOTA[přihrádka_položka] + 1) % 4; zboží_POČET[přihrádka_položka]--;
        return Velikost;
    }
    public static int 창구읽기(int INDEX) { int přihrádka_položka = ověřit(INDEX); return přihrádka_položka < 0 ? -9 : port_HODNOTA[přihrádka_položka]; }
    public static int 주소읽기(int INDEX) { int přihrádka_položka = ověřit(INDEX); return přihrádka_položka < 0 ? -9 : Adresa[přihrádka_položka]; }
    public static int odesílatel_účastník(int INDEX) { int přihrádka_položka = ověřit(INDEX); return přihrádka_položka < 0 ? -9 : RECEIVED_port[přihrádka_položka]; }
    public static int Zavřené(int INDEX) {
        int přihrádka_položka = ověřit(INDEX); if (přihrádka_položka < 0) return -9;
        použít_HODNOTA[přihrádka_položka] = 0; zboží_POČET[přihrádka_položka] = 0; port_HODNOTA[přihrádka_položka] = 0; return 0;
    }
}
