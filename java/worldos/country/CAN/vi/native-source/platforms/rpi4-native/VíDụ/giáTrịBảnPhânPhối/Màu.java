// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class Màu {
    public static void main(String[] cácĐốiSố) throws Exception {
        int giáTrịTổng = 0;
        int trịSố = 1;
        while (trịSố <= 10) {
            giáTrịTổng = giáTrịTổng + trịSố;
            trịSố = trịSố + 1;
        }
        tiếngViệt.tựThân.ĐầuRa.ghiSố(giáTrịTổng);
        tiếngViệt.tựThân.Tệp.ghi("aot.txt", "한글 AOT Tệp 😀");
        tiếngViệt.tựThân.ĐầuRa.ghiDòng(tiếngViệt.tựThân.Tệp.đọc("aot.txt"));
    }
}
