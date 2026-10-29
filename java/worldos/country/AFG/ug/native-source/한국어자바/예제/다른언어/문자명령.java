// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 수 있는 작은 Java كىرگۈزۈش_نوقتا. */
public final class 문자명령 {
    public static void main(String[] ئۆزگەرگۈچىلەر) {
        if (ئۆزگەرگۈچىلەر.length != 1) {
            System.err.println("사용법: 문자명령 ھەرپ_تىزمىسى_قىممىتى");
            System.exit(2);
        }
        System.out.println(문자.코드포인트수(ئۆزگەرگۈچىلەر[0]));
    }
}
