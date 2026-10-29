// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int digit_VALUE(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int sukat = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int VALUE = SMS.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || sukat > 6553) return -1;
            sukat = sukat * 10 + VALUE;
            if (sukat > 65535) return -1;
        }
        return sukat;
    }
    static int email(String SMS) {
        if (SMS == null) return 0;
        int VALUE = 0, sukat = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= SMS.length(); INDEX++) {
            int 문자 = INDEX == SMS.length() ? '.' : SMS.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                sukat = (sukat << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? sukat : 0;
    }
    public static int run() {
        if (gumagamit.인수개수() != 3) { gumagamit.sumulat("Usage: run udp IP PORT TEXT\n"); return 2; }
        int email = email(gumagamit.인수(0)), port_VALUE = digit_VALUE(gumagamit.인수(1));
        String Nilalaman_VALUE = gumagamit.인수(2);
        if (email == 0 || port_VALUE < 1 || Nilalaman_VALUE.length() > 1024) { gumagamit.sumulat("Bad destination\n"); return 2; }
        int hawakán_VALUE = gumagamit.buksan_Network(0);
        if (hawakán_VALUE < 0) { gumagamit.sumulat("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Nilalaman_VALUE.length(); INDEX++) data[INDEX] = Nilalaman_VALUE.charAt(INDEX);
        if (gumagamit.i_email_data(hawakán_VALUE, email, port_VALUE, data, Nilalaman_VALUE.length()) < 0) {
            gumagamit.sumulat("UDP SEND FAILED\n"); gumagamit.isara_Network(hawakán_VALUE); return 4;
        }
        gumagamit.sumulat("UDP SENT\n");
        int RECEIVED_haba = gumagamit.자료받기(hawakán_VALUE, data, 1500);
        boolean 같음 = RECEIVED_haba == Nilalaman_VALUE.length() && gumagamit.보낸주소(hawakán_VALUE) == email && gumagamit.보낸창구(hawakán_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_haba; INDEX++) if (data[INDEX] != Nilalaman_VALUE.charAt(INDEX)) 같음 = false;
        gumagamit.isara_Network(hawakán_VALUE);
        if (RECEIVED_haba < 0) { gumagamit.sumulat("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        gumagamit.sumulat(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
