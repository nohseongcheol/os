// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Käivita_2() {
        int 첫째 = kasutaja.avama_võrk(45000);
        if (첫째 < 0) { kasutaja.Kirjutamine("NETWORK UNAVAILABLE\n"); return 3; }
        int[] andmed = new int[8];
        boolean edastama_VALUE = kasutaja.avama_võrk(45000) == -98
            && kasutaja.saama_andmed(첫째, andmed, 0) == -11
            && kasutaja.saama_andmed(첫째, andmed, 50) == -110
            && kasutaja.saama_andmed(첫째, andmed, 3000) == -22
            && kasutaja.saatma_andmed(첫째, 0x0a000202, 9, andmed, 9) == -90
            && kasutaja.saama_andmed(첫째, null, 0) == -14
            && kasutaja.Sule_võrk(첫째) == 0 && kasutaja.Sule_võrk(첫째) == -9;
        kasutaja.Kirjutamine(edastama_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return edastama_VALUE ? 0 : 1;
    }
}
