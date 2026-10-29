// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Sebenzisa() {
        int 첫째 = umsebenzisi.vula_iNethiwekhi(45000);
        if (첫째 < 0) { umsebenzisi.Bhala("NETWORK UNAVAILABLE\n"); return 3; }
        int[] imininingwane = new int[8];
        boolean dlulisa_inani = umsebenzisi.vula_iNethiwekhi(45000) == -98
            && umsebenzisi.자료받기(첫째, imininingwane, 0) == -11
            && umsebenzisi.자료받기(첫째, imininingwane, 50) == -110
            && umsebenzisi.자료받기(첫째, imininingwane, 3000) == -22
            && umsebenzisi.Thumela_imininingwane(첫째, 0x0a000202, 9, imininingwane, 9) == -90
            && umsebenzisi.자료받기(첫째, null, 0) == -14
            && umsebenzisi.vala_iNethiwekhi(첫째) == 0 && umsebenzisi.vala_iNethiwekhi(첫째) == -9;
        umsebenzisi.Bhala(dlulisa_inani ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return dlulisa_inani ? 0 : 1;
    }
}
