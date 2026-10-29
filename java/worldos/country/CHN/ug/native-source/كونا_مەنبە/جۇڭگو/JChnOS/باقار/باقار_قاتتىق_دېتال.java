// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package جۇڭگو.JChnOS.باقار;

import java.util.HashMap;
import java.util.Map;
import جۇڭگو.JChnOS.يادرو.قاتتىق_دېتال_قىممىتى;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 قاتتىق_دېتال_قىممىتى 대역이다. */
public final class باقار_قاتتىق_دېتال implements قاتتىق_دېتال_قىممىتى {
    private final Map<Integer, Integer> قاتتىق_دېتال_ئېغىز_قىممىتى = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String مەزمۇن_قىممىتى) {
        직렬기록.append(مەزمۇن_قىممىتى);
        System.out.print(مەزمۇن_قىممىتى);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer قىممىتى = قاتتىق_دېتال_ئېغىز_قىممىتى.get(Integer.valueOf(포트번호));
        return قىممىتى == null ? 0 : قىممىتى.intValue();
    }

    @Override
    public void يازماق_ئېغىز_بايت(int 포트번호, int قىممىتى) {
        قاتتىق_دېتال_ئېغىز_قىممىتى.put(Integer.valueOf(포트번호), Integer.valueOf(قىممىتى & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // باقار 시험에서는 كېيىنكى_تۈر 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

