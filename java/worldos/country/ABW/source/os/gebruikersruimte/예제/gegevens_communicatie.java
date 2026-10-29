// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class gegevens_communicatie {
    static int cijfer_WAARDE(String tekst) {
        if (tekst == null || tekst.length() == 0) return -1;
        int resultaat = 0;
        for (int INDEX = 0; INDEX < tekst.length(); INDEX++) {
            int WAARDE = tekst.charAt(INDEX) - '0';
            if (WAARDE < 0 || WAARDE > 9 || resultaat > 6553) return -1;
            resultaat = resultaat * 10 + WAARDE;
            if (resultaat > 65535) return -1;
        }
        return resultaat;
    }
    static int ADRES(String tekst) {
        if (tekst == null) return 0;
        int WAARDE = 0, resultaat = 0, 부분 = 0, 자릿수 = 0;
        for (int INDEX = 0; INDEX <= tekst.length(); INDEX++) {
            int 문자 = INDEX == tekst.length() ? '.' : tekst.charAt(INDEX);
            if (문자 == '.') {
                if (자릿수 == 0 || 부분 == 4) return 0;
                resultaat = (resultaat << 8) | WAARDE; 부분++; WAARDE = 0; 자릿수 = 0;
            } else {
                if (문자 < '0' || 문자 > '9') return 0;
                WAARDE = WAARDE * 10 + 문자 - '0';
                if (++자릿수 > 3 || WAARDE > 255) return 0;
            }
        }
        return 부분 == 4 ? resultaat : 0;
    }
    public static int starten() {
        if (gebruikersruimte.인수개수() != 3) { gebruikersruimte.Schrijven("Usage: run udp IP PORT TEXT\n"); return 2; }
        int ADRES = ADRES(gebruikersruimte.argumenten(0)), poort_WAARDE = cijfer_WAARDE(gebruikersruimte.argumenten(1));
        String Inhoud_WAARDE = gebruikersruimte.argumenten(2);
        if (ADRES == 0 || poort_WAARDE < 1 || Inhoud_WAARDE.length() > 1024) { gebruikersruimte.Schrijven("Bad destination\n"); return 2; }
        int greep_WAARDE = gebruikersruimte.open_net(0);
        if (greep_WAARDE < 0) { gebruikersruimte.Schrijven("UDP OPEN FAILED (network unavailable)\n"); return 3; }
        int[] gegevens = new int[1024];
        for (int INDEX = 0; INDEX < Inhoud_WAARDE.length(); INDEX++) gegevens[INDEX] = Inhoud_WAARDE.charAt(INDEX);
        if (gebruikersruimte.e_mailen_gegevens(greep_WAARDE, ADRES, poort_WAARDE, gegevens, Inhoud_WAARDE.length()) < 0) {
            gebruikersruimte.Schrijven("UDP SEND FAILED\n"); gebruikersruimte.Sluiten_net(greep_WAARDE); return 4;
        }
        gebruikersruimte.Schrijven("UDP SENT\n");
        int OPBRENGST_tijdsduur = gebruikersruimte.ontvangen_gegevens(greep_WAARDE, gegevens, 1500);
        boolean 같음 = OPBRENGST_tijdsduur == Inhoud_WAARDE.length() && gebruikersruimte.보낸주소(greep_WAARDE) == ADRES && gebruikersruimte.보낸창구(greep_WAARDE) == poort_WAARDE;
        if (같음) for (int INDEX = 0; INDEX < OPBRENGST_tijdsduur; INDEX++) if (gegevens[INDEX] != Inhoud_WAARDE.charAt(INDEX)) 같음 = false;
        gebruikersruimte.Sluiten_net(greep_WAARDE);
        if (OPBRENGST_tijdsduur < 0) { gebruikersruimte.Schrijven("UDP RECEIVE TIMEOUT/ERROR\n"); return 5; }
        gebruikersruimte.Schrijven(같음 ? "UDP ECHO PASS\n" : "UDP REPLY MISMATCH\n");
        return 같음 ? 0 : 6;
    }
}
