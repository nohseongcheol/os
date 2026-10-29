// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Velikost/홀수 길이 데이터그램으로 dejanski_podatki RTL8139 sprejeti_sprejemati_prejeti_prejemati_VALUE Loop_VALUE 순환을 시험한다. */
public final class mreža_Loop {
    public static int Zaženi() {
        if (uporabnik.인수개수() != 1) { uporabnik.Pisanje("Usage: run stress PORT\n"); return 2; }
        String Besedilo = uporabnik.Argumenti(0);
        int vrata_VALUE = 0;
        for (int INDEX = 0; INDEX < Besedilo.length(); INDEX++) {
            if (Besedilo.charAt(INDEX) < '0' || Besedilo.charAt(INDEX) > '9' || vrata_VALUE > 6553) return 2;
            vrata_VALUE = vrata_VALUE * 10 + Besedilo.charAt(INDEX) - '0';
        }
        if (vrata_VALUE < 1 || vrata_VALUE > 65535) return 2;
        int ročica_VALUE = uporabnik.odprto_mreža(0);
        if (ročica_VALUE < 0) return 3;
        int[] podatki = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int 길이 = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < 길이; INDEX++) podatki[INDEX] = (INDEX + 회차) & 255;
            if (uporabnik.poslati_podatki(ročica_VALUE, 0x0a000202, vrata_VALUE, podatki, 길이) != 길이) return 4;
            if (uporabnik.sprejeti_sprejemati_prejeti_prejemati_podatki(ročica_VALUE, podatki, 300) != 길이) return 5;
            for (int INDEX = 0; INDEX < 길이; INDEX++) if (podatki[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        uporabnik.Zapri_mreža(ročica_VALUE);
        uporabnik.Pisanje("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
