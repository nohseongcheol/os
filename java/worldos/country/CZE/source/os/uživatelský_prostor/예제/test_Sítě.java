// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Sítě {
    public static int Spustit_2() {
        int 첫째 = uživatelský_prostor.otevřít_síť(45000);
        if (첫째 < 0) { uživatelský_prostor.Zápis("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean předat_HODNOTA = uživatelský_prostor.otevřít_síť(45000) == -98
            && uživatelský_prostor.dostat_data(첫째, data, 0) == -11
            && uživatelský_prostor.dostat_data(첫째, data, 50) == -110
            && uživatelský_prostor.dostat_data(첫째, data, 3000) == -22
            && uživatelský_prostor.poslat_data(첫째, 0x0a000202, 9, data, 9) == -90
            && uživatelský_prostor.dostat_data(첫째, null, 0) == -14
            && uživatelský_prostor.Zavřít_síť(첫째) == 0 && uživatelský_prostor.Zavřít_síť(첫째) == -9;
        uživatelský_prostor.Zápis(předat_HODNOTA ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return předat_HODNOTA ? 0 : 1;
    }
}
