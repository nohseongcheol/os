// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class data_komunikasi {
    static int angka_VALUE(String teks) {
        if (teks == null || teks.length() == 0) return -1;
        int hasil = 0;
        for (int INDEX = 0; INDEX < teks.length(); INDEX++) {
            int VALUE = teks.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || hasil > 6553) return -1;
            hasil = hasil * 10 + VALUE;
            if (hasil > 65535) return -1;
        }
        return hasil;
    }
    static int surel(String teks) {
        if (teks == null) return 0;
        int VALUE = 0, hasil = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= teks.length(); INDEX++) {
            int 문자 = INDEX == teks.length() ? '.' : teks.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                hasil = (hasil << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? hasil : 0;
    }
    public static int jalankan() {
        if (ruang_pengguna.인수개수() != 3) { ruang_pengguna.Tulis("Usage: run udp IP PORT TEXT\n"); return 2; }
        int surel = surel(ruang_pengguna.argumen(0)), port_VALUE = angka_VALUE(ruang_pengguna.argumen(1));
        String Isi_VALUE = ruang_pengguna.argumen(2);
        if (surel == 0 || port_VALUE < 1 || Isi_VALUE.length() > 1024) { ruang_pengguna.Tulis("Bad destination\n"); return 2; }
        int handel_VALUE = ruang_pengguna.buat_jaringan(0);
        if (handel_VALUE < 0) { ruang_pengguna.Tulis("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Isi_VALUE.length(); INDEX++) data[INDEX] = Isi_VALUE.charAt(INDEX);
        if (ruang_pengguna.kirim_data(handel_VALUE, surel, port_VALUE, data, Isi_VALUE.length()) < 0) {
            ruang_pengguna.Tulis("UDP SEND FAILED\n"); ruang_pengguna.Tutup_jaringan(handel_VALUE); return 4;
        }
        ruang_pengguna.Tulis("UDP SENT\n");
        int RECEIVED_panjang = ruang_pengguna.Data_Penerimaan(handel_VALUE, data, 1500);
        boolean 같음 = RECEIVED_panjang == Isi_VALUE.length() && ruang_pengguna.보낸주소(handel_VALUE) == surel && ruang_pengguna.보낸창구(handel_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_panjang; INDEX++) if (data[INDEX] != Isi_VALUE.charAt(INDEX)) 같음 = false;
        ruang_pengguna.Tutup_jaringan(handel_VALUE);
        if (RECEIVED_panjang < 0) { ruang_pengguna.Tulis("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        ruang_pengguna.Tulis(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
