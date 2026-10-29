// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 vrstva_VALUE: 단일 jadro_VALUE 안의 IPv4/UDP 루프백 prenos_VALUE.
 * externý_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * ukončiť_hovor_bod 8개, 끝점당 datagram 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class spätná_slučka_sieť {
    static int[] používať_VALUE = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] adresa = new int[8];
    static int[] predný_VALUE = new int[8];
    static int[] položka_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] dĺžka_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] údaje = new int[32 * 512];
    static int[] Dopredu_VALUE = new int[512];
    static int Ďalej_účastník = 49152;
    static int overiť(int INDEX) { return INDEX >= 32 && INDEX < 40 && používať_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (používať_VALUE[칸] != 0 && port_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Ďalej_účastník++;
            if (Ďalej_účastník > 65535) Ďalej_účastník = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Create_položka(int oblasť_VALUE_0e9a97ab, int 종류, int prípad_VALUE) {
        if (oblasť_VALUE_0e9a97ab != 2) return -97;
        if (종류 != 2 || (prípad_VALUE != 0 && prípad_VALUE != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (používať_VALUE[칸] == 0) {
            používať_VALUE[칸] = 1; port_VALUE[칸] = 0; adresa[칸] = 0; predný_VALUE[칸] = 0; položka_COUNT[칸] = 0; RECEIVED_port[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int BIND_účastník(int INDEX, int sieťová_identifikácia, int účastník_číslo_portu) {
        int 칸 = overiť(INDEX);
        if (칸 < 0) return -9;
        if (sieťová_identifikácia != 0 && sieťová_identifikácia != 0x7f000001) return -99;
        if (port_VALUE[칸] != 0 || účastník_číslo_portu < 0 || účastník_číslo_portu > 65535) return -22;
        if (účastník_číslo_portu == 0) účastník_číslo_portu = 임시창구();
        if (účastník_číslo_portu < 0) return účastník_číslo_portu;
        if (겹침(účastník_číslo_portu)) return -98;
        port_VALUE[칸] = účastník_číslo_portu; adresa[칸] = sieťová_identifikácia; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Dopredu_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Dopredu_VALUE[INDEX] : -22; }
    public static int odoslať(int INDEX, int sieťová_identifikácia, int účastník_číslo_portu, int Veľkosť) {
        int 칸 = overiť(INDEX);
        if (칸 < 0) return -9;
        if (sieťová_identifikácia != 0x7f000001) return -101;
        if (účastník_číslo_portu < 1 || účastník_číslo_portu > 65535) return -22;
        if (Veľkosť < 0 || Veľkosť > 512) return -90;
        if (port_VALUE[칸] == 0) {
            int KR = BIND_účastník(INDEX, 0x7f000001, 0);
            if (KR < 0) return KR;
        }
        int cieľ_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (používať_VALUE[후보] != 0 && port_VALUE[후보] == účastník_číslo_portu) cieľ_VALUE = 후보;
        if (cieľ_VALUE < 0) return -111;
        if (položka_COUNT[cieľ_VALUE] == 4) return -11;
        int pozičný_index = cieľ_VALUE * 4 + (predný_VALUE[cieľ_VALUE] + položka_COUNT[cieľ_VALUE]) % 4;
        for (int Byte_VALUE = 0; Byte_VALUE < Veľkosť; Byte_VALUE++) údaje[pozičný_index * 512 + Byte_VALUE] = Dopredu_VALUE[Byte_VALUE];
        dĺžka_VALUE[pozičný_index] = Veľkosť; 보낸창구[pozičný_index] = port_VALUE[칸]; položka_COUNT[cieľ_VALUE]++;
        return Veľkosť;
    }
    public static int dostať(int INDEX, int kapacita_VALUE) {
        int 칸 = overiť(INDEX);
        if (칸 < 0) return -9;
        if (kapacita_VALUE < 0 || kapacita_VALUE > 512) return -22;
        if (položka_COUNT[칸] == 0) return -11;
        int pozičný_index = 칸 * 4 + predný_VALUE[칸];
        int Veľkosť = dĺžka_VALUE[pozičný_index] < kapacita_VALUE ? dĺžka_VALUE[pozičný_index] : kapacita_VALUE;
        for (int Byte_VALUE = 0; Byte_VALUE < Veľkosť; Byte_VALUE++) Dopredu_VALUE[Byte_VALUE] = údaje[pozičný_index * 512 + Byte_VALUE];
        RECEIVED_port[칸] = 보낸창구[pozičný_index]; predný_VALUE[칸] = (predný_VALUE[칸] + 1) % 4; položka_COUNT[칸]--;
        return Veľkosť;
    }
    public static int 창구읽기(int INDEX) { int 칸 = overiť(INDEX); return 칸 < 0 ? -9 : port_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = overiť(INDEX); return 칸 < 0 ? -9 : adresa[칸]; }
    public static int odosielateľ_účastník(int INDEX) { int 칸 = overiť(INDEX); return 칸 < 0 ? -9 : RECEIVED_port[칸]; }
    public static int Zatvoriť(int INDEX) {
        int 칸 = overiť(INDEX); if (칸 < 0) return -9;
        používať_VALUE[칸] = 0; položka_COUNT[칸] = 0; port_VALUE[칸] = 0; return 0;
    }
}
