// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import українська.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 수 있는 작은 Java запис_бал. */
public final class 문자명령 {
    public static void main(String[] аргументи) {
        if (аргументи.length != 1) {
            System.err.println("사용법: 문자명령 рядок_значення");
            System.exit(2);
        }
        System.out.println(문자.코드포인트수(аргументи[0]));
    }
}
