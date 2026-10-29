// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 수 있는 작은 Java oppføring_p. */
public final class 문자명령 {
    public static void main(String[] Argument) {
        if (Argument.length != 1) {
            System.err.println("사용법: 문자명령 streng_VALUE");
            System.exit(2);
        }
        System.out.println(문자.teiknkode_COUNT(Argument[0]));
    }
}
