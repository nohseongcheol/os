// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Pokreni() {
        int 첫째 = korisnik.kreirati_Mreža(45000);
        if (첫째 < 0) { korisnik.Piši("NETWORK UNAVAILABLE\n"); return 3; }
        int[] podaci = new int[8];
        boolean proslijediti_VALUE = korisnik.kreirati_Mreža(45000) == -98
            && korisnik.자료받기(첫째, podaci, 0) == -11
            && korisnik.자료받기(첫째, podaci, 50) == -110
            && korisnik.자료받기(첫째, podaci, 3000) == -22
            && korisnik.poslati_podaci(첫째, 0x0a000202, 9, podaci, 9) == -90
            && korisnik.자료받기(첫째, null, 0) == -14
            && korisnik.zatvoriti_Mreža(첫째) == 0 && korisnik.zatvoriti_Mreža(첫째) == -9;
        korisnik.Piši(proslijediti_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return proslijediti_VALUE ? 0 : 1;
    }
}
