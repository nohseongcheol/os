// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kernel_VALUE 안의 연결형 bait_VALUE strim_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket lapisan_VALUE. */
public final class strim_rangkaian {
    static int[] status_VALUE = new int[16], port_VALUE = new int[16], 짝 = new int[16], rakan_port = new int[16], tunggu_VALUE = new int[16], teknologi_maklumat_sempadan = new int[16];
    static int[] hadapan_VALUE = new int[16], 수 = new int[16], data = new int[16 * 1024];
    static int Seterusnya_item = 50000;
    static int tentu_sahkan(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && status_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int nombor_port) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (status_VALUE[Loop_INDEX] != 0 && teknologi_maklumat_sempadan[Loop_INDEX] != 0 && port_VALUE[Loop_INDEX] == nombor_port) return true; return false; }
    public static int cipta_pemasukan() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (status_VALUE[Loop_INDEX] == 0) { status_VALUE[Loop_INDEX] = 1; rakan_port[Loop_INDEX] = port_VALUE[Loop_INDEX] = hadapan_VALUE[Loop_INDEX] = 수[Loop_INDEX] = tunggu_VALUE[Loop_INDEX] = teknologi_maklumat_sempadan[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int ikat_peserta(int 열린파일번호, int 통신주소, int nombor_port) {
        int Loop_INDEX = tentu_sahkan(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (통신주소 != 0 && 통신주소 != 0x7f000001) return -99;
        if (status_VALUE[Loop_INDEX] != 1 || nombor_port < 0 || nombor_port > 65535) return -22;
        if (nombor_port == 0) { do { nombor_port = Seterusnya_item++; if (Seterusnya_item > 65535) Seterusnya_item = 50000; } while (사용중(nombor_port)); }
        if (사용중(nombor_port)) return -98; port_VALUE[Loop_INDEX] = nombor_port; teknologi_maklumat_sempadan[Loop_INDEX] = 1; status_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int dengar_peserta(int 열린파일번호, int tunggakan) { int Loop_INDEX = tentu_sahkan(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 2 || tunggakan < 1) return -22; status_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Sambung(int 열린파일번호, int 통신주소, int nombor_port) {
        int Loop_INDEX = tentu_sahkan(열린파일번호); if (Loop_INDEX < 0) return -9; if (통신주소 != 0x7f000001) return -101;
        if (nombor_port < 1 || nombor_port > 65535 || status_VALUE[Loop_INDEX] > 2) return -22;
        int 수신쪽 = -1; for (int dalaman_jawatan = 0; dalaman_jawatan < 16; dalaman_jawatan++) if (status_VALUE[dalaman_jawatan] == 3 && port_VALUE[dalaman_jawatan] == nombor_port) 수신쪽 = dalaman_jawatan;
        if (수신쪽 < 0) return -111;
        int 대기여부 = 0; for (int dalaman_jawatan = 0; dalaman_jawatan < 16; dalaman_jawatan++) if (tunggu_VALUE[dalaman_jawatan] == 수신쪽 + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (status_VALUE[Loop_INDEX] == 1) { int 처리값 = ikat_peserta(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int 다른번호 = cipta_pemasukan(); if (다른번호 < 0) return 다른번호; 다른번호 -= 40;
        status_VALUE[Loop_INDEX] = status_VALUE[다른번호] = 4; 짝[Loop_INDEX] = 다른번호; 짝[다른번호] = Loop_INDEX; port_VALUE[다른번호] = nombor_port; rakan_port[Loop_INDEX] = nombor_port; rakan_port[다른번호] = port_VALUE[Loop_INDEX]; tunggu_VALUE[다른번호] = 수신쪽 + 1; return 0;
    }
    public static int terima_hubungan(int 열린파일번호) { int Loop_INDEX = tentu_sahkan(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 3) return -22; for (int dalaman_jawatan = 0; dalaman_jawatan < 16; dalaman_jawatan++) if (status_VALUE[dalaman_jawatan] != 0 && tunggu_VALUE[dalaman_jawatan] == Loop_INDEX + 1) { tunggu_VALUE[dalaman_jawatan] = 0; return dalaman_jawatan + 40; } return -11; }
    public static int Tulis(int 열린파일번호, int pemasukan_COUNT) {
        int Loop_INDEX = tentu_sahkan(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 4) return -107;
        if (pemasukan_COUNT < 0 || pemasukan_COUNT > 512) return -22; if (pemasukan_COUNT == 0) return 0;
        int dalaman_jawatan = 짝[Loop_INDEX]; if (dalaman_jawatan < 0) return -32; int 총수 = 1024 - 수[dalaman_jawatan]; if (총수 == 0) return -11; if (총수 > pemasukan_COUNT) 총수 = pemasukan_COUNT;
        for (int Perbandingan_jawatan = 0; Perbandingan_jawatan < 총수; Perbandingan_jawatan++) data[dalaman_jawatan * 1024 + (hadapan_VALUE[dalaman_jawatan] + 수[dalaman_jawatan] + Perbandingan_jawatan) % 1024] = 되돌림망.Mara_VALUE[Perbandingan_jawatan]; 수[dalaman_jawatan] += 총수; return 총수;
    }
    public static int Baca(int 열린파일번호, int pemasukan_COUNT) {
        int Loop_INDEX = tentu_sahkan(열린파일번호); if (Loop_INDEX < 0) return -9; if (status_VALUE[Loop_INDEX] != 4) return -107; if (pemasukan_COUNT < 0 || pemasukan_COUNT > 512) return -22;
        if (pemasukan_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (pemasukan_COUNT > 수[Loop_INDEX]) pemasukan_COUNT = 수[Loop_INDEX];
        for (int Perbandingan_jawatan = 0; Perbandingan_jawatan < pemasukan_COUNT; Perbandingan_jawatan++) 되돌림망.Mara_VALUE[Perbandingan_jawatan] = data[Loop_INDEX * 1024 + (hadapan_VALUE[Loop_INDEX] + Perbandingan_jawatan) % 1024]; hadapan_VALUE[Loop_INDEX] = (hadapan_VALUE[Loop_INDEX] + pemasukan_COUNT) % 1024; 수[Loop_INDEX] -= pemasukan_COUNT; return pemasukan_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = tentu_sahkan(열린파일번호); return Loop_INDEX < 0 ? -9 : port_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = tentu_sahkan(열린파일번호); return Loop_INDEX < 0 ? -9 : rakan_port[Loop_INDEX]; }
    public static int Tutup(int 열린파일번호) {
        int Loop_INDEX = tentu_sahkan(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (status_VALUE[Loop_INDEX] == 3) for (int dalaman_jawatan = 0; dalaman_jawatan < 16; dalaman_jawatan++) if (tunggu_VALUE[dalaman_jawatan] == Loop_INDEX + 1) { if (짝[dalaman_jawatan] >= 0) 짝[짝[dalaman_jawatan]] = -1; status_VALUE[dalaman_jawatan] = tunggu_VALUE[dalaman_jawatan] = teknologi_maklumat_sempadan[dalaman_jawatan] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; status_VALUE[Loop_INDEX] = teknologi_maklumat_sempadan[Loop_INDEX] = 수[Loop_INDEX] = tunggu_VALUE[Loop_INDEX] = 0; return 0;
    }
}
