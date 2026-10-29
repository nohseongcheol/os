// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int mati_uara(String Ngā_kupu) {
        if (Ngā_kupu == null || Ngā_kupu.length() == 0) return -1;
        int mēhua = 0;
        for (int INDEX = 0; INDEX < Ngā_kupu.length(); INDEX++) {
            int uara = Ngā_kupu.charAt(INDEX) - '0';
            if (uara < 0 || uara > 9 || mēhua > 6553) return -1;
            mēhua = mēhua * 10 + uara;
            if (mēhua > 65535) return -1;
        }
        return mēhua;
    }
    static int ADDRESS(String Ngā_kupu) {
        if (Ngā_kupu == null) return 0;
        int uara = 0, mēhua = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Ngā_kupu.length(); INDEX++) {
            int 문자 = INDEX == Ngā_kupu.length() ? '.' : Ngā_kupu.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                mēhua = (mēhua << 8) | uara; 부분++; uara = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                uara = uara * 10 + 문자 - '0';
                if (++자릿수 > 3 || uara > 255) return 0;
            }
        }
        return 부분 == 4 ? mēhua : 0;
    }
    public static int whakahaere() {
        if (kaiwhakamahi.인수개수() != 3) { kaiwhakamahi.Tuhia("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADDRESS = ADDRESS(kaiwhakamahi.인수(0)), kawe_uara = mati_uara(kaiwhakamahi.인수(1));
        String Ihirangi_uara = kaiwhakamahi.인수(2);
        if (ADDRESS == 0 || kawe_uara < 1 || Ihirangi_uara.length() > 1024) { kaiwhakamahi.Tuhia("Bad destination\n"); return 2; }
        int raweke_uara = kaiwhakamahi.tiwhikete_whatunga(0);
        if (raweke_uara < 0) { kaiwhakamahi.Tuhia("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] raraunga = new int[1024];
        for (int INDEX = 0; INDEX < Ihirangi_uara.length(); INDEX++) raraunga[INDEX] = Ihirangi_uara.charAt(INDEX);
        if (kaiwhakamahi.tuku_raraunga(raweke_uara, ADDRESS, kawe_uara, raraunga, Ihirangi_uara.length()) < 0) {
            kaiwhakamahi.Tuhia("UDP SEND FAILED\n"); kaiwhakamahi.kati_whatunga(raweke_uara); return 4;
        }
        kaiwhakamahi.Tuhia("UDP SENT\n");
        int RECEIVED_roa = kaiwhakamahi.자료받기(raweke_uara, raraunga, 1500);
        boolean 같음 = RECEIVED_roa == Ihirangi_uara.length() && kaiwhakamahi.보낸주소(raweke_uara) == ADDRESS && kaiwhakamahi.보낸창구(raweke_uara) == kawe_uara;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_roa; INDEX++) if (raraunga[INDEX] != Ihirangi_uara.charAt(INDEX)) 같음 = false;
        kaiwhakamahi.kati_whatunga(raweke_uara);
        if (RECEIVED_roa < 0) { kaiwhakamahi.Tuhia("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        kaiwhakamahi.Tuhia(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
