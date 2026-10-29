// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import বাংলা.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 수 있는 작은 Java ভুক্তি_বিন্দু. */
public final class 문자명령 {
    public static void main(String[] আর্গুমেন্ট_তালিকা) {
        if (আর্গুমেন্ট_তালিকা.length != 1) {
            System.err.println("사용법: 문자명령 স্ট্রিং_মান");
            System.exit(2);
        }
        System.out.println(문자.코드포인트수(আর্গুমেন্ট_তালিকা[0]));
    }
}
