// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int cifra_VALUE(String Tekst) {
        if (Tekst == null || Tekst.length() == 0) return -1;
        int mjera = 0;
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            int VALUE = Tekst.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || mjera > 6553) return -1;
            mjera = mjera * 10 + VALUE;
            if (mjera > 65535) return -1;
        }
        return mjera;
    }
    static int adresa(String Tekst) {
        if (Tekst == null) return 0;
        int VALUE = 0, mjera = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Tekst.length(); INDEX++) {
            int 문자 = INDEX == Tekst.length() ? '.' : Tekst.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                mjera = (mjera << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? mjera : 0;
    }
    public static int Pokreni() {
        if (korisnik.인수개수() != 3) { korisnik.Piši("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adresa = adresa(korisnik.Argumenti(0)), port_VALUE = cifra_VALUE(korisnik.Argumenti(1));
        String Sadržaj_VALUE = korisnik.Argumenti(2);
        if (adresa == 0 || port_VALUE < 1 || Sadržaj_VALUE.length() > 1024) { korisnik.Piši("Bad destination\n"); return 2; }
        int hvatište_VALUE = korisnik.kreirati_Mreža(0);
        if (hvatište_VALUE < 0) { korisnik.Piši("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] podaci = new int[1024];
        for (int INDEX = 0; INDEX < Sadržaj_VALUE.length(); INDEX++) podaci[INDEX] = Sadržaj_VALUE.charAt(INDEX);
        if (korisnik.poslati_podaci(hvatište_VALUE, adresa, port_VALUE, podaci, Sadržaj_VALUE.length()) < 0) {
            korisnik.Piši("UDP SEND FAILED\n"); korisnik.zatvoriti_Mreža(hvatište_VALUE); return 4;
        }
        korisnik.Piši("UDP SENT\n");
        int RECEIVED_dužina = korisnik.자료받기(hvatište_VALUE, podaci, 1500);
        boolean 같음 = RECEIVED_dužina == Sadržaj_VALUE.length() && korisnik.보낸주소(hvatište_VALUE) == adresa && korisnik.보낸창구(hvatište_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < RECEIVED_dužina; INDEX++) if (podaci[INDEX] != Sadržaj_VALUE.charAt(INDEX)) 같음 = false;
        korisnik.zatvoriti_Mreža(hvatište_VALUE);
        if (RECEIVED_dužina < 0) { korisnik.Piši("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        korisnik.Piši(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
