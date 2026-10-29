// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Køyr_2() {
        int 첫째 = brukar.opne_Nettverk(45000);
        if (첫째 < 0) { brukar.Skriv("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean sende_VALUE = brukar.opne_Nettverk(45000) == -98
            && brukar.자료받기(첫째, data, 0) == -11
            && brukar.자료받기(첫째, data, 50) == -110
            && brukar.자료받기(첫째, data, 3000) == -22
            && brukar.sende_data(첫째, 0x0a000202, 9, data, 9) == -90
            && brukar.자료받기(첫째, null, 0) == -14
            && brukar.Lukk_Nettverk(첫째) == 0 && brukar.Lukk_Nettverk(첫째) == -9;
        brukar.Skriv(sende_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return sende_VALUE ? 0 : 1;
    }
}
