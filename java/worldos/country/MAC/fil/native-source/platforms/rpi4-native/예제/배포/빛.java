// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] 인수) throws Exception {
        int SUM_VALUE = 0;
        int 수 = 1;
        while (수 <= 10) {
            SUM_VALUE = SUM_VALUE + 수;
            수 = 수 + 1;
        }
        한국어.자체.출력.수쓰기(SUM_VALUE);
        한국어.자체.file.sumulat("aot.txt", "한글 AOT file 😀");
        한국어.자체.출력.sumulat_linya(한국어.자체.file.읽기("aot.txt"));
    }
}
