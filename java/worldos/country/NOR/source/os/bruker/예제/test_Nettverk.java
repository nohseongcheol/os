// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Nettverk {
    public static int Kjør_2() {
        int 첫째 = bruker.åpen_nettverk(45000);
        if (첫째 < 0) { bruker.Skriv("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean sende_VERDI = bruker.åpen_nettverk(45000) == -98
            && bruker.motta_data(첫째, data, 0) == -11
            && bruker.motta_data(첫째, data, 50) == -110
            && bruker.motta_data(첫째, data, 3000) == -22
            && bruker.sende_data(첫째, 0x0a000202, 9, data, 9) == -90
            && bruker.motta_data(첫째, null, 0) == -14
            && bruker.Lukk_nettverk(첫째) == 0 && bruker.Lukk_nettverk(첫째) == -9;
        bruker.Skriv(sende_VERDI ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return sende_VERDI ? 0 : 1;
    }
}
