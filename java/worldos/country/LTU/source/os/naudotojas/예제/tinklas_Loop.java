// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Dydis/홀수 길이 데이터그램으로 faktinis_duomenys RTL8139 gauti_VALUE_cef4d8ab Loop_VALUE 순환을 시험한다. */
public final class tinklas_Loop {
    public static int Paleisti() {
        if (naudotojas.인수개수() != 1) { naudotojas.Rašymas("Usage: run stress PORT\n"); return 2; }
        String Tekstas = naudotojas.Argumentai(0);
        int jungtis_VALUE = 0;
        for (int INDEX = 0; INDEX < Tekstas.length(); INDEX++) {
            if (Tekstas.charAt(INDEX) < '0' || Tekstas.charAt(INDEX) > '9' || jungtis_VALUE > 6553) return 2;
            jungtis_VALUE = jungtis_VALUE * 10 + Tekstas.charAt(INDEX) - '0';
        }
        if (jungtis_VALUE < 1 || jungtis_VALUE > 65535) return 2;
        int rodyklė_VALUE = naudotojas.kurti_tinklas(0);
        if (rodyklė_VALUE < 0) return 3;
        int[] duomenys = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int 길이 = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < 길이; INDEX++) duomenys[INDEX] = (INDEX + 회차) & 255;
            if (naudotojas.siųsti_duomenys(rodyklė_VALUE, 0x0a000202, jungtis_VALUE, duomenys, 길이) != 길이) return 4;
            if (naudotojas.gauti_duomenys(rodyklė_VALUE, duomenys, 300) != 길이) return 5;
            for (int INDEX = 0; INDEX < 길이; INDEX++) if (duomenys[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        naudotojas.Uždaryti_tinklas(rodyklė_VALUE);
        naudotojas.Rašymas("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
