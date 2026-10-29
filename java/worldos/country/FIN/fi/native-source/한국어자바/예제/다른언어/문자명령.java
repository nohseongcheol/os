// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import suomi.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 numero 있는 작은 Java aloituskohta. */
public final class 문자명령 {
    public static void main(String[] argumentit) {
        if (argumentit.length != 1) {
            System.err.println("사용법: 문자명령 merkkijono_ARVO");
            System.exit(2);
        }
        System.out.println(문자.koodipiste_LASKE(argumentit[0]));
    }
}
