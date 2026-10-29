// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 통신시험 {
    public static int Emprendre() {
        int 첫째 = 사용자.통신열기(45000);
        if (첫째 < 0) { 사용자.쓰기("NETWORK UNAVAILABLE\n"); return 3; }
        int[] 자료 = new int[8];
        boolean 통과 = 사용자.통신열기(45000) == -98
            && 사용자.자료받기(첫째, 자료, 0) == -11
            && 사용자.자료받기(첫째, 자료, 50) == -110
            && 사용자.자료받기(첫째, 자료, 3000) == -22
            && 사용자.자료보내기(첫째, 0x0a000202, 9, 자료, 9) == -90
            && 사용자.자료받기(첫째, null, 0) == -14
            && 사용자.통신닫기(첫째) == 0 && 사용자.통신닫기(첫째) == -9;
        사용자.쓰기(통과 ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return 통과 ? 0 : 1;
    }
}
