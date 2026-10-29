// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class preskusiti_Uporaba_omrežij {
    public static int Zaženi() {
        int 첫째 = uporabnik.odprto_mreža(45000);
        if (첫째 < 0) { uporabnik.Pisanje("NETWORK UNAVAILABLE\n"); return 3; }
        int[] podatki = new int[8];
        boolean posredovati_VALUE = uporabnik.odprto_mreža(45000) == -98
            && uporabnik.sprejeti_sprejemati_prejeti_prejemati_podatki(첫째, podatki, 0) == -11
            && uporabnik.sprejeti_sprejemati_prejeti_prejemati_podatki(첫째, podatki, 50) == -110
            && uporabnik.sprejeti_sprejemati_prejeti_prejemati_podatki(첫째, podatki, 3000) == -22
            && uporabnik.poslati_podatki(첫째, 0x0a000202, 9, podatki, 9) == -90
            && uporabnik.sprejeti_sprejemati_prejeti_prejemati_podatki(첫째, null, 0) == -14
            && uporabnik.Zapri_mreža(첫째) == 0 && uporabnik.Zapri_mreža(첫째) == -9;
        uporabnik.Pisanje(posredovati_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return posredovati_VALUE ? 0 : 1;
    }
}
