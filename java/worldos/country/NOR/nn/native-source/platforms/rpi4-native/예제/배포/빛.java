// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argument) throws Exception {
        int SUM_VALUE = 0;
        int 수 = 1;
        while (수 <= 10) {
            SUM_VALUE = SUM_VALUE + 수;
            수 = 수 + 1;
        }
        한국어.자체.Utdata.수쓰기(SUM_VALUE);
        한국어.자체.Fil.Skriv("aot.txt", "한글 AOT Fil 😀");
        한국어.자체.Utdata.skrive_line(한국어.자체.Fil.Les("aot.txt"));
    }
}
