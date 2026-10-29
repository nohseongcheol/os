// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int ruith() {
        int 첫째 = cleachdaiche.fosgail_lìonra(45000);
        if (첫째 < 0) { cleachdaiche.sgrìobh("NETWORK UNAVAILABLE\n"); return 3; }
        int[] dàta = new int[8];
        boolean sìn_air_adhart_VALUE = cleachdaiche.fosgail_lìonra(45000) == -98
            && cleachdaiche.자료받기(첫째, dàta, 0) == -11
            && cleachdaiche.자료받기(첫째, dàta, 50) == -110
            && cleachdaiche.자료받기(첫째, dàta, 3000) == -22
            && cleachdaiche.cuir_dàta(첫째, 0x0a000202, 9, dàta, 9) == -90
            && cleachdaiche.자료받기(첫째, null, 0) == -14
            && cleachdaiche.dùin_lìonra(첫째) == 0 && cleachdaiche.dùin_lìonra(첫째) == -9;
        cleachdaiche.sgrìobh(sìn_air_adhart_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return sìn_air_adhart_VALUE ? 0 : 1;
    }
}
