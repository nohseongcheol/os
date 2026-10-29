// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int รวม_ค่า(int 끝) {
        int ผลลัพธ์ = 0;
        for (int ดัชนี = 1; ดัชนี <= 끝; ดัชนี++) ผลลัพธ์ += ดัชนี;
        return ผลลัพธ์;
    }

    public static int เรียกใช้งาน() {
        int[] 값들 = new int[3];
        값들[0] = รวม_ค่า(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
