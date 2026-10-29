// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int skaitmuo_VALUE(String Tekstas) {
        if (Tekstas == null || Tekstas.length() == 0) return -1;
        int REZULTATAS = 0;
        for (int INDEX = 0; INDEX < Tekstas.length(); INDEX++) {
            int VALUE = Tekstas.charAt(INDEX) - '0';
            if (VALUE < 0 || VALUE > 9 || REZULTATAS > 6553) return -1;
            REZULTATAS = REZULTATAS * 10 + VALUE;
            if (REZULTATAS > 65535) return -1;
        }
        return REZULTATAS;
    }
    static int ADDRESS(String Tekstas) {
        if (Tekstas == null) return 0;
        int VALUE = 0, REZULTATAS = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= Tekstas.length(); INDEX++) {
            int 문자 = INDEX == Tekstas.length() ? '.' : Tekstas.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                REZULTATAS = (REZULTATAS << 8) | VALUE; 부분++; VALUE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VALUE = VALUE * 10 + 문자 - '0';
                if (++자릿수 > 3 || VALUE > 255) return 0;
            }
        }
        return 부분 == 4 ? REZULTATAS : 0;
    }
    public static int Paleisti() {
        if (naudotojas.인수개수() != 3) { naudotojas.Rašymas("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADDRESS = ADDRESS(naudotojas.Argumentai(0)), jungtis_VALUE = skaitmuo_VALUE(naudotojas.Argumentai(1));
        String Turinys_VALUE = naudotojas.Argumentai(2);
        if (ADDRESS == 0 || jungtis_VALUE < 1 || Turinys_VALUE.length() > 1024) { naudotojas.Rašymas("Bad destination\n"); return 2; }
        int rodyklė_VALUE = naudotojas.kurti_tinklas(0);
        if (rodyklė_VALUE < 0) { naudotojas.Rašymas("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] duomenys = new int[1024];
        for (int INDEX = 0; INDEX < Turinys_VALUE.length(); INDEX++) duomenys[INDEX] = Turinys_VALUE.charAt(INDEX);
        if (naudotojas.siųsti_duomenys(rodyklė_VALUE, ADDRESS, jungtis_VALUE, duomenys, Turinys_VALUE.length()) < 0) {
            naudotojas.Rašymas("UDP SEND FAILED\n"); naudotojas.Uždaryti_tinklas(rodyklė_VALUE); return 4;
        }
        naudotojas.Rašymas("UDP SENT\n");
        int 받은길이 = naudotojas.gauti_duomenys(rodyklė_VALUE, duomenys, 1500);
        boolean 같음 = 받은길이 == Turinys_VALUE.length() && naudotojas.보낸주소(rodyklė_VALUE) == ADDRESS && naudotojas.보낸창구(rodyklė_VALUE) == jungtis_VALUE;
        if (같음) for (int INDEX = 0; INDEX < 받은길이; INDEX++) if (duomenys[INDEX] != Turinys_VALUE.charAt(INDEX)) 같음 = false;
        naudotojas.Uždaryti_tinklas(rodyklė_VALUE);
        if (받은길이 < 0) { naudotojas.Rašymas("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        naudotojas.Rašymas(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
