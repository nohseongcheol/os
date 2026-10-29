// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Magyarország.JHunOS.gazda;

import java.util.HashMap;
import java.util.Map;
import Magyarország.JHunOS.kernel.hardver_ÉRTÉK;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardver_ÉRTÉK 대역이다. */
public final class gazda_hardver implements hardver_ÉRTÉK {
    private final Map<Integer, Integer> hardver_port_ÉRTÉK = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Tartalom_ÉRTÉK) {
        직렬기록.append(Tartalom_ÉRTÉK);
        System.out.print(Tartalom_ÉRTÉK);
    }

    @Override
    public int 포트바이트읽기(int hardver_portszám) {
        Integer ÉRTÉK = hardver_port_ÉRTÉK.get(Integer.valueOf(hardver_portszám));
        return ÉRTÉK == null ? 0 : ÉRTÉK.intValue();
    }

    @Override
    public void ír_port_bájt(int hardver_portszám, int ÉRTÉK) {
        hardver_port_ÉRTÉK.put(Integer.valueOf(hardver_portszám), Integer.valueOf(ÉRTÉK & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // gazda 시험에서는 Tovább_cikk 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

