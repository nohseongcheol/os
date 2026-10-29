// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Latviešu.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 numurs 있는 작은 Java ieejas_punkts. */
public final class 문자명령 {
    public static void main(String[] Parametri) {
        if (Parametri.length != 1) {
            System.err.println("사용법: 문자명령 virkne_VALUE");
            System.exit(2);
        }
        System.out.println(문자.koda_punkts_COUNT(Parametri[0]));
    }
}
