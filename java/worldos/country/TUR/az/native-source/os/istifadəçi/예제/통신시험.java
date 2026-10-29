// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int İcra_Et() {
        int 첫째 = istifadəçi.açmaq_Şəbəkə(45000);
        if (첫째 < 0) { istifadəçi.Yazma("NETWORK UNAVAILABLE\n"); return 3; }
        int[] verilənlər = new int[8];
        boolean ötürmək_VALUE = istifadəçi.açmaq_Şəbəkə(45000) == -98
            && istifadəçi.자료받기(첫째, verilənlər, 0) == -11
            && istifadəçi.자료받기(첫째, verilənlər, 50) == -110
            && istifadəçi.자료받기(첫째, verilənlər, 3000) == -22
            && istifadəçi.göndərmək_verilənlər(첫째, 0x0a000202, 9, verilənlər, 9) == -90
            && istifadəçi.자료받기(첫째, null, 0) == -14
            && istifadəçi.bağlamaq_Şəbəkə(첫째) == 0 && istifadəçi.bağlamaq_Şəbəkə(첫째) == -9;
        istifadəçi.Yazma(ötürmək_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return ötürmək_VALUE ? 0 : 1;
    }
}
