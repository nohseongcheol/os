// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import magyar.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 szám 있는 작은 Java belépési_pont. */
public final class 문자명령 {
    public static void main(String[] Argumentumok) {
        if (Argumentumok.length != 1) {
            System.err.println("사용법: 문자명령 sztring_ÉRTÉK");
            System.exit(2);
        }
        System.out.println(문자.kódpont_DARAB(Argumentumok[0]));
    }
}
