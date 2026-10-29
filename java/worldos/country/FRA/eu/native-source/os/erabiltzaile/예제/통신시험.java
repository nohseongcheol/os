// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Exekutatu_2() {
        int 첫째 = erabiltzaile.ireki_sare(45000);
        if (첫째 < 0) { erabiltzaile.Idatzi("NETWORK UNAVAILABLE\n"); return 3; }
        int[] datuak = new int[8];
        boolean pasatu_balio = erabiltzaile.ireki_sare(45000) == -98
            && erabiltzaile.자료받기(첫째, datuak, 0) == -11
            && erabiltzaile.자료받기(첫째, datuak, 50) == -110
            && erabiltzaile.자료받기(첫째, datuak, 3000) == -22
            && erabiltzaile.bidali_datuak(첫째, 0x0a000202, 9, datuak, 9) == -90
            && erabiltzaile.자료받기(첫째, null, 0) == -14
            && erabiltzaile.itxi_sare(첫째) == 0 && erabiltzaile.itxi_sare(첫째) == -9;
        erabiltzaile.Idatzi(pasatu_balio ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return pasatu_balio ? 0 : 1;
    }
}
