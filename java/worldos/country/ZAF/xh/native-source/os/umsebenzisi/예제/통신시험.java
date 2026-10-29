// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Phumeza() {
        int 첫째 = umsebenzisi.vula_Inethiwekhi(45000);
        if (첫째 < 0) { umsebenzisi.Bhala("NETWORK UNAVAILABLE\n"); return 3; }
        int[] iingcombolo = new int[8];
        boolean dlulisela_ixabiso = umsebenzisi.vula_Inethiwekhi(45000) == -98
            && umsebenzisi.자료받기(첫째, iingcombolo, 0) == -11
            && umsebenzisi.자료받기(첫째, iingcombolo, 50) == -110
            && umsebenzisi.자료받기(첫째, iingcombolo, 3000) == -22
            && umsebenzisi.thumela_iingcombolo(첫째, 0x0a000202, 9, iingcombolo, 9) == -90
            && umsebenzisi.자료받기(첫째, null, 0) == -14
            && umsebenzisi.vala_Inethiwekhi(첫째) == 0 && umsebenzisi.vala_Inethiwekhi(첫째) == -9;
        umsebenzisi.Bhala(dlulisela_ixabiso ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return dlulisela_ixabiso ? 0 : 1;
    }
}
