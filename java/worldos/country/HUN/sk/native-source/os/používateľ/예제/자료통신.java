// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int číslica_VALUE(String Spracovanie_textu) {
        if (Spracovanie_textu == null || Spracovanie_textu.length() == 0) return -1;
        int KR = 0;
        for (int INDEX = 0; INDEX < Spracovanie_textu.length(); INDEX++) {
            int VALUE = Spracovanie_textu.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || KR > 6553) return -1;
            KR = KR * 10 + VALUE;
            if (KR > 65535) return -1;
        }
        return KR;
    }
    static int adresa(String Spracovanie_textu) {
        if (Spracovanie_textu == null) return 0;
        int VALUE = 0, KR = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Spracovanie_textu.length(); INDEX++) {
            int 문자 = INDEX == Spracovanie_textu.length() ? '.' : Spracovanie_textu.charAt(INDEX);
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
    public static int Spustiť_2() {
        if (používateľ.인수개수() != 3) { používateľ.Zápis("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adresa = adresa(používateľ.Argumenty(0)), port_VALUE = číslica_VALUE(používateľ.Argumenty(1));
        String obsah_VALUE = používateľ.Argumenty(2);
        if (adresa == 0 || port_VALUE < 1 || obsah_VALUE.length() > 1024) { používateľ.Zápis("Bad destination\n"); return 2; }
        int rukoväť_VALUE = používateľ.otvoriť_sieť(0);
        if (rukoväť_VALUE < 0) { používateľ.Zápis("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] údaje = new int[1024];
        for (int INDEX = 0; INDEX < obsah_VALUE.length(); INDEX++) údaje[INDEX] = obsah_VALUE.charAt(INDEX);
        if (používateľ.odoslať_údaje(rukoväť_VALUE, adresa, port_VALUE, údaje, obsah_VALUE.length()) < 0) {
            používateľ.Zápis("UDP SEND FAILED\n"); používateľ.Zavrieť_sieť(rukoväť_VALUE); return 4;
        }
        používateľ.Zápis("UDP SENT\n");
        int RECEIVED_dĺžka = používateľ.dostať_údaje(rukoväť_VALUE, údaje, 1500);
        boolean 같음 = RECEIVED_dĺžka == obsah_VALUE.length() && používateľ.보낸주소(rukoväť_VALUE) == adresa && používateľ.보낸창구(rukoväť_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_dĺžka; INDEX++) if (údaje[INDEX] != obsah_VALUE.charAt(INDEX)) 같음 = false;
        používateľ.Zavrieť_sieť(rukoväť_VALUE);
        if (RECEIVED_dĺžka < 0) { používateľ.Zápis("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        používateľ.Zápis(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
