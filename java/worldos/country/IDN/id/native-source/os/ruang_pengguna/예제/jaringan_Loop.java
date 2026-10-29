// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Ukuran/홀수 panjang_VALUE 데이터그램으로 aktual_data RTL8139 terima_VALUE Loop_VALUE 순환을 시험한다. */
public final class jaringan_Loop {
    public static int jalankan() {
        if (ruang_pengguna.인수개수() != 1) { ruang_pengguna.Tulis("Usage: run stress PORT\n"); return 2; }
        String teks = ruang_pengguna.argumen(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < teks.length(); INDEX++) {
            if (teks.charAt(INDEX) < '0' || teks.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + teks.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int handel_VALUE = ruang_pengguna.buat_jaringan(0);
        if (handel_VALUE < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int panjang_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (ruang_pengguna.kirim_data(handel_VALUE, 0x0a000202, port_VALUE, data, panjang_VALUE) != panjang_VALUE) return 4;
            if (ruang_pengguna.Data_Penerimaan(handel_VALUE, data, 300) != panjang_VALUE) return 5;
            for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        ruang_pengguna.Tutup_jaringan(handel_VALUE);
        ruang_pengguna.Tulis("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
