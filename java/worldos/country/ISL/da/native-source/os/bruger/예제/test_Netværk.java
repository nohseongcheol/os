// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Netværk {
    public static int Kør_2() {
        int 첫째 = bruger.åben_netværk(45000);
        if (첫째 < 0) { bruger.Skrive("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean videregive_VÆRDI = bruger.åben_netværk(45000) == -98
            && bruger.modtage_data(첫째, data, 0) == -11
            && bruger.modtage_data(첫째, data, 50) == -110
            && bruger.modtage_data(첫째, data, 3000) == -22
            && bruger.maile_data(첫째, 0x0a000202, 9, data, 9) == -90
            && bruger.modtage_data(첫째, null, 0) == -14
            && bruger.Luk_netværk(첫째) == 0 && bruger.Luk_netværk(첫째) == -9;
        bruger.Skrive(videregive_VÆRDI ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return videregive_VÆRDI ? 0 : 1;
    }
}
