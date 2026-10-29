// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Bajarish() {
        int 첫째 = foydalanuvchi.ochmoq_Tarmoq(45000);
        if (첫째 < 0) { foydalanuvchi.Yozish("NETWORK UNAVAILABLE\n"); return 3; }
        int[] ma_lumotlar = new int[8];
        boolean 통과 = foydalanuvchi.ochmoq_Tarmoq(45000) == -98
            && foydalanuvchi.자료받기(첫째, ma_lumotlar, 0) == -11
            && foydalanuvchi.자료받기(첫째, ma_lumotlar, 50) == -110
            && foydalanuvchi.자료받기(첫째, ma_lumotlar, 3000) == -22
            && foydalanuvchi.yuborish_ma_lumotlar(첫째, 0x0a000202, 9, ma_lumotlar, 9) == -90
            && foydalanuvchi.자료받기(첫째, null, 0) == -14
            && foydalanuvchi.yopmoq_Tarmoq(첫째) == 0 && foydalanuvchi.yopmoq_Tarmoq(첫째) == -9;
        foydalanuvchi.Yozish(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
