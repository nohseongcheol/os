// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 sloj_VALUE: 단일 jedro_VALUE 안의 IPv4/UDP 루프백 Prenos_VALUE.
 * zunanji_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * končati_klic_p 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class povratna_zanka_mreža {
    static int[] uporaba_VALUE = new int[8];
    static int[] vrata_VALUE = new int[8];
    static int[] naslov = new int[8];
    static int[] sprednja_VALUE = new int[8];
    static int[] element_COUNT = new int[8];
    static int[] RECEIVED_vrata = new int[8];
    static int[] 길이 = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] podatki = new int[32 * 512];
    static int[] Naprej_VALUE = new int[512];
    static int Naprej_končna_točka = 49152;
    static int 확인(int INDEX) { return INDEX >= 32 && INDEX < 40 && uporaba_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (uporaba_VALUE[칸] != 0 && vrata_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Naprej_končna_točka++;
            if (Naprej_končna_točka > 65535) Naprej_končna_točka = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Ustvari_vnos(int območje_VALUE_0e9a97ab, int 종류, int primer_VALUE) {
        if (območje_VALUE_0e9a97ab != 2) return -97;
        if (종류 != 2 || (primer_VALUE != 0 && primer_VALUE != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (uporaba_VALUE[칸] == 0) {
            uporaba_VALUE[칸] = 1; vrata_VALUE[칸] = 0; naslov[칸] = 0; sprednja_VALUE[칸] = 0; element_COUNT[칸] = 0; RECEIVED_vrata[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int BIND_končna_točka(int INDEX, int omrežni_identifikator, int končna_točka_številka_vrat) {
        int 칸 = 확인(INDEX);
        if (칸 < 0) return -9;
        if (omrežni_identifikator != 0 && omrežni_identifikator != 0x7f000001) return -99;
        if (vrata_VALUE[칸] != 0 || končna_točka_številka_vrat < 0 || končna_točka_številka_vrat > 65535) return -22;
        if (končna_točka_številka_vrat == 0) končna_točka_številka_vrat = 임시창구();
        if (končna_točka_številka_vrat < 0) return končna_točka_številka_vrat;
        if (겹침(končna_točka_številka_vrat)) return -98;
        vrata_VALUE[칸] = končna_točka_številka_vrat; naslov[칸] = omrežni_identifikator; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Naprej_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Naprej_VALUE[INDEX] : -22; }
    public static int poslati(int INDEX, int omrežni_identifikator, int končna_točka_številka_vrat, int Velikost) {
        int 칸 = 확인(INDEX);
        if (칸 < 0) return -9;
        if (omrežni_identifikator != 0x7f000001) return -101;
        if (končna_točka_številka_vrat < 1 || končna_točka_številka_vrat > 65535) return -22;
        if (Velikost < 0 || Velikost > 512) return -90;
        if (vrata_VALUE[칸] == 0) {
            int REZULTAT = BIND_končna_točka(INDEX, 0x7f000001, 0);
            if (REZULTAT < 0) return REZULTAT;
        }
        int cilj_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (uporaba_VALUE[후보] != 0 && vrata_VALUE[후보] == končna_točka_številka_vrat) cilj_VALUE = 후보;
        if (cilj_VALUE < 0) return -111;
        if (element_COUNT[cilj_VALUE] == 4) return -11;
        int kazalec_mesta = cilj_VALUE * 4 + (sprednja_VALUE[cilj_VALUE] + element_COUNT[cilj_VALUE]) % 4;
        for (int bajt_VALUE = 0; bajt_VALUE < Velikost; bajt_VALUE++) podatki[kazalec_mesta * 512 + bajt_VALUE] = Naprej_VALUE[bajt_VALUE];
        길이[kazalec_mesta] = Velikost; 보낸창구[kazalec_mesta] = vrata_VALUE[칸]; element_COUNT[cilj_VALUE]++;
        return Velikost;
    }
    public static int sprejeti_sprejemati_prejeti_prejemati(int INDEX, int zmogljivost_VALUE) {
        int 칸 = 확인(INDEX);
        if (칸 < 0) return -9;
        if (zmogljivost_VALUE < 0 || zmogljivost_VALUE > 512) return -22;
        if (element_COUNT[칸] == 0) return -11;
        int kazalec_mesta = 칸 * 4 + sprednja_VALUE[칸];
        int Velikost = 길이[kazalec_mesta] < zmogljivost_VALUE ? 길이[kazalec_mesta] : zmogljivost_VALUE;
        for (int bajt_VALUE = 0; bajt_VALUE < Velikost; bajt_VALUE++) Naprej_VALUE[bajt_VALUE] = podatki[kazalec_mesta * 512 + bajt_VALUE];
        RECEIVED_vrata[칸] = 보낸창구[kazalec_mesta]; sprednja_VALUE[칸] = (sprednja_VALUE[칸] + 1) % 4; element_COUNT[칸]--;
        return Velikost;
    }
    public static int 창구읽기(int INDEX) { int 칸 = 확인(INDEX); return 칸 < 0 ? -9 : vrata_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = 확인(INDEX); return 칸 < 0 ? -9 : naslov[칸]; }
    public static int pošiljatelj_končna_točka(int INDEX) { int 칸 = 확인(INDEX); return 칸 < 0 ? -9 : RECEIVED_vrata[칸]; }
    public static int Zapri(int INDEX) {
        int 칸 = 확인(INDEX); if (칸 < 0) return -9;
        uporaba_VALUE[칸] = 0; element_COUNT[칸] = 0; vrata_VALUE[칸] = 0; return 0;
    }
}
