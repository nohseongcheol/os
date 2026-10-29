// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Sieć {
    public static int Uruchom_2() {
        int 첫째 = przestrzeń_użytkownika.otwarty_sieć(45000);
        if (첫째 < 0) { przestrzeń_użytkownika.Zapis("NETWORK UNAVAILABLE\n"); return 3; }
        int[] dane = new int[8];
        boolean przekazać_WARTOŚĆ = przestrzeń_użytkownika.otwarty_sieć(45000) == -98
            && przestrzeń_użytkownika.odbierać_dane(첫째, dane, 0) == -11
            && przestrzeń_użytkownika.odbierać_dane(첫째, dane, 50) == -110
            && przestrzeń_użytkownika.odbierać_dane(첫째, dane, 3000) == -22
            && przestrzeń_użytkownika.wysłać_dane(첫째, 0x0a000202, 9, dane, 9) == -90
            && przestrzeń_użytkownika.odbierać_dane(첫째, null, 0) == -14
            && przestrzeń_użytkownika.Zamknij_sieć(첫째) == 0 && przestrzeń_użytkownika.Zamknij_sieć(첫째) == -9;
        przestrzeń_użytkownika.Zapis(przekazać_WARTOŚĆ ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return przekazać_WARTOŚĆ ? 0 : 1;
    }
}
