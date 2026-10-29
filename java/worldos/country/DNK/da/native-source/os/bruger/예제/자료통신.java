// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int ciffer_VÆRDI(String Tekst) {
        if (Tekst == null || Tekst.length() == 0) return -1;
        int KR = 0;
        for (int INDEKS = 0; INDEKS < Tekst.length(); INDEKS++) {
            int VÆRDI = Tekst.charAt(INDEKS) - '0';
            if (VÆRDI < 0 || VÆRDI > 9 || KR > 6553) return -1;
            KR = KR * 10 + VÆRDI;
            if (KR > 65535) return -1;
        }
        return KR;
    }
    static int mail(String Tekst) {
        if (Tekst == null) return 0;
        int VÆRDI = 0, KR = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEKS = 0; INDEKS <= Tekst.length(); INDEKS++) {
            int 문자 = INDEKS == Tekst.length() ? '.' : Tekst.charAt(INDEKS);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                KR = (KR << 8) | VÆRDI; 부분++; VÆRDI = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VÆRDI = VÆRDI * 10 + 문자 - '0';
                if (++자릿수 > 3 || VÆRDI > 255) return 0;
            }
        }
        return 부분 == 4 ? KR : 0;
    }
    public static int Kør_2() {
        if (bruger.인수개수() != 3) { bruger.Skrive("Usage: run udp IP PORT TEXT\n"); return 2; }
        int mail = mail(bruger.Argumenter(0)), port_VÆRDI = ciffer_VÆRDI(bruger.Argumenter(1));
        String Indhold_VÆRDI = bruger.Argumenter(2);
        if (mail == 0 || port_VÆRDI < 1 || Indhold_VÆRDI.length() > 1024) { bruger.Skrive("Bad destination\n"); return 2; }
        int handle_VÆRDI = bruger.åben_netværk(0);
        if (handle_VÆRDI < 0) { bruger.Skrive("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEKS = 0; INDEKS < Indhold_VÆRDI.length(); INDEKS++) data[INDEKS] = Indhold_VÆRDI.charAt(INDEKS);
        if (bruger.maile_data(handle_VÆRDI, mail, port_VÆRDI, data, Indhold_VÆRDI.length()) < 0) {
            bruger.Skrive("UDP SEND FAILED\n"); bruger.Luk_netværk(handle_VÆRDI); return 4;
        }
        bruger.Skrive("UDP SENT\n");
        int MODTAGET_VED_UDLØB_varighed = bruger.modtage_data(handle_VÆRDI, data, 1500);
        boolean 같음 = MODTAGET_VED_UDLØB_varighed == Indhold_VÆRDI.length() && bruger.보낸주소(handle_VÆRDI) == mail && bruger.보낸창구(handle_VÆRDI) == port_VÆRDI;
        if (같음) for (int INDEKS = 0; INDEKS < MODTAGET_VED_UDLØB_varighed; INDEKS++) if (data[INDEKS] != Indhold_VÆRDI.charAt(INDEKS)) 같음 = false;
        bruger.Luk_netværk(handle_VÆRDI);
        if (MODTAGET_VED_UDLØB_varighed < 0) { bruger.Skrive("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        bruger.Skrive(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
