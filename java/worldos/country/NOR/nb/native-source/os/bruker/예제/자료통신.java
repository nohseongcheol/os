// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int siffer_VERDI(String Tekst) {
        if (Tekst == null || Tekst.length() == 0) return -1;
        int KR = 0;
        for (int INDEKS = 0; INDEKS < Tekst.length(); INDEKS++) {
            int VERDI = Tekst.charAt(INDEKS) - '0';
            if (VERDI < 0 || VERDI > 9 || KR > 6553) return -1;
            KR = KR * 10 + VERDI;
            if (KR > 65535) return -1;
        }
        return KR;
    }
    static int e_post(String Tekst) {
        if (Tekst == null) return 0;
        int VERDI = 0, KR = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEKS = 0; INDEKS <= Tekst.length(); INDEKS++) {
            int 문자 = INDEKS == Tekst.length() ? '.' : Tekst.charAt(INDEKS);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                KR = (KR << 8) | VERDI; 부분++; VERDI = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                VERDI = VERDI * 10 + 문자 - '0';
                if (++자릿수 > 3 || VERDI > 255) return 0;
            }
        }
        return 부분 == 4 ? KR : 0;
    }
    public static int Kjør_2() {
        if (bruker.인수개수() != 3) { bruker.Skriv("Usage: run udp IP PORT TEXT\n"); return 2; }
        int e_post = e_post(bruker.Argumenter(0)), port_VERDI = siffer_VERDI(bruker.Argumenter(1));
        String Innhold_VERDI = bruker.Argumenter(2);
        if (e_post == 0 || port_VERDI < 1 || Innhold_VERDI.length() > 1024) { bruker.Skriv("Bad destination\n"); return 2; }
        int håndtak_VERDI = bruker.åpen_nettverk(0);
        if (håndtak_VERDI < 0) { bruker.Skriv("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] data = new int[1024];
        for (int INDEKS = 0; INDEKS < Innhold_VERDI.length(); INDEKS++) data[INDEKS] = Innhold_VERDI.charAt(INDEKS);
        if (bruker.sende_data(håndtak_VERDI, e_post, port_VERDI, data, Innhold_VERDI.length()) < 0) {
            bruker.Skriv("UDP SEND FAILED\n"); bruker.Lukk_nettverk(håndtak_VERDI); return 4;
        }
        bruker.Skriv("UDP SENT\n");
        int MOTTATT_AVKAST_lengde = bruker.motta_data(håndtak_VERDI, data, 1500);
        boolean 같음 = MOTTATT_AVKAST_lengde == Innhold_VERDI.length() && bruker.보낸주소(håndtak_VERDI) == e_post && bruker.보낸창구(håndtak_VERDI) == port_VERDI;
        if (같음) for (int INDEKS = 0; INDEKS < MOTTATT_AVKAST_lengde; INDEKS++) if (data[INDEKS] != Innhold_VERDI.charAt(INDEKS)) 같음 = false;
        bruker.Lukk_nettverk(håndtak_VERDI);
        if (MOTTATT_AVKAST_lengde < 0) { bruker.Skriv("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        bruker.Skriv(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
