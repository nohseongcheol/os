// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int cifra_VALUE(String SMS) {
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
    public static int koristiti() {
        if (korisnik.인수개수() != 3) { korisnik.쓰기("Usage: run udp IP PORT TEXT\n"); return 2; }
        int adresa = adresa(korisnik.인수(0)), port_VALUE = cifra_VALUE(korisnik.인수(1));
        String Sadržaj_VALUE = korisnik.인수(2);
        if (adresa == 0 || port_VALUE < 1 || Sadržaj_VALUE.length() > 1024) { korisnik.쓰기("Bad destination\n"); return 2; }
        int pokazivač_VALUE = korisnik.otvoren_Mreža(0);
        if (pokazivač_VALUE < 0) { korisnik.쓰기("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] podaci = new int[1024];
        for (int INDEX = 0; INDEX < Sadržaj_VALUE.length(); INDEX++) podaci[INDEX] = Sadržaj_VALUE.charAt(INDEX);
        if (korisnik.poslati_podaci(pokazivač_VALUE, adresa, port_VALUE, podaci, Sadržaj_VALUE.length()) < 0) {
            korisnik.쓰기("UDP SEND FAILED\n"); korisnik.Zatvori_Mreža(pokazivač_VALUE); return 4;
        }
        korisnik.쓰기("UDP SENT\n");
        int 받은길이 = korisnik.primiti_podaci(pokazivač_VALUE, podaci, 1500);
        boolean 같음 = 받은길이 == Sadržaj_VALUE.length() && korisnik.보낸주소(pokazivač_VALUE) == adresa && korisnik.보낸창구(pokazivač_VALUE) == port_VALUE;
        if (같음) for (int INDEX = 0; INDEX < 받은길이; INDEX++) if (podaci[INDEX] != Sadržaj_VALUE.charAt(INDEX)) 같음 = false;
        korisnik.Zatvori_Mreža(pokazivač_VALUE);
        if (받은길이 < 0) { korisnik.쓰기("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        korisnik.쓰기(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
