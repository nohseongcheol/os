// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Íslenska.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 númer 있는 작은 Java færsla_P. */
public final class 문자명령 {
    public static void main(String[] Viðföng) {
        if (Viðföng.length != 1) {
            System.err.println("사용법: 문자명령 strengur_VALUE");
            System.exit(2);
        }
        System.out.println(문자.stafkóði_COUNT(Viðföng[0]));
    }
}
