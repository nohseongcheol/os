// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.hostiteľ;

import java.util.HashMap;
import java.util.Map;
import Česko.JCzeOS.jadro.hardvér_VALUE;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardvér_VALUE 대역이다. */
public final class hostiteľ_hardvér implements hardvér_VALUE {
    private final Map<Integer, Integer> hardvér_port_VALUE = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String obsah_VALUE) {
        직렬기록.append(obsah_VALUE);
        System.out.print(obsah_VALUE);
    }

    @Override
    public int 포트바이트읽기(int hardvér_číslo_portu) {
        Integer VALUE = hardvér_port_VALUE.get(Integer.valueOf(hardvér_číslo_portu));
        return VALUE == null ? 0 : VALUE.intValue();
    }

    @Override
    public void zapísať_port_Byte(int hardvér_číslo_portu, int VALUE) {
        hardvér_port_VALUE.put(Integer.valueOf(hardvér_číslo_portu), Integer.valueOf(VALUE & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // hostiteľ 시험에서는 Ďalej_položka 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

