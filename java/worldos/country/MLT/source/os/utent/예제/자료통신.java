// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int ċifra_VALUE(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int miżura = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int VALUE = SMS.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || miżura > 6553) return -1;
            miżura = miżura * 10 + VALUE;
            if (miżura > 65535) return -1;
        }
        return miżura;
    }
    static int ADDRESS(String SMS) {
        if (SMS == null) return 0;
        int VALUE = 0, miżura = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= SMS.length(); INDEX++) {
            int 문자 = INDEX == SMS.length() ? '.' : SMS.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                miżura = (miżura << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? miżura : 0;
    }
    public static int serje() {
        if (utent.인수개수() != 3) { utent.kiteb("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADDRESS = ADDRESS(utent.인수(0)), port_VALUE = ċifra_VALUE(utent.인수(1));
        String Kontenut_VALUE = utent.인수(2);
        if (ADDRESS == 0 || port_VALUE < 1 || Kontenut_VALUE.length() > 1024) { utent.kiteb("Bad destination\n"); return 2; }
        int handle_VALUE = utent.fetaħ_netwerk(0);
        if (handle_VALUE < 0) { utent.kiteb("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Kontenut_VALUE.length(); INDEX++) data[INDEX] = Kontenut_VALUE.charAt(INDEX);
        if (utent.bagħat_data(handle_VALUE, ADDRESS, port_VALUE, data, Kontenut_VALUE.length()) < 0) {
            utent.kiteb("UDP SEND FAILED\n"); utent.agħlaq_netwerk(handle_VALUE); return 4;
        }
        utent.kiteb("UDP SENT\n");
        int RECEIVED_tul = utent.자료받기(handle_VALUE, data, 1500);
        boolean 같음 = RECEIVED_tul == Kontenut_VALUE.length() && utent.보낸주소(handle_VALUE) == ADDRESS && utent.보낸창구(handle_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_tul; INDEX++) if (data[INDEX] != Kontenut_VALUE.charAt(INDEX)) 같음 = false;
        utent.agħlaq_netwerk(handle_VALUE);
        if (RECEIVED_tul < 0) { utent.kiteb("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        utent.kiteb(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
