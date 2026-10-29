// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import ગુજરાતી.자바.문자;

/** 다른 언어가 표준 출력으로 결과를 받을 수 있는 작은 Java પ્રવેશ_બિંદુ. */
public final class 문자명령 {
    public static void main(String[] દલીલો) {
        if (દલીલો.length != 1) {
            System.err.println("사용법: 문자명령 સ્ટ્રિંગ_મૂલ્ય");
            System.exit(2);
        }
        System.out.println(문자.코드포인트수(દલીલો[0]));
    }
}
