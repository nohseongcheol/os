// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 Layer_VALUE: 단일 Kernel_VALUE 안의 IPv4/UDP 루프백 Transfer_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * bëennegen_Punkt 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] Port_VALUE = new int[8];
    static int[] Adress = new int[8];
    static int[] 앞 = new int[8];
    static int[] Element_COUNT = new int[8];
    static int[] RECEIVED_Port = new int[8];
    static int[] Längt_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] Daten = new int[32 * 512];
    static int[] Virun_VALUE = new int[512];
    static int 다음창구 = 49152;
    static int verifizéieren(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int Slot_Agab = 0; Slot_Agab < 8; Slot_Agab++) if (사용[Slot_Agab] != 0 && Port_VALUE[Slot_Agab] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = 다음창구++;
            if (다음창구 > 65535) 다음창구 = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Create_Agab(int 영역, int 종류, int Job_VALUE) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (Job_VALUE != 0 && Job_VALUE != 17)) return -93;
        for (int Slot_Agab = 0; Slot_Agab < 8; Slot_Agab++) if (사용[Slot_Agab] == 0) {
            사용[Slot_Agab] = 1; Port_VALUE[Slot_Agab] = 0; Adress[Slot_Agab] = 0; 앞[Slot_Agab] = 0; Element_COUNT[Slot_Agab] = 0; RECEIVED_Port[Slot_Agab] = 0;
            return Slot_Agab + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int Reseau_Adress, int 창구번호) {
        int Slot_Agab = verifizéieren(INDEX);
        if (Slot_Agab < 0) return -9;
        if (Reseau_Adress != 0 && Reseau_Adress != 0x7f000001) return -99;
        if (Port_VALUE[Slot_Agab] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        Port_VALUE[Slot_Agab] = 창구번호; Adress[Slot_Agab] = Reseau_Adress; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Virun_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Virun_VALUE[INDEX] : -22; }
    public static int mailen(int INDEX, int Reseau_Adress, int 창구번호, int d_Gréisst_veränneren) {
        int Slot_Agab = verifizéieren(INDEX);
        if (Slot_Agab < 0) return -9;
        if (Reseau_Adress != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (d_Gréisst_veränneren < 0 || d_Gréisst_veränneren > 512) return -90;
        if (Port_VALUE[Slot_Agab] == 0) {
            int Mooss = 묶기(INDEX, 0x7f000001, 0);
            if (Mooss < 0) return Mooss;
        }
        int Zil_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && Port_VALUE[후보] == 창구번호) Zil_VALUE = 후보;
        if (Zil_VALUE < 0) return -111;
        if (Element_COUNT[Zil_VALUE] == 4) return -11;
        int positionéieren_INDEX = Zil_VALUE * 4 + (앞[Zil_VALUE] + Element_COUNT[Zil_VALUE]) % 4;
        for (int Byte_VALUE = 0; Byte_VALUE < d_Gréisst_veränneren; Byte_VALUE++) Daten[positionéieren_INDEX * 512 + Byte_VALUE] = Virun_VALUE[Byte_VALUE];
        Längt_VALUE[positionéieren_INDEX] = d_Gréisst_veränneren; 보낸창구[positionéieren_INDEX] = Port_VALUE[Slot_Agab]; Element_COUNT[Zil_VALUE]++;
        return d_Gréisst_veränneren;
    }
    public static int 받기(int INDEX, int 용량) {
        int Slot_Agab = verifizéieren(INDEX);
        if (Slot_Agab < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (Element_COUNT[Slot_Agab] == 0) return -11;
        int positionéieren_INDEX = Slot_Agab * 4 + 앞[Slot_Agab];
        int d_Gréisst_veränneren = Längt_VALUE[positionéieren_INDEX] < 용량 ? Längt_VALUE[positionéieren_INDEX] : 용량;
        for (int Byte_VALUE = 0; Byte_VALUE < d_Gréisst_veränneren; Byte_VALUE++) Virun_VALUE[Byte_VALUE] = Daten[positionéieren_INDEX * 512 + Byte_VALUE];
        RECEIVED_Port[Slot_Agab] = 보낸창구[positionéieren_INDEX]; 앞[Slot_Agab] = (앞[Slot_Agab] + 1) % 4; Element_COUNT[Slot_Agab]--;
        return d_Gréisst_veränneren;
    }
    public static int 창구읽기(int INDEX) { int Slot_Agab = verifizéieren(INDEX); return Slot_Agab < 0 ? -9 : Port_VALUE[Slot_Agab]; }
    public static int 주소읽기(int INDEX) { int Slot_Agab = verifizéieren(INDEX); return Slot_Agab < 0 ? -9 : Adress[Slot_Agab]; }
    public static int 보낸곳(int INDEX) { int Slot_Agab = verifizéieren(INDEX); return Slot_Agab < 0 ? -9 : RECEIVED_Port[Slot_Agab]; }
    public static int Clôture(int INDEX) {
        int Slot_Agab = verifizéieren(INDEX); if (Slot_Agab < 0) return -9;
        사용[Slot_Agab] = 0; Element_COUNT[Slot_Agab] = 0; Port_VALUE[Slot_Agab] = 0; return 0;
    }
}
