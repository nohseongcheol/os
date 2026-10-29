// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int σύνολο_τιμή(int 끝) {
        int μέτρηση = 0;
        for (int Ευρετήριο = 1; Ευρετήριο <= 끝; Ευρετήριο++) μέτρηση += Ευρετήριο;
        return μέτρηση;
    }

    public static int Εκτέλεση_2() {
        int[] 값들 = new int[3];
        값들[0] = σύνολο_τιμή(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
