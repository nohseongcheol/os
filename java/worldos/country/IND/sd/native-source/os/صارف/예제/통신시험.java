// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int هلائڻ() {
        int 첫째 = صارف.ٺاھيو_نيٽ_ورڪ(45000);
        if (첫째 < 0) { صارف.لکو("NETWORK UNAVAILABLE\n"); return 3; }
        int[] ڪوائف = new int[8];
        boolean 통과 = صارف.ٺاھيو_نيٽ_ورڪ(45000) == -98
            && صارف.자료받기(첫째, ڪوائف, 0) == -11
            && صارف.자료받기(첫째, ڪوائف, 50) == -110
            && صارف.자료받기(첫째, ڪوائف, 3000) == -22
            && صارف.اي_ميل_ڪوائف(첫째, 0x0a000202, 9, ڪوائف, 9) == -90
            && صارف.자료받기(첫째, null, 0) == -14
            && صارف.بند_ڪرڻ_نيٽ_ورڪ(첫째) == 0 && صارف.بند_ڪرڻ_نيٽ_ورڪ(첫째) == -9;
        صارف.لکو(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
