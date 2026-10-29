// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int dirisa() {
        int 첫째 = modirisi.bula_Neteweke(45000);
        if (첫째 < 0) { modirisi.kwala("NETWORK UNAVAILABLE\n"); return 3; }
        int[] tshedimosetso = new int[8];
        boolean fetisa_Boleng = modirisi.bula_Neteweke(45000) == -98
            && modirisi.자료받기(첫째, tshedimosetso, 0) == -11
            && modirisi.자료받기(첫째, tshedimosetso, 50) == -110
            && modirisi.자료받기(첫째, tshedimosetso, 3000) == -22
            && modirisi.romela_tshedimosetso(첫째, 0x0a000202, 9, tshedimosetso, 9) == -90
            && modirisi.자료받기(첫째, null, 0) == -14
            && modirisi.tswala_Neteweke(첫째) == 0 && modirisi.tswala_Neteweke(첫째) == -9;
        modirisi.kwala(fetisa_Boleng ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return fetisa_Boleng ? 0 : 1;
    }
}
