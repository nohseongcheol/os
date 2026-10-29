// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 수 있는 작은 Java položka_bod. */
public final class 문자명령 {
    public static void main(String[] Argumenty) {
        if (Argumenty.length != 1) {
            System.err.println("사용법: 문자명령 reťazec_VALUE");
            System.exit(2);
        }
        System.out.println(문자.bod_kódu_COUNT(Argumenty[0]));
    }
}
