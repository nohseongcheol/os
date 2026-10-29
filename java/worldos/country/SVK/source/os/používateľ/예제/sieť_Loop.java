// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 Veľkosť/홀수 dĺžka_VALUE 데이터그램으로 skutočný_údaje RTL8139 dostať_VALUE Loop_VALUE 순환을 시험한다. */
public final class sieť_Loop {
    public static int Spustiť_2() {
        if (používateľ.인수개수() != 1) { používateľ.Zápis("Usage: run stress PORT\n"); return 2; }
        String Spracovanie_textu = používateľ.Argumenty(0);
        int port_VALUE = 0;
        for (int INDEX = 0; INDEX < Spracovanie_textu.length(); INDEX++) {
            if (Spracovanie_textu.charAt(INDEX) < '0' || Spracovanie_textu.charAt(INDEX) > '9' || port_VALUE > 6553) return 2;
            port_VALUE = port_VALUE * 10 + Spracovanie_textu.charAt(INDEX) - '0';
        }
        if (port_VALUE < 1 || port_VALUE > 65535) return 2;
        int rukoväť_VALUE = používateľ.otvoriť_sieť(0);
        if (rukoväť_VALUE < 0) return 3;
        int[] údaje = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int dĺžka_VALUE = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) údaje[INDEX] = (INDEX + 회차) & 255;
            if (používateľ.odoslať_údaje(rukoväť_VALUE, 0x0a000202, port_VALUE, údaje, dĺžka_VALUE) != dĺžka_VALUE) return 4;
            if (používateľ.dostať_údaje(rukoväť_VALUE, údaje, 300) != dĺžka_VALUE) return 5;
            for (int INDEX = 0; INDEX < dĺžka_VALUE; INDEX++) if (údaje[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        používateľ.Zavrieť_sieť(rukoväť_VALUE);
        používateľ.Zápis("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
