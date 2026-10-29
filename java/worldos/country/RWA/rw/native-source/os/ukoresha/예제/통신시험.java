// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int ihuriro() {
        int 첫째 = ukoresha.kurema_Urusobemiyoboro(45000);
        if (첫째 < 0) { ukoresha.kwandika("NETWORK UNAVAILABLE\n"); return 3; }
        int[] amakurushingiro = new int[8];
        boolean 통과 = ukoresha.kurema_Urusobemiyoboro(45000) == -98
            && ukoresha.자료받기(첫째, amakurushingiro, 0) == -11
            && ukoresha.자료받기(첫째, amakurushingiro, 50) == -110
            && ukoresha.자료받기(첫째, amakurushingiro, 3000) == -22
            && ukoresha.kohereza_amakurushingiro(첫째, 0x0a000202, 9, amakurushingiro, 9) == -90
            && ukoresha.자료받기(첫째, null, 0) == -14
            && ukoresha.gufunga_Urusobemiyoboro(첫째) == 0 && ukoresha.gufunga_Urusobemiyoboro(첫째) == -9;
        ukoresha.kwandika(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
