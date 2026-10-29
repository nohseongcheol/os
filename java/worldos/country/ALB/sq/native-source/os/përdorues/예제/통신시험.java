// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Ekzekuto() {
        int 첫째 = përdorues.hap_rrjet(45000);
        if (첫째 < 0) { përdorues.Shkrimi("NETWORK UNAVAILABLE\n"); return 3; }
        int[] të_dhëna = new int[8];
        boolean kaloj_VALUE = përdorues.hap_rrjet(45000) == -98
            && përdorues.자료받기(첫째, të_dhëna, 0) == -11
            && përdorues.자료받기(첫째, të_dhëna, 50) == -110
            && përdorues.자료받기(첫째, të_dhëna, 3000) == -22
            && përdorues.dërgoj_të_dhëna(첫째, 0x0a000202, 9, të_dhëna, 9) == -90
            && përdorues.자료받기(첫째, null, 0) == -14
            && përdorues.mbyll_rrjet(첫째) == 0 && përdorues.mbyll_rrjet(첫째) == -9;
        përdorues.Shkrimi(kaloj_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return kaloj_VALUE ? 0 : 1;
    }
}
