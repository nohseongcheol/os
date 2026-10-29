// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int 시작() {
        int 첫째 = atuqtuq.matuirli_Kasuqatigiitsimajut(45000);
        if (첫째 < 0) { atuqtuq.titiraq("NETWORK UNAVAILABLE\n"); return 3; }
        int[] titiqqat = new int[8];
        boolean 통과 = atuqtuq.matuirli_Kasuqatigiitsimajut(45000) == -98
            && atuqtuq.자료받기(첫째, titiqqat, 0) == -11
            && atuqtuq.자료받기(첫째, titiqqat, 50) == -110
            && atuqtuq.자료받기(첫째, titiqqat, 3000) == -22
            && atuqtuq.nassiutili_titiqqat(첫째, 0x0a000202, 9, titiqqat, 9) == -90
            && atuqtuq.자료받기(첫째, null, 0) == -14
            && atuqtuq.matuli_Kasuqatigiitsimajut(첫째) == 0 && atuqtuq.matuli_Kasuqatigiitsimajut(첫째) == -9;
        atuqtuq.titiraq(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
