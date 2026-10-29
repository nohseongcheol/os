// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] 인수) throws Exception {
        int 합 = 0;
        int 수 = 1;
        while (수 <= 10) {
            합 = 합 + 수;
            수 = 수 + 1;
        }
        한국어.자체.নিৰ্গম.수쓰기(합);
        한국어.자체.নথিপত্ৰ.লিখা("aot.txt", "한글 AOT নথিপত্ৰ 😀");
        한국어.자체.নিৰ্গম.লিখক_লাইন(한국어.자체.নথিপত্ৰ.পড়া("aot.txt"));
    }
}
