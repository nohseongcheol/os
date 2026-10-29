// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Grootte/홀수 tijdsduur_WAARDE 데이터그램으로 werkelijk_gegevens RTL8139 ontvangen_WAARDE lus_WAARDE 순환을 시험한다. */
public final class net_lus {
    public static int starten() {
        if (gebruikersruimte.인수개수() != 1) { gebruikersruimte.Schrijven("Usage: run stress PORT\n"); return 2; }
        String tekst = gebruikersruimte.argumenten(0);
        int poort_WAARDE = 0;
        for (int INDEX = 0; INDEX < tekst.length(); INDEX++) {
            if (tekst.charAt(INDEX) < '0' || tekst.charAt(INDEX) > '9' || poort_WAARDE > 6553) return 2;
            poort_WAARDE = poort_WAARDE * 10 + tekst.charAt(INDEX) - '0';
        }
        if (poort_WAARDE < 1 || poort_WAARDE > 65535) return 2;
        int greep_WAARDE = gebruikersruimte.open_net(0);
        if (greep_WAARDE < 0) return 3;
        int[] gegevens = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int tijdsduur_WAARDE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) gegevens[INDEX] = (INDEX + 회차) & 255;
            if (gebruikersruimte.e_mailen_gegevens(greep_WAARDE, 0x0a000202, poort_WAARDE, gegevens, tijdsduur_WAARDE) != tijdsduur_WAARDE) return 4;
            if (gebruikersruimte.ontvangen_gegevens(greep_WAARDE, gegevens, 300) != tijdsduur_WAARDE) return 5;
            for (int INDEX = 0; INDEX < tijdsduur_WAARDE; INDEX++) if (gegevens[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        gebruikersruimte.Sluiten_net(greep_WAARDE);
        gebruikersruimte.Schrijven("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
