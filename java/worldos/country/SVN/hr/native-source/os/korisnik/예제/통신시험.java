// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Pokreni() {
        int 첫째 = korisnik.otvoreno_mreža(45000);
        if (첫째 < 0) { korisnik.Zapisuj("NETWORK UNAVAILABLE\n"); return 3; }
        int[] podaci = new int[8];
        boolean proslijediti_VALUE = korisnik.otvoreno_mreža(45000) == -98
            && korisnik.primiti_podaci(첫째, podaci, 0) == -11
            && korisnik.primiti_podaci(첫째, podaci, 50) == -110
            && korisnik.primiti_podaci(첫째, podaci, 3000) == -22
            && korisnik.slati_podaci(첫째, 0x0a000202, 9, podaci, 9) == -90
            && korisnik.primiti_podaci(첫째, null, 0) == -14
            && korisnik.Zatvori_mreža(첫째) == 0 && korisnik.Zatvori_mreža(첫째) == -9;
        korisnik.Zapisuj(proslijediti_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return proslijediti_VALUE ? 0 : 1;
    }
}
