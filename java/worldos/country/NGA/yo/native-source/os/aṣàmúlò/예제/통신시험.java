// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Rọ́ọ̀nù() {
        int 첫째 = aṣàmúlò.ṣí_Alásopọ̀(45000);
        if (첫째 < 0) { aṣàmúlò.Kọ("NETWORK UNAVAILABLE\n"); return 3; }
        int[] détà = new int[8];
        boolean fí_dátà_ránṣẹ́_iye = aṣàmúlò.ṣí_Alásopọ̀(45000) == -98
            && aṣàmúlò.자료받기(첫째, détà, 0) == -11
            && aṣàmúlò.자료받기(첫째, détà, 50) == -110
            && aṣàmúlò.자료받기(첫째, détà, 3000) == -22
            && aṣàmúlò.í_meèlì_détà(첫째, 0x0a000202, 9, détà, 9) == -90
            && aṣàmúlò.자료받기(첫째, null, 0) == -14
            && aṣàmúlò.pa_dé_Alásopọ̀(첫째) == 0 && aṣàmúlò.pa_dé_Alásopọ̀(첫째) == -9;
        aṣàmúlò.Kọ(fí_dátà_ránṣẹ́_iye ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return fí_dátà_ránṣẹ́_iye ? 0 : 1;
    }
}
