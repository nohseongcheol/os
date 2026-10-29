// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class phépTính {
    static int giáTrịTổngCộng(int phầnKết) {
        int kếtQuả = 0;
        for (int sốHiệu = 1; sốHiệu <= phầnKết; sốHiệu++) kếtQuả += sốHiệu;
        return kếtQuả;
    }

    public static int chạy() {
        int[] cácGiáTrị = new int[3];
        cácGiáTrị[0] = giáTrịTổngCộng(10);
        cácGiáTrị[1] = -7 / 3;
        cácGiáTrị[2] = "한글".length();
        return cácGiáTrị[0] == 55 && cácGiáTrị[1] == -2 && cácGiáTrị[2] == 2 ? 0 : 1;
    }
}
