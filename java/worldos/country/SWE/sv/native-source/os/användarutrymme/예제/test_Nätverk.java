// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Nätverk {
    public static int Kör() {
        int 첫째 = användarutrymme.skapa_nätverk(45000);
        if (첫째 < 0) { användarutrymme.Skriv("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean skicka_värde = användarutrymme.skapa_nätverk(45000) == -98
            && användarutrymme.få_data(첫째, data, 0) == -11
            && användarutrymme.få_data(첫째, data, 50) == -110
            && användarutrymme.få_data(첫째, data, 3000) == -22
            && användarutrymme.skicka_data(첫째, 0x0a000202, 9, data, 9) == -90
            && användarutrymme.få_data(첫째, null, 0) == -14
            && användarutrymme.Stäng_nätverk(첫째) == 0 && användarutrymme.Stäng_nätverk(첫째) == -9;
        användarutrymme.Skriv(skicka_värde ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return skicka_värde ? 0 : 1;
    }
}
