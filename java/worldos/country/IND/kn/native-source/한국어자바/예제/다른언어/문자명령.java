// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ಕನ್ನಡ.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 수 있는 작은 Java ನಮೂದು_ಬಿಂದು. */
public final class 문자명령 {
    public static void main(String[] 인수) {
        if (인수.length != 1) {
            System.err.println("사용법: 문자명령 ಸ್ಟ್ರಿಂಗ್_ಮೌಲ್ಯ");
            System.exit(2);
        }
        System.out.println(문자.코드포인트수(인수[0]));
    }
}
