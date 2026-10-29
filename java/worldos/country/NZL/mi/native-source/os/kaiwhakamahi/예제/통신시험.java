// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int whakahaere() {
        int 첫째 = kaiwhakamahi.tiwhikete_whatunga(45000);
        if (첫째 < 0) { kaiwhakamahi.Tuhia("NETWORK UNAVAILABLE\n"); return 3; }
        int[] raraunga = new int[8];
        boolean whakawhiti_uara = kaiwhakamahi.tiwhikete_whatunga(45000) == -98
            && kaiwhakamahi.자료받기(첫째, raraunga, 0) == -11
            && kaiwhakamahi.자료받기(첫째, raraunga, 50) == -110
            && kaiwhakamahi.자료받기(첫째, raraunga, 3000) == -22
            && kaiwhakamahi.tuku_raraunga(첫째, 0x0a000202, 9, raraunga, 9) == -90
            && kaiwhakamahi.자료받기(첫째, null, 0) == -14
            && kaiwhakamahi.kati_whatunga(첫째) == 0 && kaiwhakamahi.kati_whatunga(첫째) == -9;
        kaiwhakamahi.Tuhia(whakawhiti_uara ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return whakawhiti_uara ? 0 : 1;
    }
}
