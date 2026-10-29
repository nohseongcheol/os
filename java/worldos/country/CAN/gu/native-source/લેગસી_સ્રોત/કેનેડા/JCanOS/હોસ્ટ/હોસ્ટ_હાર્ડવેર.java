// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેનેડા.JCanOS.હોસ્ટ;

import java.util.HashMap;
import java.util.Map;
import કેનેડા.JCanOS.કર્નેલ.હાર્ડવેર_મૂલ્ય;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 હાર્ડવેર_મૂલ્ય 대역이다. */
public final class હોસ્ટ_હાર્ડવેર implements હાર્ડવેર_મૂલ્ય {
    private final Map<Integer, Integer> હાર્ડવેર_પૉર્ટ_મૂલ્ય = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String સામગ્રી_મૂલ્ય) {
        직렬기록.append(સામગ્રી_મૂલ્ય);
        System.out.print(સામગ્રી_મૂલ્ય);
    }

    @Override
    public int 포트바이트읽기(int હાર્ડવેર_પોર્ટ_નંબર) {
        Integer મૂલ્ય = હાર્ડવેર_પૉર્ટ_મૂલ્ય.get(Integer.valueOf(હાર્ડવેર_પોર્ટ_નંબર));
        return મૂલ્ય == null ? 0 : મૂલ્ય.intValue();
    }

    @Override
    public void લખો_પૉર્ટ_બાઇટ(int હાર્ડવેર_પોર્ટ_નંબર, int મૂલ્ય) {
        હાર્ડવેર_પૉર્ટ_મૂલ્ય.put(Integer.valueOf(હાર્ડવેર_પોર્ટ_નંબર), Integer.valueOf(મૂલ્ય & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // હોસ્ટ 시험에서는 આગલું_આઇટમ 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

