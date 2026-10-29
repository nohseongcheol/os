// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 자료통신 {
    static int digitu_balio(String Testua) {
        if (Testua == null || Testua.length() == 0) return -1;
        int EMAITZA = 0;
        for (int INDIZE = 0; INDIZE < Testua.length(); INDIZE++) {
            int balio = Testua.charAt(INDIZE) - '0';
            if (balio < 0 || balio > 9 || EMAITZA > 6553) return -1;
            EMAITZA = EMAITZA * 10 + balio;
            if (EMAITZA > 65535) return -1;
        }
        return EMAITZA;
    }
    static int helbide(String Testua) {
        if (Testua == null) return 0;
        int balio = 0, EMAITZA = 0, 부분 = 0, 자릿수 = 0;
        for (int INDIZE = 0; INDIZE <= Testua.length(); INDIZE++) {
            int 문자 = INDIZE == Testua.length() ? '.' : Testua.charAt(INDIZE);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                EMAITZA = (EMAITZA << 8) | balio; 부분++; balio = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                balio = balio * 10 + 문자 - '0';
                if (++자릿수 > 3 || balio > 255) return 0;
            }
        }
        return 부분 == 4 ? EMAITZA : 0;
    }
    public static int Exekutatu_2() {
        if (erabiltzaile.인수개수() != 3) { erabiltzaile.Idatzi("Usage: run udp IP PORT TEXT\n"); return 2; }
        int helbide = helbide(erabiltzaile.Argumentuak(0)), ataka_balio = digitu_balio(erabiltzaile.Argumentuak(1));
        String eduki_balio = erabiltzaile.Argumentuak(2);
        if (helbide == 0 || ataka_balio < 1 || eduki_balio.length() > 1024) { erabiltzaile.Idatzi("Bad destination\n"); return 2; }
        int helduleku_balio = erabiltzaile.ireki_sare(0);
        if (helduleku_balio < 0) { erabiltzaile.Idatzi("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] datuak = new int[1024];
        for (int INDIZE = 0; INDIZE < eduki_balio.length(); INDIZE++) datuak[INDIZE] = eduki_balio.charAt(INDIZE);
        if (erabiltzaile.bidali_datuak(helduleku_balio, helbide, ataka_balio, datuak, eduki_balio.length()) < 0) {
            erabiltzaile.Idatzi("UDP SEND FAILED\n"); erabiltzaile.itxi_sare(helduleku_balio); return 4;
        }
        erabiltzaile.Idatzi("UDP SENT\n");
        int RECEIVED_luzera = erabiltzaile.자료받기(helduleku_balio, datuak, 1500);
        boolean 같음 = RECEIVED_luzera == eduki_balio.length() && erabiltzaile.보낸주소(helduleku_balio) == helbide && erabiltzaile.보낸창구(helduleku_balio) == ataka_balio;
        if (같음) for (int INDIZE = 0; INDIZE < RECEIVED_luzera; INDIZE++) if (datuak[INDIZE] != eduki_balio.charAt(INDIZE)) 같음 = false;
        erabiltzaile.itxi_sare(helduleku_balio);
        if (RECEIVED_luzera < 0) { erabiltzaile.Idatzi("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        erabiltzaile.Idatzi(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
