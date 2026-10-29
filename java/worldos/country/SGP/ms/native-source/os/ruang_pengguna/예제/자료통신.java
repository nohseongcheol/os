// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int digit_VALUE(String Teks) {
        if (Teks == null || Teks.length() == 0) return -1;
        int ukuran = 0;
        for (int INDEX = 0; INDEX < Teks.length(); INDEX++) {
            int VALUE = Teks.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || ukuran > 6553) return -1;
            ukuran = ukuran * 10 + VALUE;
            if (ukuran > 65535) return -1;
        }
        return ukuran;
    }
    static int e_mel(String Teks) {
        if (Teks == null) return 0;
        int VALUE = 0, ukuran = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Teks.length(); INDEX++) {
            int 문자 = INDEX == Teks.length() ? '.' : Teks.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                ukuran = (ukuran << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? ukuran : 0;
    }
    public static int Jalan() {
        if (ruang_pengguna.인수개수() != 3) { ruang_pengguna.Tulis("Usage: run udp IP PORT TEXT\n"); return 2; }
        int e_mel = e_mel(ruang_pengguna.인수(0)), port_VALUE = digit_VALUE(ruang_pengguna.인수(1));
        String Kandungan_VALUE = ruang_pengguna.인수(2);
        if (e_mel == 0 || port_VALUE < 1 || Kandungan_VALUE.length() > 1024) { ruang_pengguna.Tulis("Bad destination\n"); return 2; }
        int pemegang_VALUE = ruang_pengguna.buka_rangkaian(0);
        if (pemegang_VALUE < 0) { ruang_pengguna.Tulis("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Kandungan_VALUE.length(); INDEX++) data[INDEX] = Kandungan_VALUE.charAt(INDEX);
        if (ruang_pengguna.e_mel_data_5b5410b2(pemegang_VALUE, e_mel, port_VALUE, data, Kandungan_VALUE.length()) < 0) {
            ruang_pengguna.Tulis("UDP SEND FAILED\n"); ruang_pengguna.Tutup_rangkaian(pemegang_VALUE); return 4;
        }
        ruang_pengguna.Tulis("UDP SENT\n");
        int RECEIVED_kepanjangan = ruang_pengguna.자료받기(pemegang_VALUE, data, 1500);
        boolean 같음 = RECEIVED_kepanjangan == Kandungan_VALUE.length() && ruang_pengguna.보낸주소(pemegang_VALUE) == e_mel && ruang_pengguna.보낸창구(pemegang_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_kepanjangan; INDEX++) if (data[INDEX] != Kandungan_VALUE.charAt(INDEX)) 같음 = false;
        ruang_pengguna.Tutup_rangkaian(pemegang_VALUE);
        if (RECEIVED_kepanjangan < 0) { ruang_pengguna.Tulis("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        ruang_pengguna.Tulis(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
