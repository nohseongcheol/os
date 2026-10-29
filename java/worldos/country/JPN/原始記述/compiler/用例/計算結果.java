// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 計算結果 {
    static int 合計値(int 終端) {
        int 結果 = 0;
        for (int 番号 = 1; 番号 <= 終端; 番号++) 結果 += 番号;
        return 結果;
    }

    public static int 起動処理() {
        int[] 値一覧 = new int[3];
        値一覧[0] = 合計値(10);
        値一覧[1] = -7 / 3;
        値一覧[2] = "한글".length();
        return 値一覧[0] == 55 && 値一覧[1] == -2 && 値一覧[2] == 2 ? 0 : 1;
    }
}
