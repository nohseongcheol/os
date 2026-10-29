// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Nederlands.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 nummer 있는 작은 Java beginpunt. */
public final class 문자명령 {
    public static void main(String[] argumenten) {
        if (argumenten.length != 1) {
            System.err.println("사용법: 문자명령 tekenreeks_WAARDE");
            System.exit(2);
        }
        System.out.println(문자.codepoint_AANTAL(argumenten[0]));
    }
}
