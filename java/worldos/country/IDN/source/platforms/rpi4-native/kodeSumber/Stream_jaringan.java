// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_VALUE 안의 연결형 byte_VALUE Stream_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket lapisan_VALUE. */
public final class Stream_jaringan {
    static int[] Status_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], serekan_port = new int[16], tunggu_VALUE = new int[16], teknologi_informasi_batas = new int[16];
    static int[] depan_VALUE = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int Berikutnya_item = 50000;
    static int periksa(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && Status_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int nomor_port) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Status_VALUE[Loop_INDEX] != 0 && teknologi_informasi_batas[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == nomor_port) return true; return false; }
    public static int Buat_entri() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (Status_VALUE[Loop_INDEX] == 0) { Status_VALUE[Loop_INDEX] = 1; serekan_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = depan_VALUE[Loop_INDEX] = 수[Loop_INDEX] = tunggu_VALUE[Loop_INDEX] = teknologi_informasi_batas[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int ikat_peserta(int 열린파일번호, int 통신주소, int nomor_port) {
        int Loop_INDEX = periksa(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (Status_VALUE[Loop_INDEX] != 1 || nomor_port < 0 || nomor_port > 65535) return -22;
        if (nomor_port == 0) { do { nomor_port = Berikutnya_item++; if (Berikutnya_item > 65535) Berikutnya_item = 50000; } while (사용중(nomor_port)); }
        if (사용중(nomor_port)) return -98; port_VALUE[Loop_INDEX] = nomor_port; teknologi_informasi_batas[Loop_INDEX] = 1; Status_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int mendengarkan_peserta(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = periksa(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; Status_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Sambung(int 열린파일번호, int 통신주소, int nomor_port) {
        int Loop_INDEX = periksa(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (nomor_port < 1 || nomor_port > 65535 || Status_VALUE[Loop_INDEX] > 2) return -22;
        int terima_halaman = -1; for (int dalam_posisi = 0; dalam_posisi < 16; dalam_posisi++) if (Status_VALUE[dalam_posisi] == 3 && port_VALUE[dalam_posisi] == nomor_port) terima_halaman = dalam_posisi;
        if (terima_halaman < 0) return -111;
        int 대기여부 = 0; for (int dalam_posisi = 0; dalam_posisi < 16; dalam_posisi++) if (tunggu_VALUE[dalam_posisi] == terima_halaman + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (Status_VALUE[Loop_INDEX] == 1) { int 처리값 = ikat_peserta(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = Buat_entri(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        Status_VALUE[Loop_INDEX] = Status_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALUE[다른번호] = nomor_port; serekan_port[Loop_INDEX] = nomor_port; serekan_port[다른번호] = port_VALUE[Loop_INDEX]; tunggu_VALUE[다른번호] = terima_halaman + 1; return 0;
    }
    public static int terima_koneksi(int 열린파일번호) { int Loop_INDEX = periksa(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 3) return -22; for (int dalam_posisi = 0; dalam_posisi < 16; dalam_posisi++) if (Status_VALUE[dalam_posisi] != 0 && tunggu_VALUE[dalam_posisi] == Loop_INDEX + 1) { tunggu_VALUE[dalam_posisi] = 0; return dalam_posisi + 40; } return -11; }
    public static int Tulis(int 열린파일번호, int entri_COUNT) {
        int Loop_INDEX = periksa(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 4) return -107;
        if (entri_COUNT < 0 || entri_COUNT > 512) return -22; if (entri_COUNT == 0) return 0;
        int dalam_posisi = 짝[Loop_INDEX]; if (dalam_posisi < 0) return -32; int total_COUNT = 1024 - 수[dalam_posisi]; if (total_COUNT == 0) return -11; if (total_COUNT > entri_COUNT) total_COUNT = entri_COUNT;
        for (int Perbandingan_posisi = 0; Perbandingan_posisi < total_COUNT; Perbandingan_posisi++) data[dalam_posisi * 1024 + (depan_VALUE[dalam_posisi] + 수[dalam_posisi] + Perbandingan_posisi) % 1024] = 되돌림망.Maju_VALUE[Perbandingan_posisi]; 수[dalam_posisi] += total_COUNT; return total_COUNT;
    }
    public static int Baca(int 열린파일번호, int entri_COUNT) {
        int Loop_INDEX = periksa(열린파일번호); if (Loop_INDEX < 0) return -9; if (Status_VALUE[Loop_INDEX] != 4) return -107; if (entri_COUNT < 0 || entri_COUNT > 512) return -22;
        if (entri_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (entri_COUNT > 수[Loop_INDEX]) entri_COUNT = 수[Loop_INDEX];
        for (int Perbandingan_posisi = 0; Perbandingan_posisi < entri_COUNT; Perbandingan_posisi++) 되돌림망.Maju_VALUE[Perbandingan_posisi] = data[Loop_INDEX * 1024 + (depan_VALUE[Loop_INDEX] + Perbandingan_posisi) % 1024]; depan_VALUE[Loop_INDEX] = (depan_VALUE[Loop_INDEX] + entri_COUNT) % 1024; 수[Loop_INDEX] -= entri_COUNT; return entri_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = periksa(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = periksa(열린파일번호); return Loop_INDEX < 0 ? -9 : serekan_port[Loop_INDEX]; }
    public static int Tutup(int 열린파일번호) {
        int Loop_INDEX = periksa(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (Status_VALUE[Loop_INDEX] == 3) for (int dalam_posisi = 0; dalam_posisi < 16; dalam_posisi++) if (tunggu_VALUE[dalam_posisi] == Loop_INDEX + 1) { if (짝[dalam_posisi] >= 0) 짝[짝[dalam_posisi]] = -1; Status_VALUE[dalam_posisi] = tunggu_VALUE[dalam_posisi] = teknologi_informasi_batas[dalam_posisi] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; Status_VALUE[Loop_INDEX] = teknologi_informasi_batas[Loop_INDEX] = 수[Loop_INDEX] = tunggu_VALUE[Loop_INDEX] = 0; return 0;
    }
}
