// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 slānis_VALUE: 단일 kodols_VALUE 안의 IPv4/UDP 루프백 nodot_VALUE_630ba093.
 * ārējs_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * beigt_zvanu_p 8개, 끝점당 datogramma 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class atgriezeniskā_cilpa_tīkls {
    static int[] lietot_VALUE = new int[8];
    static int[] ports_VALUE = new int[8];
    static int[] adrese = new int[8];
    static int[] priekšējā_VALUE = new int[8];
    static int[] krājums_COUNT = new int[8];
    static int[] RECEIVED_ports = new int[8];
    static int[] 길이 = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] dati = new int[32 * 512];
    static int[] pārsūtīt_VALUE = new int[512];
    static int Tālāk_dalībnieks = 49152;
    static int verificēt(int INDEX) { return INDEX >= 32 && INDEX < 40 && lietot_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (lietot_VALUE[칸] != 0 && ports_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Tālāk_dalībnieks++;
            if (Tālāk_dalībnieks > 65535) Tālāk_dalībnieks = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int atvērt_ievade(int reģions_VALUE, int 종류, int līguma_vērtība) {
        if (reģions_VALUE != 2) return -97;
        if (종류 != 2 || (līguma_vērtība != 0 && līguma_vērtība != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (lietot_VALUE[칸] == 0) {
            lietot_VALUE[칸] = 1; ports_VALUE[칸] = 0; adrese[칸] = 0; priekšējā_VALUE[칸] = 0; krājums_COUNT[칸] = 0; RECEIVED_ports[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int BIND_dalībnieks(int INDEX, int tīkla_ID, int dalībnieks_porta_numurs) {
        int 칸 = verificēt(INDEX);
        if (칸 < 0) return -9;
        if (tīkla_ID != 0 && tīkla_ID != 0x7f000001) return -99;
        if (ports_VALUE[칸] != 0 || dalībnieks_porta_numurs < 0 || dalībnieks_porta_numurs > 65535) return -22;
        if (dalībnieks_porta_numurs == 0) dalībnieks_porta_numurs = 임시창구();
        if (dalībnieks_porta_numurs < 0) return dalībnieks_porta_numurs;
        if (겹침(dalībnieks_porta_numurs)) return -98;
        ports_VALUE[칸] = dalībnieks_porta_numurs; adrese[칸] = tīkla_ID; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        pārsūtīt_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? pārsūtīt_VALUE[INDEX] : -22; }
    public static int sūtīt(int INDEX, int tīkla_ID, int dalībnieks_porta_numurs, int Izmērs) {
        int 칸 = verificēt(INDEX);
        if (칸 < 0) return -9;
        if (tīkla_ID != 0x7f000001) return -101;
        if (dalībnieks_porta_numurs < 1 || dalībnieks_porta_numurs > 65535) return -22;
        if (Izmērs < 0 || Izmērs > 512) return -90;
        if (ports_VALUE[칸] == 0) {
            int mērs = BIND_dalībnieks(INDEX, 0x7f000001, 0);
            if (mērs < 0) return mērs;
        }
        int mērķis_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (lietot_VALUE[후보] != 0 && ports_VALUE[후보] == dalībnieks_porta_numurs) mērķis_VALUE = 후보;
        if (mērķis_VALUE < 0) return -111;
        if (krājums_COUNT[mērķis_VALUE] == 4) return -11;
        int pozīcijas_indekss = mērķis_VALUE * 4 + (priekšējā_VALUE[mērķis_VALUE] + krājums_COUNT[mērķis_VALUE]) % 4;
        for (int byte_VALUE = 0; byte_VALUE < Izmērs; byte_VALUE++) dati[pozīcijas_indekss * 512 + byte_VALUE] = pārsūtīt_VALUE[byte_VALUE];
        길이[pozīcijas_indekss] = Izmērs; 보낸창구[pozīcijas_indekss] = ports_VALUE[칸]; krājums_COUNT[mērķis_VALUE]++;
        return Izmērs;
    }
    public static int saņemt(int INDEX, int noslodze_VALUE) {
        int 칸 = verificēt(INDEX);
        if (칸 < 0) return -9;
        if (noslodze_VALUE < 0 || noslodze_VALUE > 512) return -22;
        if (krājums_COUNT[칸] == 0) return -11;
        int pozīcijas_indekss = 칸 * 4 + priekšējā_VALUE[칸];
        int Izmērs = 길이[pozīcijas_indekss] < noslodze_VALUE ? 길이[pozīcijas_indekss] : noslodze_VALUE;
        for (int byte_VALUE = 0; byte_VALUE < Izmērs; byte_VALUE++) pārsūtīt_VALUE[byte_VALUE] = dati[pozīcijas_indekss * 512 + byte_VALUE];
        RECEIVED_ports[칸] = 보낸창구[pozīcijas_indekss]; priekšējā_VALUE[칸] = (priekšējā_VALUE[칸] + 1) % 4; krājums_COUNT[칸]--;
        return Izmērs;
    }
    public static int 창구읽기(int INDEX) { int 칸 = verificēt(INDEX); return 칸 < 0 ? -9 : ports_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = verificēt(INDEX); return 칸 < 0 ? -9 : adrese[칸]; }
    public static int sūtītājs_dalībnieks(int INDEX) { int 칸 = verificēt(INDEX); return 칸 < 0 ? -9 : RECEIVED_ports[칸]; }
    public static int Aizvērt(int INDEX) {
        int 칸 = verificēt(INDEX); if (칸 < 0) return -9;
        lietot_VALUE[칸] = 0; krājums_COUNT[칸] = 0; ports_VALUE[칸] = 0; return 0;
    }
}
