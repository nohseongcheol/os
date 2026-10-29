// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 계산 {
    static int إجمالي_قيمة(int 끝) {
        int نتيجة = 0;
        for (int فهرس = 1; فهرس <= 끝; فهرس++) نتيجة += فهرس;
        return نتيجة;
    }

    public static int تشغيل() {
        int[] 값들 = new int[3];
        값들[0] = إجمالي_قيمة(10);
        값들[1] = -7 / 3;
        값들[2] = "한글".length();
        return 값들[0] == 55 && 값들[1] == -2 && 값들[2] == 2 ? 0 : 1;
    }
}
