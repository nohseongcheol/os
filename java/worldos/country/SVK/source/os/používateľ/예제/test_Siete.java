// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Siete {
    public static int Spustiť_2() {
        int 첫째 = používateľ.otvoriť_sieť(45000);
        if (첫째 < 0) { používateľ.Zápis("NETWORK UNAVAILABLE\n"); return 3; }
        int[] údaje = new int[8];
        boolean odovzdať_VALUE = používateľ.otvoriť_sieť(45000) == -98
            && používateľ.dostať_údaje(첫째, údaje, 0) == -11
            && používateľ.dostať_údaje(첫째, údaje, 50) == -110
            && používateľ.dostať_údaje(첫째, údaje, 3000) == -22
            && používateľ.odoslať_údaje(첫째, 0x0a000202, 9, údaje, 9) == -90
            && používateľ.dostať_údaje(첫째, null, 0) == -14
            && používateľ.Zavrieť_sieť(첫째) == 0 && používateľ.Zavrieť_sieť(첫째) == -9;
        používateľ.Zápis(odovzdať_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return odovzdať_VALUE ? 0 : 1;
    }
}
