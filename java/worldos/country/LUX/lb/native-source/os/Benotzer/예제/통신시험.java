// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Laf() {
        int 첫째 = Benotzer.ariichten_Reseau(45000);
        if (첫째 < 0) { Benotzer.schreiwen("NETWORK UNAVAILABLE\n"); return 3; }
        int[] Daten = new int[8];
        boolean iwwermëttelen_VALUE = Benotzer.ariichten_Reseau(45000) == -98
            && Benotzer.자료받기(첫째, Daten, 0) == -11
            && Benotzer.자료받기(첫째, Daten, 50) == -110
            && Benotzer.자료받기(첫째, Daten, 3000) == -22
            && Benotzer.mailen_Daten(첫째, 0x0a000202, 9, Daten, 9) == -90
            && Benotzer.자료받기(첫째, null, 0) == -14
            && Benotzer.Clôture_Reseau(첫째) == 0 && Benotzer.Clôture_Reseau(첫째) == -9;
        Benotzer.schreiwen(iwwermëttelen_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return iwwermëttelen_VALUE ? 0 : 1;
    }
}
