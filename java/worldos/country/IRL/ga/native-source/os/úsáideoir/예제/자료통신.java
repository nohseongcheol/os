// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int digit_VALUE(String Téacs) {
        if (Téacs == null || Téacs.length() == 0) return -1;
        int tomhas = 0;
        for (int INDEX = 0; INDEX < Téacs.length(); INDEX++) {
            int VALUE = Téacs.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || tomhas > 6553) return -1;
            tomhas = tomhas * 10 + VALUE;
            if (tomhas > 65535) return -1;
        }
        return tomhas;
    }
    static int ADDRESS(String Téacs) {
        if (Téacs == null) return 0;
        int VALUE = 0, tomhas = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Téacs.length(); INDEX++) {
            int 문자 = INDEX == Téacs.length() ? '.' : Téacs.charAt(INDEX);
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
    public static int Rith_2() {
        if (úsáideoir.인수개수() != 3) { úsáideoir.Scríobh("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADDRESS = ADDRESS(úsáideoir.Argóintí(0)), port_VALUE = digit_VALUE(úsáideoir.Argóintí(1));
        String Inneachar_VALUE = úsáideoir.Argóintí(2);
        if (ADDRESS == 0 || port_VALUE < 1 || Inneachar_VALUE.length() > 1024) { úsáideoir.Scríobh("Bad destination\n"); return 2; }
        int hanla_VALUE = úsáideoir.oscail_Líonra(0);
        if (hanla_VALUE < 0) { úsáideoir.Scríobh("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] sonraí = new int[1024];
        for (int INDEX = 0; INDEX < Inneachar_VALUE.length(); INDEX++) sonraí[INDEX] = Inneachar_VALUE.charAt(INDEX);
        if (úsáideoir.seol_sonraí(hanla_VALUE, ADDRESS, port_VALUE, sonraí, Inneachar_VALUE.length()) < 0) {
            úsáideoir.Scríobh("UDP SEND FAILED\n"); úsáideoir.dún_Líonra(hanla_VALUE); return 4;
        }
        úsáideoir.Scríobh("UDP SENT\n");
        int RECEIVED_fad = úsáideoir.자료받기(hanla_VALUE, sonraí, 1500);
        boolean 같음 = RECEIVED_fad == Inneachar_VALUE.length() && úsáideoir.보낸주소(hanla_VALUE) == ADDRESS && úsáideoir.보낸창구(hanla_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_fad; INDEX++) if (sonraí[INDEX] != Inneachar_VALUE.charAt(INDEX)) 같음 = false;
        úsáideoir.dún_Líonra(hanla_VALUE);
        if (RECEIVED_fad < 0) { úsáideoir.Scríobh("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        úsáideoir.Scríobh(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
