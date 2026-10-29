// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int znamenka_VALUE(String Tekst) {
        if (Tekst == null || Tekst.length() == 0) return -1;
        int REZULTAT = 0;
        for (int INDEX = 0; INDEX < Tekst.length(); INDEX++) {
            int VALUE = Tekst.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || REZULTAT > 6553) return -1;
            REZULTAT = REZULTAT * 10 + VALUE;
            if (REZULTAT > 65535) return -1;
        }
        return REZULTAT;
    }
    static int adresa(String Tekst) {
        if (Tekst == null) return 0;
        int VALUE = 0, REZULTAT = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Tekst.length(); INDEX++) {
            int 문자 = INDEX == Tekst.length() ? '.' : Tekst.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                REZULTAT = (REZULTAT << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? REZULTAT : 0;
    }
    public static int Pokreni() {
        if (korisnik.인수개수() != 3) { korisnik.Zapisuj("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adresa = adresa(korisnik.Argumenti(0)), prebaciti_VALUE = znamenka_VALUE(korisnik.Argumenti(1));
        String Sadržaj_VALUE = korisnik.Argumenti(2);
        if (adresa == 0 || prebaciti_VALUE < 1 || Sadržaj_VALUE.length() > 1024) { korisnik.Zapisuj("Bad destination\n"); return 2; }
        int ustroj_VALUE = korisnik.otvoreno_mreža(0);
        if (ustroj_VALUE < 0) { korisnik.Zapisuj("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] podaci = new int[1024];
        for (int INDEX = 0; INDEX < Sadržaj_VALUE.length(); INDEX++) podaci[INDEX] = Sadržaj_VALUE.charAt(INDEX);
        if (korisnik.slati_podaci(ustroj_VALUE, adresa, prebaciti_VALUE, podaci, Sadržaj_VALUE.length()) < 0) {
            korisnik.Zapisuj("UDP SEND FAILED\n"); korisnik.Zatvori_mreža(ustroj_VALUE); return 4;
        }
        korisnik.Zapisuj("UDP SENT\n");
        int 받은길이 = korisnik.primiti_podaci(ustroj_VALUE, podaci, 1500);
        boolean 같음 = 받은길이 == Sadržaj_VALUE.length() && korisnik.보낸주소(ustroj_VALUE) == adresa && korisnik.보낸창구(ustroj_VALUE) == prebaciti_VALUE;
        if (같음) for (int INDEX = 0; INDEX < 받은길이; INDEX++) if (podaci[INDEX] != Sadržaj_VALUE.charAt(INDEX)) 같음 = false;
        korisnik.Zatvori_mreža(ustroj_VALUE);
        if (받은길이 < 0) { korisnik.Zapisuj("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        korisnik.Zapisuj(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
