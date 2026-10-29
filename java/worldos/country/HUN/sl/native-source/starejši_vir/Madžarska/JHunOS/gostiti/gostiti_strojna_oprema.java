// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Madžarska.JHunOS.gostiti;

import java.util.HashMap;
import java.util.Map;
import Madžarska.JHunOS.jedro.strojna_oprema_VALUE;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 strojna_oprema_VALUE 대역이다. */
public final class gostiti_strojna_oprema implements strojna_oprema_VALUE {
    private final Map<Integer, Integer> strojna_oprema_vrata_VALUE = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String vsebina_VALUE) {
        직렬기록.append(vsebina_VALUE);
        System.out.print(vsebina_VALUE);
    }

    @Override
    public int 포트바이트읽기(int strojna_oprema_številka_vrat) {
        Integer VALUE = strojna_oprema_vrata_VALUE.get(Integer.valueOf(strojna_oprema_številka_vrat));
        return VALUE == null ? 0 : VALUE.intValue();
    }

    @Override
    public void pisati_vrata_bajt(int strojna_oprema_številka_vrat, int VALUE) {
        strojna_oprema_vrata_VALUE.put(Integer.valueOf(strojna_oprema_številka_vrat), Integer.valueOf(VALUE & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // gostiti 시험에서는 Naprej_element 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

