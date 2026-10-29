// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] 인수) throws Exception {
        int 합 = 0;
        int 수 = 1;
        while (수 <= 10) {
            합 = 합 + 수;
            수 = 수 + 1;
        }
        한국어.자체.출력.수쓰기(합);
        한국어.자체.טעקע.쓰기("aot.txt", "한글 AOT טעקע 😀");
        한국어.자체.출력.줄쓰기(한국어.자체.טעקע.읽기("aot.txt"));
    }
}
