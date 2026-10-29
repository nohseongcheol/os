// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int syfer_VALUE(String Teks) {
        if (Teks == null || Teks.length() == 0) return -1;
        int maatreël = 0;
        for (int INDEX = 0; INDEX < Teks.length(); INDEX++) {
            int VALUE = Teks.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || maatreël > 6553) return -1;
            maatreël = maatreël * 10 + VALUE;
            if (maatreël > 65535) return -1;
        }
        return maatreël;
    }
    static int adres(String Teks) {
        if (Teks == null) return 0;
        int VALUE = 0, maatreël = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Teks.length(); INDEX++) {
            int 문자 = INDEX == Teks.length() ? '.' : Teks.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                maatreël = (maatreël << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? maatreël : 0;
    }
    public static int Loop() {
        if (gebruiker.인수개수() != 3) { gebruiker.Skryf("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adres = adres(gebruiker.인수(0)), ombou_VALUE = syfer_VALUE(gebruiker.인수(1));
        String Inhoud_VALUE = gebruiker.인수(2);
        if (adres == 0 || ombou_VALUE < 1 || Inhoud_VALUE.length() > 1024) { gebruiker.Skryf("Bad destination\n"); return 2; }
        int handvatsel_VALUE = gebruiker.skep_Netwerk(0);
        if (handvatsel_VALUE < 0) { gebruiker.Skryf("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Inhoud_VALUE.length(); INDEX++) data[INDEX] = Inhoud_VALUE.charAt(INDEX);
        if (gebruiker.e_pos_data(handvatsel_VALUE, adres, ombou_VALUE, data, Inhoud_VALUE.length()) < 0) {
            gebruiker.Skryf("UDP SEND FAILED\n"); gebruiker.sluit_Netwerk(handvatsel_VALUE); return 4;
        }
        gebruiker.Skryf("UDP SENT\n");
        int RECEIVED_lengte = gebruiker.자료받기(handvatsel_VALUE, data, 1500);
        boolean 같음 = RECEIVED_lengte == Inhoud_VALUE.length() && gebruiker.보낸주소(handvatsel_VALUE) == adres && gebruiker.보낸창구(handvatsel_VALUE) == ombou_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_lengte; INDEX++) if (data[INDEX] != Inhoud_VALUE.charAt(INDEX)) 같음 = false;
        gebruiker.sluit_Netwerk(handvatsel_VALUE);
        if (RECEIVED_lengte < 0) { gebruiker.Skryf("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        gebruiker.Skryf(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
