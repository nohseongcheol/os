// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int cipars_VALUE(String Teksts) {
        if (Teksts == null || Teksts.length() == 0) return -1;
        int mērs = 0;
        for (int INDEX = 0; INDEX < Teksts.length(); INDEX++) {
            int VALUE = Teksts.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || mērs > 6553) return -1;
            mērs = mērs * 10 + VALUE;
            if (mērs > 65535) return -1;
        }
        return mērs;
    }
    static int adrese(String Teksts) {
        if (Teksts == null) return 0;
        int VALUE = 0, mērs = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Teksts.length(); INDEX++) {
            int 문자 = INDEX == Teksts.length() ? '.' : Teksts.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                mērs = (mērs << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? mērs : 0;
    }
    public static int Palaist() {
        if (lietotājs.인수개수() != 3) { lietotājs.Rakstīt("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adrese = adrese(lietotājs.Parametri(0)), ports_VALUE = cipars_VALUE(lietotājs.Parametri(1));
        String Saturs_VALUE = lietotājs.Parametri(2);
        if (adrese == 0 || ports_VALUE < 1 || Saturs_VALUE.length() > 1024) { lietotājs.Rakstīt("Bad destination\n"); return 2; }
        int turis_VALUE = lietotājs.atvērt_tīkls(0);
        if (turis_VALUE < 0) { lietotājs.Rakstīt("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] dati = new int[1024];
        for (int INDEX = 0; INDEX < Saturs_VALUE.length(); INDEX++) dati[INDEX] = Saturs_VALUE.charAt(INDEX);
        if (lietotājs.sūtīt_dati(turis_VALUE, adrese, ports_VALUE, dati, Saturs_VALUE.length()) < 0) {
            lietotājs.Rakstīt("UDP SEND FAILED\n"); lietotājs.Aizvērt_tīkls(turis_VALUE); return 4;
        }
        lietotājs.Rakstīt("UDP SENT\n");
        int 받은길이 = lietotājs.saņemt_dati(turis_VALUE, dati, 1500);
        boolean 같음 = 받은길이 == Saturs_VALUE.length() && lietotājs.보낸주소(turis_VALUE) == adrese && lietotājs.보낸창구(turis_VALUE) == ports_VALUE;
        if (같음) for (int INDEX = 0; INDEX < 받은길이; INDEX++) if (dati[INDEX] != Saturs_VALUE.charAt(INDEX)) 같음 = false;
        lietotājs.Aizvērt_tīkls(turis_VALUE);
        if (받은길이 < 0) { lietotājs.Rakstīt("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        lietotājs.Rakstīt(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
