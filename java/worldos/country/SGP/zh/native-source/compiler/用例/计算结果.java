// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 计算结果 {
    static int 总计值(int 结尾) {
        int 结果 = 0;
        for (int 编号 = 1; 编号 <= 结尾; 编号++) 结果 += 编号;
        return 结果;
    }

    public static int 运行() {
        int[] 值列 = new int[3];
        值列[0] = 总计值(10);
        值列[1] = -7 / 3;
        值列[2] = "한글".length();
        return 值列[0] == 55 && 值列[1] == -2 && 值列[2] == 2 ? 0 : 1;
    }
}
