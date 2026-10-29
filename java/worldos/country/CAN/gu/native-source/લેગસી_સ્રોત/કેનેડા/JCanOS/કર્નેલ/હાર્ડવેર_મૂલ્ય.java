// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેનેડા.JCanOS.કર્નેલ;

/** Java 관리 커널과 CPU 고유 코드 사이의 유일한 경계다. */
public interface હાર્ડવેર_મૂલ્ય {
    void 직렬출력(String સામગ્રી_મૂલ્ય);

    int 포트바이트읽기(int હાર્ડવેર_પોર્ટ_નંબર);

    void લખો_પૉર્ટ_બાઇટ(int હાર્ડવેર_પોર્ટ_નંબર, int મૂલ્ય);

    void 중앙처리장치멈춤();
}

