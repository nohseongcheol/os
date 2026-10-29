// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 sluoksnis_VALUE: 단일 branduolys_VALUE 안의 IPv4/UDP 루프백 perduoti_VALUE_630ba093.
 * išorinis_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * baigti_pokalbį_p 8개, 끝점당 paketų_kelio_schema 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class ciklinis_testas_tinklas {
    static int[] naudoti_VALUE = new int[8];
    static int[] jungtis_VALUE = new int[8];
    static int[] ADDRESS = new int[8];
    static int[] priekinis_VALUE = new int[8];
    static int[] prekė_COUNT = new int[8];
    static int[] RECEIVED_jungtis = new int[8];
    static int[] 길이 = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] duomenys = new int[32 * 512];
    static int[] Pirmyn_VALUE = new int[512];
    static int toliau_dalyvis = 49152;
    static int patvirtinti(int INDEX) { return INDEX >= 32 && INDEX < 40 && naudoti_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (naudoti_VALUE[칸] != 0 && jungtis_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = toliau_dalyvis++;
            if (toliau_dalyvis > 65535) toliau_dalyvis = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int kurti_įrašas(int sritis_VALUE_0e9a97ab, int 종류, int sutarties_vertė) {
        if (sritis_VALUE_0e9a97ab != 2) return -97;
        if (종류 != 2 || (sutarties_vertė != 0 && sutarties_vertė != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (naudoti_VALUE[칸] == 0) {
            naudoti_VALUE[칸] = 1; jungtis_VALUE[칸] = 0; ADDRESS[칸] = 0; priekinis_VALUE[칸] = 0; prekė_COUNT[칸] = 0; RECEIVED_jungtis[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int BIND_dalyvis(int INDEX, int tinklo_identifikatorius, int dalyvis_prievado_numeris) {
        int 칸 = patvirtinti(INDEX);
        if (칸 < 0) return -9;
        if (tinklo_identifikatorius != 0 && tinklo_identifikatorius != 0x7f000001) return -99;
        if (jungtis_VALUE[칸] != 0 || dalyvis_prievado_numeris < 0 || dalyvis_prievado_numeris > 65535) return -22;
        if (dalyvis_prievado_numeris == 0) dalyvis_prievado_numeris = 임시창구();
        if (dalyvis_prievado_numeris < 0) return dalyvis_prievado_numeris;
        if (겹침(dalyvis_prievado_numeris)) return -98;
        jungtis_VALUE[칸] = dalyvis_prievado_numeris; ADDRESS[칸] = tinklo_identifikatorius; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Pirmyn_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Pirmyn_VALUE[INDEX] : -22; }
    public static int siųsti(int INDEX, int tinklo_identifikatorius, int dalyvis_prievado_numeris, int Dydis) {
        int 칸 = patvirtinti(INDEX);
        if (칸 < 0) return -9;
        if (tinklo_identifikatorius != 0x7f000001) return -101;
        if (dalyvis_prievado_numeris < 1 || dalyvis_prievado_numeris > 65535) return -22;
        if (Dydis < 0 || Dydis > 512) return -90;
        if (jungtis_VALUE[칸] == 0) {
            int REZULTATAS = BIND_dalyvis(INDEX, 0x7f000001, 0);
            if (REZULTATAS < 0) return REZULTATAS;
        }
        int vieta_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (naudoti_VALUE[후보] != 0 && jungtis_VALUE[후보] == dalyvis_prievado_numeris) vieta_VALUE = 후보;
        if (vieta_VALUE < 0) return -111;
        if (prekė_COUNT[vieta_VALUE] == 4) return -11;
        int vietos_rodyklė = vieta_VALUE * 4 + (priekinis_VALUE[vieta_VALUE] + prekė_COUNT[vieta_VALUE]) % 4;
        for (int baitas_VALUE = 0; baitas_VALUE < Dydis; baitas_VALUE++) duomenys[vietos_rodyklė * 512 + baitas_VALUE] = Pirmyn_VALUE[baitas_VALUE];
        길이[vietos_rodyklė] = Dydis; 보낸창구[vietos_rodyklė] = jungtis_VALUE[칸]; prekė_COUNT[vieta_VALUE]++;
        return Dydis;
    }
    public static int gauti(int INDEX, int pajėgumas_VALUE) {
        int 칸 = patvirtinti(INDEX);
        if (칸 < 0) return -9;
        if (pajėgumas_VALUE < 0 || pajėgumas_VALUE > 512) return -22;
        if (prekė_COUNT[칸] == 0) return -11;
        int vietos_rodyklė = 칸 * 4 + priekinis_VALUE[칸];
        int Dydis = 길이[vietos_rodyklė] < pajėgumas_VALUE ? 길이[vietos_rodyklė] : pajėgumas_VALUE;
        for (int baitas_VALUE = 0; baitas_VALUE < Dydis; baitas_VALUE++) Pirmyn_VALUE[baitas_VALUE] = duomenys[vietos_rodyklė * 512 + baitas_VALUE];
        RECEIVED_jungtis[칸] = 보낸창구[vietos_rodyklė]; priekinis_VALUE[칸] = (priekinis_VALUE[칸] + 1) % 4; prekė_COUNT[칸]--;
        return Dydis;
    }
    public static int 창구읽기(int INDEX) { int 칸 = patvirtinti(INDEX); return 칸 < 0 ? -9 : jungtis_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = patvirtinti(INDEX); return 칸 < 0 ? -9 : ADDRESS[칸]; }
    public static int siuntėjas_dalyvis(int INDEX) { int 칸 = patvirtinti(INDEX); return 칸 < 0 ? -9 : RECEIVED_jungtis[칸]; }
    public static int Užverti(int INDEX) {
        int 칸 = patvirtinti(INDEX); if (칸 < 0) return -9;
        naudoti_VALUE[칸] = 0; prekė_COUNT[칸] = 0; jungtis_VALUE[칸] = 0; return 0;
    }
}
