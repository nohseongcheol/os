// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Saiz/홀수 kepanjangan_VALUE 데이터그램으로 sebenar_data RTL8139 수신 Loop_VALUE 순환을 시험한다. */
public final class rangkaian_Loop {
    public static int Jalan() {
        if (ruang_pengguna.인수개수() != 1) { ruang_pengguna.Tulis("Usage: run stress PORT\n"); return 2; }
        String Teks = ruang_pengguna.인수(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < Teks.length(); INDEX++) {
            if (Teks.charAt(INDEX) < '0' || Teks.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + Teks.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int pemegang_VALUE = ruang_pengguna.buka_rangkaian(0);
        if (pemegang_VALUE < 0) return 3;
        int[] data = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int kepanjangan_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) data[INDEX] = (INDEX + 회차) & 255;
            if (ruang_pengguna.e_mel_data_5b5410b2(pemegang_VALUE, 0x0a000202, port_VALUE, data, kepanjangan_VALUE) != kepanjangan_VALUE) return 4;
            if (ruang_pengguna.자료받기(pemegang_VALUE, data, 300) != kepanjangan_VALUE) return 5;
            for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) if (data[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        ruang_pengguna.Tutup_rangkaian(pemegang_VALUE);
        ruang_pengguna.Tulis("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
