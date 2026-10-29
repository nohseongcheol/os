// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Rith_2() {
        int 첫째 = úsáideoir.oscail_Líonra(45000);
        if (첫째 < 0) { úsáideoir.Scríobh("NETWORK UNAVAILABLE\n"); return 3; }
        int[] sonraí = new int[8];
        boolean seol_ar_aghaidh_VALUE = úsáideoir.oscail_Líonra(45000) == -98
            && úsáideoir.자료받기(첫째, sonraí, 0) == -11
            && úsáideoir.자료받기(첫째, sonraí, 50) == -110
            && úsáideoir.자료받기(첫째, sonraí, 3000) == -22
            && úsáideoir.seol_sonraí(첫째, 0x0a000202, 9, sonraí, 9) == -90
            && úsáideoir.자료받기(첫째, null, 0) == -14
            && úsáideoir.dún_Líonra(첫째) == 0 && úsáideoir.dún_Líonra(첫째) == -9;
        úsáideoir.Scríobh(seol_ar_aghaidh_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return seol_ar_aghaidh_VALUE ? 0 : 1;
    }
}
