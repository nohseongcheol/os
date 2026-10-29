// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Palaist() {
        int 첫째 = lietotājs.atvērt_tīkls(45000);
        if (첫째 < 0) { lietotājs.Rakstīt("NETWORK UNAVAILABLE\n"); return 3; }
        int[] dati = new int[8];
        boolean padot_VALUE = lietotājs.atvērt_tīkls(45000) == -98
            && lietotājs.saņemt_dati(첫째, dati, 0) == -11
            && lietotājs.saņemt_dati(첫째, dati, 50) == -110
            && lietotājs.saņemt_dati(첫째, dati, 3000) == -22
            && lietotājs.sūtīt_dati(첫째, 0x0a000202, 9, dati, 9) == -90
            && lietotājs.saņemt_dati(첫째, null, 0) == -14
            && lietotājs.Aizvērt_tīkls(첫째) == 0 && lietotājs.Aizvērt_tīkls(첫째) == -9;
        lietotājs.Rakstīt(padot_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return padot_VALUE ? 0 : 1;
    }
}
