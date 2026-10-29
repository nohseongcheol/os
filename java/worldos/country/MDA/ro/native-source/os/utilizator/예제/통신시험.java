// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Pornește() {
        int 첫째 = utilizator.crea_rețea(45000);
        if (첫째 < 0) { utilizator.Scriere("NETWORK UNAVAILABLE\n"); return 3; }
        int[] date = new int[8];
        boolean transfera_VALUE = utilizator.crea_rețea(45000) == -98
            && utilizator.primi_date(첫째, date, 0) == -11
            && utilizator.primi_date(첫째, date, 50) == -110
            && utilizator.primi_date(첫째, date, 3000) == -22
            && utilizator.trimite_date(첫째, 0x0a000202, 9, date, 9) == -90
            && utilizator.primi_date(첫째, null, 0) == -14
            && utilizator.închide_rețea(첫째) == 0 && utilizator.închide_rețea(첫째) == -9;
        utilizator.Scriere(transfera_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return transfera_VALUE ? 0 : 1;
    }
}
