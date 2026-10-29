// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 strat_VALUE: 단일 nucleu_VALUE 안의 IPv4/UDP 루프백 Transfer_VALUE.
 * extern_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * termina_un_apel_p 8개, 끝점당 diagramă_informații 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class cu_reacție_în_buclă_rețea {
    static int[] utiliza_VALUE = new int[8];
    static int[] muta_VALUE = new int[8];
    static int[] adresa = new int[8];
    static int[] frontală_VALUE = new int[8];
    static int[] element_COUNT = new int[8];
    static int[] RECEIVED_muta = new int[8];
    static int[] lungime_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] date = new int[32 * 512];
    static int[] Înainte_VALUE = new int[512];
    static int Următorul_participant = 49152;
    static int verifica(int INDEX) { return INDEX >= 32 && INDEX < 40 && utiliza_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (utiliza_VALUE[칸] != 0 && muta_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Următorul_participant++;
            if (Următorul_participant > 65535) Următorul_participant = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int crea_intrare(int regiune_VALUE, int 종류, int caz_VALUE) {
        if (regiune_VALUE != 2) return -97;
        if (종류 != 2 || (caz_VALUE != 0 && caz_VALUE != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (utiliza_VALUE[칸] == 0) {
            utiliza_VALUE[칸] = 1; muta_VALUE[칸] = 0; adresa[칸] = 0; frontală_VALUE[칸] = 0; element_COUNT[칸] = 0; RECEIVED_muta[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int BIND_participant(int INDEX, int ID_rețea, int participant_număr_port) {
        int 칸 = verifica(INDEX);
        if (칸 < 0) return -9;
        if (ID_rețea != 0 && ID_rețea != 0x7f000001) return -99;
        if (muta_VALUE[칸] != 0 || participant_număr_port < 0 || participant_număr_port > 65535) return -22;
        if (participant_număr_port == 0) participant_număr_port = 임시창구();
        if (participant_număr_port < 0) return participant_număr_port;
        if (겹침(participant_număr_port)) return -98;
        muta_VALUE[칸] = participant_număr_port; adresa[칸] = ID_rețea; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Înainte_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Înainte_VALUE[INDEX] : -22; }
    public static int trimite(int INDEX, int ID_rețea, int participant_număr_port, int Mărime) {
        int 칸 = verifica(INDEX);
        if (칸 < 0) return -9;
        if (ID_rețea != 0x7f000001) return -101;
        if (participant_număr_port < 1 || participant_număr_port > 65535) return -22;
        if (Mărime < 0 || Mărime > 512) return -90;
        if (muta_VALUE[칸] == 0) {
            int KR = BIND_participant(INDEX, 0x7f000001, 0);
            if (KR < 0) return KR;
        }
        int destinație_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (utiliza_VALUE[후보] != 0 && muta_VALUE[후보] == participant_număr_port) destinație_VALUE = 후보;
        if (destinație_VALUE < 0) return -111;
        if (element_COUNT[destinație_VALUE] == 4) return -11;
        int index_de_poziție = destinație_VALUE * 4 + (frontală_VALUE[destinație_VALUE] + element_COUNT[destinație_VALUE]) % 4;
        for (int byte_VALUE = 0; byte_VALUE < Mărime; byte_VALUE++) date[index_de_poziție * 512 + byte_VALUE] = Înainte_VALUE[byte_VALUE];
        lungime_VALUE[index_de_poziție] = Mărime; 보낸창구[index_de_poziție] = muta_VALUE[칸]; element_COUNT[destinație_VALUE]++;
        return Mărime;
    }
    public static int primi(int INDEX, int capacitate_VALUE) {
        int 칸 = verifica(INDEX);
        if (칸 < 0) return -9;
        if (capacitate_VALUE < 0 || capacitate_VALUE > 512) return -22;
        if (element_COUNT[칸] == 0) return -11;
        int index_de_poziție = 칸 * 4 + frontală_VALUE[칸];
        int Mărime = lungime_VALUE[index_de_poziție] < capacitate_VALUE ? lungime_VALUE[index_de_poziție] : capacitate_VALUE;
        for (int byte_VALUE = 0; byte_VALUE < Mărime; byte_VALUE++) Înainte_VALUE[byte_VALUE] = date[index_de_poziție * 512 + byte_VALUE];
        RECEIVED_muta[칸] = 보낸창구[index_de_poziție]; frontală_VALUE[칸] = (frontală_VALUE[칸] + 1) % 4; element_COUNT[칸]--;
        return Mărime;
    }
    public static int 창구읽기(int INDEX) { int 칸 = verifica(INDEX); return 칸 < 0 ? -9 : muta_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = verifica(INDEX); return 칸 < 0 ? -9 : adresa[칸]; }
    public static int expeditor_participant(int INDEX) { int 칸 = verifica(INDEX); return 칸 < 0 ? -9 : RECEIVED_muta[칸]; }
    public static int Închide(int INDEX) {
        int 칸 = verifica(INDEX); if (칸 < 0) return -9;
        utiliza_VALUE[칸] = 0; element_COUNT[칸] = 0; muta_VALUE[칸] = 0; return 0;
    }
}
