// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import polski.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 identyfikator 있는 작은 Java punkt_wejścia. */
public final class 문자명령 {
    public static void main(String[] argumenty) {
        if (argumenty.length != 1) {
            System.err.println("사용법: 문자명령 ciąg_WARTOŚĆ");
            System.exit(2);
        }
        System.out.println(문자.kod_znaku_ILE_LICZB(argumenty[0]));
    }
}
