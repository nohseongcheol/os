// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 nivå_värde: 단일 kärna_värde 안의 IPv4/UDP 루프백 Överför_värde.
 * extern_värde IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * avsluta_peka 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class loopback_nätverk {
    static int[] använda_värde = new int[8];
    static int[] port_värde = new int[8];
    static int[] Adress = new int[8];
    static int[] framåtvänd_värde = new int[8];
    static int[] objekt_ANTAL = new int[8];
    static int[] BELOPP_port = new int[8];
    static int[] längd_värde = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] Framåt_värde = new int[512];
    static int Nästa_deltagare = 49152;
    static int verifiera(int INDEX) { return INDEX >= 32 && INDEX < 40 && använda_värde[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int fack_post = 0; fack_post < 8; fack_post++) if (använda_värde[fack_post] != 0 && port_värde[fack_post] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int kandidat = Nästa_deltagare++;
            if (Nästa_deltagare > 65535) Nästa_deltagare = 49152;
            if (!겹침(kandidat)) return kandidat;
        }
        return -98;
    }
    public static int Skapa_post(int område_värde_0e9a97ab, int variant_värde, int kontraktsvärde) {
        if (område_värde_0e9a97ab != 2) return -97;
        if (variant_värde != 2 || (kontraktsvärde != 0 && kontraktsvärde != 17)) return -93;
        for (int fack_post = 0; fack_post < 8; fack_post++) if (använda_värde[fack_post] == 0) {
            använda_värde[fack_post] = 1; port_värde[fack_post] = 0; Adress[fack_post] = 0; framåtvänd_värde[fack_post] = 0; objekt_ANTAL[fack_post] = 0; BELOPP_port[fack_post] = 0;
            return fack_post + 32;
        }
        return -24;
    }
    public static int BIND_deltagare(int INDEX, int Nätverks_ID, int deltagare_portnummer) {
        int fack_post = verifiera(INDEX);
        if (fack_post < 0) return -9;
        if (Nätverks_ID != 0 && Nätverks_ID != 0x7f000001) return -99;
        if (port_värde[fack_post] != 0 || deltagare_portnummer < 0 || deltagare_portnummer > 65535) return -22;
        if (deltagare_portnummer == 0) deltagare_portnummer = 임시창구();
        if (deltagare_portnummer < 0) return deltagare_portnummer;
        if (겹침(deltagare_portnummer)) return -98;
        port_värde[fack_post] = deltagare_portnummer; Adress[fack_post] = Nätverks_ID; return 0;
    }
    public static int 자료넣기(int INDEX, int värde) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Framåt_värde[INDEX] = värde & 255; return 0;
    }
    public static int läsa_data(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Framåt_värde[INDEX] : -22; }
    public static int skicka(int INDEX, int Nätverks_ID, int deltagare_portnummer, int Storlek) {
        int fack_post = verifiera(INDEX);
        if (fack_post < 0) return -9;
        if (Nätverks_ID != 0x7f000001) return -101;
        if (deltagare_portnummer < 1 || deltagare_portnummer > 65535) return -22;
        if (Storlek < 0 || Storlek > 512) return -90;
        if (port_värde[fack_post] == 0) {
            int RESULTAT = BIND_deltagare(INDEX, 0x7f000001, 0);
            if (RESULTAT < 0) return RESULTAT;
        }
        int mål_värde = -1;
        for (int kandidat = 0; kandidat < 8; kandidat++) if (använda_värde[kandidat] != 0 && port_värde[kandidat] == deltagare_portnummer) mål_värde = kandidat;
        if (mål_värde < 0) return -111;
        if (objekt_ANTAL[mål_värde] == 4) return -11;
        int positionsindex = mål_värde * 4 + (framåtvänd_värde[mål_värde] + objekt_ANTAL[mål_värde]) % 4;
        for (int byte_värde = 0; byte_värde < Storlek; byte_värde++) data[positionsindex * 512 + byte_värde] = Framåt_värde[byte_värde];
        längd_värde[positionsindex] = Storlek; 보낸창구[positionsindex] = port_värde[fack_post]; objekt_ANTAL[mål_värde]++;
        return Storlek;
    }
    public static int få(int INDEX, int kapacitet_värde) {
        int fack_post = verifiera(INDEX);
        if (fack_post < 0) return -9;
        if (kapacitet_värde < 0 || kapacitet_värde > 512) return -22;
        if (objekt_ANTAL[fack_post] == 0) return -11;
        int positionsindex = fack_post * 4 + framåtvänd_värde[fack_post];
        int Storlek = längd_värde[positionsindex] < kapacitet_värde ? längd_värde[positionsindex] : kapacitet_värde;
        for (int byte_värde = 0; byte_värde < Storlek; byte_värde++) Framåt_värde[byte_värde] = data[positionsindex * 512 + byte_värde];
        BELOPP_port[fack_post] = 보낸창구[positionsindex]; framåtvänd_värde[fack_post] = (framåtvänd_värde[fack_post] + 1) % 4; objekt_ANTAL[fack_post]--;
        return Storlek;
    }
    public static int läsa_deltagare_port(int INDEX) { int fack_post = verifiera(INDEX); return fack_post < 0 ? -9 : port_värde[fack_post]; }
    public static int läsa_ADRESS(int INDEX) { int fack_post = verifiera(INDEX); return fack_post < 0 ? -9 : Adress[fack_post]; }
    public static int avsändare_deltagare(int INDEX) { int fack_post = verifiera(INDEX); return fack_post < 0 ? -9 : BELOPP_port[fack_post]; }
    public static int Stäng(int INDEX) {
        int fack_post = verifiera(INDEX); if (fack_post < 0) return -9;
        använda_värde[fack_post] = 0; objekt_ANTAL[fack_post] = 0; port_värde[fack_post] = 0; return 0;
    }
}
