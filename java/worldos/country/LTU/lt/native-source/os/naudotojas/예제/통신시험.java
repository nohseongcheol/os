// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Paleisti() {
        int 첫째 = naudotojas.kurti_tinklas(45000);
        if (첫째 < 0) { naudotojas.Rašymas("NETWORK UNAVAILABLE\n"); return 3; }
        int[] duomenys = new int[8];
        boolean perduoti_VALUE = naudotojas.kurti_tinklas(45000) == -98
            && naudotojas.gauti_duomenys(첫째, duomenys, 0) == -11
            && naudotojas.gauti_duomenys(첫째, duomenys, 50) == -110
            && naudotojas.gauti_duomenys(첫째, duomenys, 3000) == -22
            && naudotojas.siųsti_duomenys(첫째, 0x0a000202, 9, duomenys, 9) == -90
            && naudotojas.gauti_duomenys(첫째, null, 0) == -14
            && naudotojas.Uždaryti_tinklas(첫째) == 0 && naudotojas.Uždaryti_tinklas(첫째) == -9;
        naudotojas.Rašymas(perduoti_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return perduoti_VALUE ? 0 : 1;
    }
}
