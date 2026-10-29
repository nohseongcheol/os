// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 lapisan_VALUE: 단일 kernel_VALUE 안의 IPv4/UDP 루프백 Transfer_VALUE.
 * eksternal_VALUE IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * mengakhiri_p 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] gunakan_VALUE = new int[8];
    static int[] port_VALUE = new int[8];
    static int[] surel = new int[8];
    static int[] depan_VALUE = new int[8];
    static int[] item_COUNT = new int[8];
    static int[] RECEIVED_port = new int[8];
    static int[] panjang_VALUE = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] data = new int[32 * 512];
    static int[] Maju_VALUE = new int[512];
    static int Berikutnya_peserta = 49152;
    static int periksa(int INDEX) { return INDEX >= 32 && INDEX < 40 && gunakan_VALUE[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int slot_entri = 0; slot_entri < 8; slot_entri++) if (gunakan_VALUE[slot_entri] != 0 && port_VALUE[slot_entri] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = Berikutnya_peserta++;
            if (Berikutnya_peserta > 65535) Berikutnya_peserta = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int Buat_entri(int wilayah_VALUE, int 종류, int kasus_VALUE) {
        if (wilayah_VALUE != 2) return -97;
        if (종류 != 2 || (kasus_VALUE != 0 && kasus_VALUE != 17)) return -93;
        for (int slot_entri = 0; slot_entri < 8; slot_entri++) if (gunakan_VALUE[slot_entri] == 0) {
            gunakan_VALUE[slot_entri] = 1; port_VALUE[slot_entri] = 0; surel[slot_entri] = 0; depan_VALUE[slot_entri] = 0; item_COUNT[slot_entri] = 0; RECEIVED_port[slot_entri] = 0;
            return slot_entri + 32;
        }
        return -24;
    }
    public static int ikat_peserta(int INDEX, int jaringan_surel, int peserta_nomor_port) {
        int slot_entri = periksa(INDEX);
        if (slot_entri < 0) return -9;
        if (jaringan_surel != 0 && jaringan_surel != 0x7f000001) return -99;
        if (port_VALUE[slot_entri] != 0 || peserta_nomor_port < 0 || peserta_nomor_port > 65535) return -22;
        if (peserta_nomor_port == 0) peserta_nomor_port = 임시창구();
        if (peserta_nomor_port < 0) return peserta_nomor_port;
        if (겹침(peserta_nomor_port)) return -98;
        port_VALUE[slot_entri] = peserta_nomor_port; surel[slot_entri] = jaringan_surel; return 0;
    }
    public static int 자료넣기(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        Maju_VALUE[INDEX] = VALUE & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? Maju_VALUE[INDEX] : -22; }
    public static int kirim(int INDEX, int jaringan_surel, int peserta_nomor_port, int Ukuran) {
        int slot_entri = periksa(INDEX);
        if (slot_entri < 0) return -9;
        if (jaringan_surel != 0x7f000001) return -101;
        if (peserta_nomor_port < 1 || peserta_nomor_port > 65535) return -22;
        if (Ukuran < 0 || Ukuran > 512) return -90;
        if (port_VALUE[slot_entri] == 0) {
            int hasil = ikat_peserta(INDEX, 0x7f000001, 0);
            if (hasil < 0) return hasil;
        }
        int tujuan_VALUE = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (gunakan_VALUE[후보] != 0 && port_VALUE[후보] == peserta_nomor_port) tujuan_VALUE = 후보;
        if (tujuan_VALUE < 0) return -111;
        if (item_COUNT[tujuan_VALUE] == 4) return -11;
        int posisi_INDEX = tujuan_VALUE * 4 + (depan_VALUE[tujuan_VALUE] + item_COUNT[tujuan_VALUE]) % 4;
        for (int byte_VALUE = 0; byte_VALUE < Ukuran; byte_VALUE++) data[posisi_INDEX * 512 + byte_VALUE] = Maju_VALUE[byte_VALUE];
        panjang_VALUE[posisi_INDEX] = Ukuran; 보낸창구[posisi_INDEX] = port_VALUE[slot_entri]; item_COUNT[tujuan_VALUE]++;
        return Ukuran;
    }
    public static int terima(int INDEX, int kapasitas_VALUE) {
        int slot_entri = periksa(INDEX);
        if (slot_entri < 0) return -9;
        if (kapasitas_VALUE < 0 || kapasitas_VALUE > 512) return -22;
        if (item_COUNT[slot_entri] == 0) return -11;
        int posisi_INDEX = slot_entri * 4 + depan_VALUE[slot_entri];
        int Ukuran = panjang_VALUE[posisi_INDEX] < kapasitas_VALUE ? panjang_VALUE[posisi_INDEX] : kapasitas_VALUE;
        for (int byte_VALUE = 0; byte_VALUE < Ukuran; byte_VALUE++) Maju_VALUE[byte_VALUE] = data[posisi_INDEX * 512 + byte_VALUE];
        RECEIVED_port[slot_entri] = 보낸창구[posisi_INDEX]; depan_VALUE[slot_entri] = (depan_VALUE[slot_entri] + 1) % 4; item_COUNT[slot_entri]--;
        return Ukuran;
    }
    public static int 창구읽기(int INDEX) { int slot_entri = periksa(INDEX); return slot_entri < 0 ? -9 : port_VALUE[slot_entri]; }
    public static int 주소읽기(int INDEX) { int slot_entri = periksa(INDEX); return slot_entri < 0 ? -9 : surel[slot_entri]; }
    public static int pengirim_peserta(int INDEX) { int slot_entri = periksa(INDEX); return slot_entri < 0 ? -9 : RECEIVED_port[slot_entri]; }
    public static int Tutup(int INDEX) {
        int slot_entri = periksa(INDEX); if (slot_entri < 0) return -9;
        gunakan_VALUE[slot_entri] = 0; item_COUNT[slot_entri] = 0; port_VALUE[slot_entri] = 0; return 0;
    }
}
