// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int raqam_VALUE(String Matn) {
        if (Matn == null || Matn.length() == 0) return -1;
        int o_lchov = 0;
        for (int INDEX = 0; INDEX < Matn.length(); INDEX++) {
            int VALUE = Matn.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || o_lchov > 6553) return -1;
            o_lchov = o_lchov * 10 + VALUE;
            if (o_lchov > 65535) return -1;
        }
        return o_lchov;
    }
    static int manzil(String Matn) {
        if (Matn == null) return 0;
        int VALUE = 0, o_lchov = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Matn.length(); INDEX++) {
            int 문자 = INDEX == Matn.length() ? '.' : Matn.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                o_lchov = (o_lchov << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? o_lchov : 0;
    }
    public static int Bajarish() {
        if (foydalanuvchi.인수개수() != 3) { foydalanuvchi.Yozish("Usage: run udp IP PORT TEXT\n"); return 2; }
        int manzil = manzil(foydalanuvchi.인수(0)), port_VALUE = raqam_VALUE(foydalanuvchi.인수(1));
        String tarkib_VALUE = foydalanuvchi.인수(2);
        if (manzil == 0 || port_VALUE < 1 || tarkib_VALUE.length() > 1024) { foydalanuvchi.Yozish("Bad destination\n"); return 2; }
        int deskriptor_VALUE = foydalanuvchi.ochmoq_Tarmoq(0);
        if (deskriptor_VALUE < 0) { foydalanuvchi.Yozish("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] ma_lumotlar = new int[1024];
        for (int INDEX = 0; INDEX < tarkib_VALUE.length(); INDEX++) ma_lumotlar[INDEX] = tarkib_VALUE.charAt(INDEX);
        if (foydalanuvchi.yuborish_ma_lumotlar(deskriptor_VALUE, manzil, port_VALUE, ma_lumotlar, tarkib_VALUE.length()) < 0) {
            foydalanuvchi.Yozish("UDP SEND FAILED\n"); foydalanuvchi.yopmoq_Tarmoq(deskriptor_VALUE); return 4;
        }
        foydalanuvchi.Yozish("UDP SENT\n");
        int RECEIVED_uzunlik = foydalanuvchi.자료받기(deskriptor_VALUE, ma_lumotlar, 1500);
        boolean 같음 = RECEIVED_uzunlik == tarkib_VALUE.length() && foydalanuvchi.보낸주소(deskriptor_VALUE) == manzil && foydalanuvchi.보낸창구(deskriptor_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_uzunlik; INDEX++) if (ma_lumotlar[INDEX] != tarkib_VALUE.charAt(INDEX)) 같음 = false;
        foydalanuvchi.yopmoq_Tarmoq(deskriptor_VALUE);
        if (RECEIVED_uzunlik < 0) { foydalanuvchi.Yozish("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        foydalanuvchi.Yozish(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
