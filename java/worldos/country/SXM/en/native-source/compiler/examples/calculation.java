// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class calculation {
    static int totalValue(int ending) {
        int result = 0;
        for (int index = 1; index <= ending; index++) result += index;
        return result;
    }

    public static int run() {
        int[] values = new int[3];
        values[0] = totalValue(10);
        values[1] = -7 / 3;
        values[2] = "한글".length();
        return values[0] == 55 && values[1] == -2 && values[2] == 2 ? 0 : 1;
    }
}
