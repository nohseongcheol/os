// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Keyra_2() {
        int 첫째 = notandi.opið_Net(45000);
        if (첫째 < 0) { notandi.Skrift("NETWORK UNAVAILABLE\n"); return 3; }
        int[] gögn = new int[8];
        boolean senda_VALUE = notandi.opið_Net(45000) == -98
            && notandi.자료받기(첫째, gögn, 0) == -11
            && notandi.자료받기(첫째, gögn, 50) == -110
            && notandi.자료받기(첫째, gögn, 3000) == -22
            && notandi.senda_gögn(첫째, 0x0a000202, 9, gögn, 9) == -90
            && notandi.자료받기(첫째, null, 0) == -14
            && notandi.loka_Net(첫째) == 0 && notandi.loka_Net(첫째) == -9;
        notandi.Skrift(senda_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return senda_VALUE ? 0 : 1;
    }
}
