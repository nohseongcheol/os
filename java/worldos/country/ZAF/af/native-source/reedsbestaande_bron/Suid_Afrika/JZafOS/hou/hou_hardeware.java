// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Suid_Afrika.JZafOS.hou;

import java.util.HashMap;
import java.util.Map;
import Suid_Afrika.JZafOS.kern.hardeware_VALUE;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardeware_VALUE 대역이다. */
public final class hou_hardeware implements hardeware_VALUE {
    private final Map<Integer, Integer> hardeware_ombou_VALUE = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Inhoud_VALUE) {
        직렬기록.append(Inhoud_VALUE);
        System.out.print(Inhoud_VALUE);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer VALUE = hardeware_ombou_VALUE.get(Integer.valueOf(포트번호));
        return VALUE == null ? 0 : VALUE.intValue();
    }

    @Override
    public void skryf_ombou_greep(int 포트번호, int VALUE) {
        hardeware_ombou_VALUE.put(Integer.valueOf(포트번호), Integer.valueOf(VALUE & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // hou 시험에서는 Volgende_item 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

