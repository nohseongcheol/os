// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 lapisan_VALUE: 단일 kernel_VALUE 안의 IPv4/UDP 루프백 pindah_VALUE.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * tamat_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] e_mel = new int[8];
    static int[] hadapan_VALUE = new int[8];
    static int[] item_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] kepanjangan_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] Mara_VALUE = new int[512];
    static int Seterusnya_peserta = 49152;
    static int tentu_sahkan(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] != 0 && port_VALUE[칸] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Seterusnya_peserta++;
            if (Seterusnya_peserta > 65535) Seterusnya_peserta = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int cipta_pemasukan(int rantau_VALUE, int 종류, int kes_VALUE) {
        if (rantau_VALUE != 2) return -97;
        if (종류 != 2 || (kes_VALUE != 0 && kes_VALUE != 17)) return -93;
        for (int 칸 = 0; 칸 < 8; 칸++) if (사용[칸] == 0) {
            사용[칸] = 1; port_VALUE[칸] = 0; e_mel[칸] = 0; hadapan_VALUE[칸] = 0; item_COUNT[칸] = 0; RECEIVED_port[칸] = 0;
            return 칸 + 32;
        }
        return -24;
    }
    public static int ikat_peserta(int INDEX, int rangkaian_e_mel_df3458bb, int peserta_nombor_port) {
        int 칸 = tentu_sahkan(INDEX);
        if (칸 < 0) return -9;
        if (rangkaian_e_mel_df3458bb != 0 && rangkaian_e_mel_df3458bb != 0x7f000001) return -99;
        if (port_VALUE[칸] != 0 || peserta_nombor_port < 0 || peserta_nombor_port > 65535) return -22;
        if (peserta_nombor_port == 0) peserta_nombor_port = 임시창구();
        if (peserta_nombor_port < 0) return peserta_nombor_port;
        if (겹침(peserta_nombor_port)) return -98;
        port_VALUE[칸] = peserta_nombor_port; e_mel[칸] = rangkaian_e_mel_df3458bb; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Mara_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Mara_VALUE[INDEX] : -22; }
    public static int e_mel_9aee63bd(int INDEX, int rangkaian_e_mel_df3458bb, int peserta_nombor_port, int Saiz) {
        int 칸 = tentu_sahkan(INDEX);
        if (칸 < 0) return -9;
        if (rangkaian_e_mel_df3458bb != 0x7f000001) return -101;
        if (peserta_nombor_port < 1 || peserta_nombor_port > 65535) return -22;
        if (Saiz < 0 || Saiz > 512) return -90;
        if (port_VALUE[칸] == 0) {
            int ukuran = ikat_peserta(INDEX, 0x7f000001, 0);
            if (ukuran < 0) return ukuran;
        }
        int destinasi_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && port_VALUE[후보] == peserta_nombor_port) destinasi_VALUE = 후보;
        if (destinasi_VALUE < 0) return -111;
        if (item_COUNT[destinasi_VALUE] == 4) return -11;
        int jawatan_INDEX = destinasi_VALUE * 4 + (hadapan_VALUE[destinasi_VALUE] + item_COUNT[destinasi_VALUE]) % 4;
        for (int bait_VALUE = 0; bait_VALUE < Saiz; bait_VALUE++) data[jawatan_INDEX * 512 + bait_VALUE] = Mara_VALUE[bait_VALUE];
        kepanjangan_VALUE[jawatan_INDEX] = Saiz; 보낸창구[jawatan_INDEX] = port_VALUE[칸]; item_COUNT[destinasi_VALUE]++;
        return Saiz;
    }
    public static int 받기(int INDEX, int kapasiti_VALUE) {
        int 칸 = tentu_sahkan(INDEX);
        if (칸 < 0) return -9;
        if (kapasiti_VALUE < 0 || kapasiti_VALUE > 512) return -22;
        if (item_COUNT[칸] == 0) return -11;
        int jawatan_INDEX = 칸 * 4 + hadapan_VALUE[칸];
        int Saiz = kepanjangan_VALUE[jawatan_INDEX] < kapasiti_VALUE ? kepanjangan_VALUE[jawatan_INDEX] : kapasiti_VALUE;
        for (int bait_VALUE = 0; bait_VALUE < Saiz; bait_VALUE++) Mara_VALUE[bait_VALUE] = data[jawatan_INDEX * 512 + bait_VALUE];
        RECEIVED_port[칸] = 보낸창구[jawatan_INDEX]; hadapan_VALUE[칸] = (hadapan_VALUE[칸] + 1) % 4; item_COUNT[칸]--;
        return Saiz;
    }
    public static int 창구읽기(int INDEX) { int 칸 = tentu_sahkan(INDEX); return 칸 < 0 ? -9 : port_VALUE[칸]; }
    public static int 주소읽기(int INDEX) { int 칸 = tentu_sahkan(INDEX); return 칸 < 0 ? -9 : e_mel[칸]; }
    public static int penghantar_peserta(int INDEX) { int 칸 = tentu_sahkan(INDEX); return 칸 < 0 ? -9 : RECEIVED_port[칸]; }
    public static int Tutup(int INDEX) {
        int 칸 = tentu_sahkan(INDEX); if (칸 < 0) return -9;
        사용[칸] = 0; item_COUNT[칸] = 0; port_VALUE[칸] = 0; return 0;
    }
}
