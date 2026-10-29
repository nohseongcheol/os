// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int number_VALUE(String Tekst) {
        if (Tekst == null || Tekst.length() == 0) return -1;
        int TULEMUS = 0;
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            int VALUE = Tekst.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || TULEMUS > 6553) return -1;
            TULEMUS = TULEMUS * 10 + VALUE;
            if (TULEMUS > 65535) return -1;
        }
        return TULEMUS;
    }
    static int ADDRESS(String Tekst) {
        if (Tekst == null) return 0;
        int VALUE = 0, TULEMUS = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Tekst.length(); INDEX++) {
            int 문자 = INDEX == Tekst.length() ? '.' : Tekst.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                TULEMUS = (TULEMUS << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? TULEMUS : 0;
    }
    public static int Käivita_2() {
        if (kasutaja.인수개수() != 3) { kasutaja.Kirjutamine("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADDRESS = ADDRESS(kasutaja.Argumendid(0)), port_VALUE = number_VALUE(kasutaja.Argumendid(1));
        String Sisu_VALUE = kasutaja.Argumendid(2);
        if (ADDRESS == 0 || port_VALUE < 1 || Sisu_VALUE.length() > 1024) { kasutaja.Kirjutamine("Bad destination\n"); return 2; }
        int pide_VALUE = kasutaja.avama_võrk(0);
        if (pide_VALUE < 0) { kasutaja.Kirjutamine("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] andmed = new int[1024];
        for (int INDEX = 0; INDEX < Sisu_VALUE.length(); INDEX++) andmed[INDEX] = Sisu_VALUE.charAt(INDEX);
        if (kasutaja.saatma_andmed(pide_VALUE, ADDRESS, port_VALUE, andmed, Sisu_VALUE.length()) < 0) {
            kasutaja.Kirjutamine("UDP SEND FAILED\n"); kasutaja.Sule_võrk(pide_VALUE); return 4;
        }
        kasutaja.Kirjutamine("UDP SENT\n");
        int 받은길이 = kasutaja.saama_andmed(pide_VALUE, andmed, 1500);
        boolean 같음 = 받은길이 == Sisu_VALUE.length() && kasutaja.보낸주소(pide_VALUE) == ADDRESS && kasutaja.보낸창구(pide_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < 받은길이; INDEX++) if (andmed[INDEX] != Sisu_VALUE.charAt(INDEX)) 같음 = false;
        kasutaja.Sule_võrk(pide_VALUE);
        if (받은길이 < 0) { kasutaja.Kirjutamine("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        kasutaja.Kirjutamine(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
