// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int figear_VALUE(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int tomhas = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int VALUE = SMS.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || tomhas > 6553) return -1;
            tomhas = tomhas * 10 + VALUE;
            if (tomhas > 65535) return -1;
        }
        return tomhas;
    }
    static int ADDRESS(String SMS) {
        if (SMS == null) return 0;
        int VALUE = 0, tomhas = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= SMS.length(); INDEX++) {
            int 문자 = INDEX == SMS.length() ? '.' : SMS.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                tomhas = (tomhas << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? tomhas : 0;
    }
    public static int ruith() {
        if (cleachdaiche.인수개수() != 3) { cleachdaiche.sgrìobh("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADDRESS = ADDRESS(cleachdaiche.인수(0)), port_VALUE = figear_VALUE(cleachdaiche.인수(1));
        String susbaint_VALUE = cleachdaiche.인수(2);
        if (ADDRESS == 0 || port_VALUE < 1 || susbaint_VALUE.length() > 1024) { cleachdaiche.sgrìobh("Bad destination\n"); return 2; }
        int làmhrachan_VALUE = cleachdaiche.fosgail_lìonra(0);
        if (làmhrachan_VALUE < 0) { cleachdaiche.sgrìobh("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] dàta = new int[1024];
        for (int INDEX = 0; INDEX < susbaint_VALUE.length(); INDEX++) dàta[INDEX] = susbaint_VALUE.charAt(INDEX);
        if (cleachdaiche.cuir_dàta(làmhrachan_VALUE, ADDRESS, port_VALUE, dàta, susbaint_VALUE.length()) < 0) {
            cleachdaiche.sgrìobh("UDP SEND FAILED\n"); cleachdaiche.dùin_lìonra(làmhrachan_VALUE); return 4;
        }
        cleachdaiche.sgrìobh("UDP SENT\n");
        int RECEIVED_faid = cleachdaiche.자료받기(làmhrachan_VALUE, dàta, 1500);
        boolean 같음 = RECEIVED_faid == susbaint_VALUE.length() && cleachdaiche.보낸주소(làmhrachan_VALUE) == ADDRESS && cleachdaiche.보낸창구(làmhrachan_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_faid; INDEX++) if (dàta[INDEX] != susbaint_VALUE.charAt(INDEX)) 같음 = false;
        cleachdaiche.dùin_lìonra(làmhrachan_VALUE);
        if (RECEIVED_faid < 0) { cleachdaiche.sgrìobh("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        cleachdaiche.sgrìobh(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
