// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેનેડા.JCanOS.કર્નેલ;

import કેનેડા.JCanOS.기억공간.મેમરી_પ્રબંધક;
import કેનેડા.JCanOS.기억공간.પેજ_પ્રબંધક;
import કેનેડા.JCanOS.입력.입력관리자;
import કેનેડા.JCanOS.작업.પ્રક્રિયા_મૂલ્ય;
import કેનેડા.JCanOS.작업.શેડ્યૂલર;
import કેનેડા.JCanOS.체계호출.체계호출;
import કેનેડા.JCanOS.ફાઇલ_સિસ્ટમ.파일서술자표;
import કેનેડા.JCanOS.ફાઇલ_સિસ્ટમ.ફાઇલ_સિસ્ટમ;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class કર્નેલ {
    private final હાર્ડવેર_મૂલ્ય ડિવાઇસ_મૂલ્ય;
    private final મેમરી_પ્રબંધક 기억공간 = new મેમરી_પ્રબંધક(32 * 1024 * 1024);
    private final પેજ_પ્રબંધક 쪽관리 = new પેજ_પ્રબંધક();
    private final ફાઇલ_સિસ્ટમ ફાઇલ_સિસ્ટમ = new ફાઇલ_સિસ્ટમ();
    private final શેડ્યૂલર શેડ્યૂલર = new શેડ્યૂલર(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final પ્રક્રિયા_મૂલ્ય 첫과정;
    private final 체계호출 체계호출;

    public કર્નેલ(હાર્ડવેર_મૂલ્ય ડિવાઇસ_મૂલ્ય) {
        this.ડિવાઇસ_મૂલ્ય = ડિવાઇસ_મૂલ્ય;
        첫과정 = શેડ્યૂલર.첫과정(new 파일서술자표(ફાઇલ_સિસ્ટમ));
        체계호출 = new 체계호출(ફાઇલ_સિસ્ટમ, 쪽관리, શેડ્યૂલર, ડિવાઇસ_મૂલ્ય, 입력관리);
    }

    public void ચલાવો_2() {
        ડિવાઇસ_મૂલ્ય.직렬출력("=== JCanOS 관리 કર્નેલ_મૂલ્ય ===\n");
    }

    public void 한단계실행() {
        ડિવાઇસ_મૂલ્ય.중앙처리장치멈춤();
    }

    public મેમરી_પ્રબંધક 기억공간() {
        return 기억공간;
    }

    public પેજ_પ્રબંધક 쪽관리() {
        return 쪽관리;
    }

    public ફાઇલ_સિસ્ટમ ફાઇલ_સિસ્ટમ() {
        return ફાઇલ_સિસ્ટમ;
    }

    public શેડ્યૂલર શેડ્યૂલર() {
        return શેડ્યૂલર;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public પ્રક્રિયા_મૂલ્ય 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
