// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] Argumentoj) throws Exception {
        int 합 = 0;
        int 수 = 1;
        while (수 <= 10) {
            합 = 합 + 수;
            수 = 수 + 1;
        }
        한국어.자체.Eligo.수쓰기(합);
        한국어.자체.Dosiero.Skribo("aot.txt", "한글 AOT Dosiero 😀");
        한국어.자체.Eligo.줄쓰기(한국어.자체.Dosiero.Lego("aot.txt"));
    }
}
