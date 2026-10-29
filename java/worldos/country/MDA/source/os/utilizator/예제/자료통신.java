// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int cifră_VALUE(String SMS) {
        if (SMS == null || SMS.length() == 0) return -1;
        int KR = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            int VALUE = SMS.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || KR > 6553) return -1;
            KR = KR * 10 + VALUE;
            if (KR > 65535) return -1;
        }
        return KR;
    }
    static int adresa(String SMS) {
        if (SMS == null) return 0;
        int VALUE = 0, KR = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= SMS.length(); INDEX++) {
            int 문자 = INDEX == SMS.length() ? '.' : SMS.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                KR = (KR << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? KR : 0;
    }
    public static int Pornește() {
        if (utilizator.인수개수() != 3) { utilizator.Scriere("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adresa = adresa(utilizator.Argumente(0)), muta_VALUE = cifră_VALUE(utilizator.Argumente(1));
        String Conținut_VALUE = utilizator.Argumente(2);
        if (adresa == 0 || muta_VALUE < 1 || Conținut_VALUE.length() > 1024) { utilizator.Scriere("Bad destination\n"); return 2; }
        int handle_VALUE = utilizator.crea_rețea(0);
        if (handle_VALUE < 0) { utilizator.Scriere("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] date = new int[1024];
        for (int INDEX = 0; INDEX < Conținut_VALUE.length(); INDEX++) date[INDEX] = Conținut_VALUE.charAt(INDEX);
        if (utilizator.trimite_date(handle_VALUE, adresa, muta_VALUE, date, Conținut_VALUE.length()) < 0) {
            utilizator.Scriere("UDP SEND FAILED\n"); utilizator.închide_rețea(handle_VALUE); return 4;
        }
        utilizator.Scriere("UDP SENT\n");
        int RECEIVED_lungime = utilizator.primi_date(handle_VALUE, date, 1500);
        boolean 같음 = RECEIVED_lungime == Conținut_VALUE.length() && utilizator.보낸주소(handle_VALUE) == adresa && utilizator.보낸창구(handle_VALUE) == muta_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_lungime; INDEX++) if (date[INDEX] != Conținut_VALUE.charAt(INDEX)) 같음 = false;
        utilizator.închide_rețea(handle_VALUE);
        if (RECEIVED_lungime < 0) { utilizator.Scriere("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        utilizator.Scriere(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
