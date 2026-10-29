// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int siffer_VALUE(String Tekst) {
        if (Tekst == null || Tekst.length() == 0) return -1;
        int forretningsmål = 0;
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            int VALUE = Tekst.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || forretningsmål > 6553) return -1;
            forretningsmål = forretningsmål * 10 + VALUE;
            if (forretningsmål > 65535) return -1;
        }
        return forretningsmål;
    }
    static int ADDRESS(String Tekst) {
        if (Tekst == null) return 0;
        int VALUE = 0, forretningsmål = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Tekst.length(); INDEX++) {
            int 문자 = INDEX == Tekst.length() ? '.' : Tekst.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                forretningsmål = (forretningsmål << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? forretningsmål : 0;
    }
    public static int Køyr_2() {
        if (brukar.인수개수() != 3) { brukar.Skriv("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADDRESS = ADDRESS(brukar.Argument(0)), port_VALUE = siffer_VALUE(brukar.Argument(1));
        String Innhald_VALUE = brukar.Argument(2);
        if (ADDRESS == 0 || port_VALUE < 1 || Innhald_VALUE.length() > 1024) { brukar.Skriv("Bad destination\n"); return 2; }
        int handtak_VALUE = brukar.opne_Nettverk(0);
        if (handtak_VALUE < 0) { brukar.Skriv("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEX = 0; INDEX < Innhald_VALUE.length(); INDEX++) data[INDEX] = Innhald_VALUE.charAt(INDEX);
        if (brukar.sende_data(handtak_VALUE, ADDRESS, port_VALUE, data, Innhald_VALUE.length()) < 0) {
            brukar.Skriv("UDP SEND FAILED\n"); brukar.Lukk_Nettverk(handtak_VALUE); return 4;
        }
        brukar.Skriv("UDP SENT\n");
        int RECEIVED_lengd = brukar.자료받기(handtak_VALUE, data, 1500);
        boolean 같음 = RECEIVED_lengd == Innhald_VALUE.length() && brukar.보낸주소(handtak_VALUE) == ADDRESS && brukar.보낸창구(handtak_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_lengd; INDEX++) if (data[INDEX] != Innhald_VALUE.charAt(INDEX)) 같음 = false;
        brukar.Lukk_Nettverk(handtak_VALUE);
        if (RECEIVED_lengd < 0) { brukar.Skriv("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        brukar.Skriv(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
