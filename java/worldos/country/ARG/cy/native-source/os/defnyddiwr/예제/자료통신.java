// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int digid_VALUE(String Testun) {
        if (Testun == null || Testun.length() == 0) return -1;
        int mesur = 0;
        for (int INDEX = 0; INDEX < Testun.length(); INDEX++) {
            int VALUE = Testun.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || mesur > 6553) return -1;
            mesur = mesur * 10 + VALUE;
            if (mesur > 65535) return -1;
        }
        return mesur;
    }
    static int ADDRESS(String Testun) {
        if (Testun == null) return 0;
        int VALUE = 0, mesur = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Testun.length(); INDEX++) {
            int 문자 = INDEX == Testun.length() ? '.' : Testun.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                mesur = (mesur << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? mesur : 0;
    }
    public static int Gweithredu_2() {
        if (defnyddiwr.인수개수() != 3) { defnyddiwr.Ysgrifennu("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADDRESS = ADDRESS(defnyddiwr.인수(0)), porth_VALUE = digid_VALUE(defnyddiwr.인수(1));
        String Cynnwys_VALUE = defnyddiwr.인수(2);
        if (ADDRESS == 0 || porth_VALUE < 1 || Cynnwys_VALUE.length() > 1024) { defnyddiwr.Ysgrifennu("Bad destination\n"); return 2; }
        int dolen_VALUE = defnyddiwr.agor_Rhwydwaith(0);
        if (dolen_VALUE < 0) { defnyddiwr.Ysgrifennu("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Cynnwys_VALUE.length(); INDEX++) data[INDEX] = Cynnwys_VALUE.charAt(INDEX);
        if (defnyddiwr.anfon_data(dolen_VALUE, ADDRESS, porth_VALUE, data, Cynnwys_VALUE.length()) < 0) {
            defnyddiwr.Ysgrifennu("UDP SEND FAILED\n"); defnyddiwr.cau_Rhwydwaith(dolen_VALUE); return 4;
        }
        defnyddiwr.Ysgrifennu("UDP SENT\n");
        int RECEIVED_hyd = defnyddiwr.자료받기(dolen_VALUE, data, 1500);
        boolean 같음 = RECEIVED_hyd == Cynnwys_VALUE.length() && defnyddiwr.보낸주소(dolen_VALUE) == ADDRESS && defnyddiwr.보낸창구(dolen_VALUE) == porth_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_hyd; INDEX++) if (data[INDEX] != Cynnwys_VALUE.charAt(INDEX)) 같음 = false;
        defnyddiwr.cau_Rhwydwaith(dolen_VALUE);
        if (RECEIVED_hyd < 0) { defnyddiwr.Ysgrifennu("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        defnyddiwr.Ysgrifennu(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
