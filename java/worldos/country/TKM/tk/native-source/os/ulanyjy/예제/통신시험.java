// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Bitir() {
        int 첫째 = ulanyjy.aç_Tor(45000);
        if (첫째 < 0) { ulanyjy.Ýaz("NETWORK UNAVAILABLE\n"); return 3; }
        int[] maglumat = new int[8];
        boolean 통과 = ulanyjy.aç_Tor(45000) == -98
            && ulanyjy.자료받기(첫째, maglumat, 0) == -11
            && ulanyjy.자료받기(첫째, maglumat, 50) == -110
            && ulanyjy.자료받기(첫째, maglumat, 3000) == -22
            && ulanyjy.iber_maglumat(첫째, 0x0a000202, 9, maglumat, 9) == -90
            && ulanyjy.자료받기(첫째, null, 0) == -14
            && ulanyjy.ýap_Tor(첫째) == 0 && ulanyjy.ýap_Tor(첫째) == -9;
        ulanyjy.Ýaz(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
