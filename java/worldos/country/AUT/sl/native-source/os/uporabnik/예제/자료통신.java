// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int številka_VALUE(String Besedilo) {
        if (Besedilo == null || Besedilo.length() == 0) return -1;
        int REZULTAT = 0;
        for (int INDEX = 0; INDEX < Besedilo.length(); INDEX++) {
            int VALUE = Besedilo.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || REZULTAT > 6553) return -1;
            REZULTAT = REZULTAT * 10 + VALUE;
            if (REZULTAT > 65535) return -1;
        }
        return REZULTAT;
    }
    static int naslov(String Besedilo) {
        if (Besedilo == null) return 0;
        int VALUE = 0, REZULTAT = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Besedilo.length(); INDEX++) {
            int 문자 = INDEX == Besedilo.length() ? '.' : Besedilo.charAt(INDEX);
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
    public static int Zaženi() {
        if (uporabnik.인수개수() != 3) { uporabnik.Pisanje("Usage: run udp IP PORT TEXT\n"); return 2; }
        int naslov = naslov(uporabnik.Argumenti(0)), vrata_VALUE = številka_VALUE(uporabnik.Argumenti(1));
        String vsebina_VALUE = uporabnik.Argumenti(2);
        if (naslov == 0 || vrata_VALUE < 1 || vsebina_VALUE.length() > 1024) { uporabnik.Pisanje("Bad destination\n"); return 2; }
        int ročica_VALUE = uporabnik.odprto_mreža(0);
        if (ročica_VALUE < 0) { uporabnik.Pisanje("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] podatki = new int[1024];
        for (int INDEX = 0; INDEX < vsebina_VALUE.length(); INDEX++) podatki[INDEX] = vsebina_VALUE.charAt(INDEX);
        if (uporabnik.poslati_podatki(ročica_VALUE, naslov, vrata_VALUE, podatki, vsebina_VALUE.length()) < 0) {
            uporabnik.Pisanje("UDP SEND FAILED\n"); uporabnik.Zapri_mreža(ročica_VALUE); return 4;
        }
        uporabnik.Pisanje("UDP SENT\n");
        int 받은길이 = uporabnik.sprejeti_sprejemati_prejeti_prejemati_podatki(ročica_VALUE, podatki, 1500);
        boolean 같음 = 받은길이 == vsebina_VALUE.length() && uporabnik.보낸주소(ročica_VALUE) == naslov && uporabnik.보낸창구(ročica_VALUE) == vrata_VALUE;
        if (같음) for (int INDEX = 0; INDEX < 받은길이; INDEX++) if (podatki[INDEX] != vsebina_VALUE.charAt(INDEX)) 같음 = false;
        uporabnik.Zapri_mreža(ročica_VALUE);
        if (받은길이 < 0) { uporabnik.Pisanje("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        uporabnik.Pisanje(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
