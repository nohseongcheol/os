// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int toplam_değer(int 끝) {
        int sonuç = 0;
        for (int Dizin = 1; Dizin <= 끝; Dizin++) sonuç += Dizin;
        return sonuç;
    }

    public static int çalıştır() {
        int[] 값들 = new int[3];
        값들[0] = toplam_değer(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
