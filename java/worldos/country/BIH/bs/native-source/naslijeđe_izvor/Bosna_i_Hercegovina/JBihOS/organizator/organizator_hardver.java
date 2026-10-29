// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.organizator;

import java.util.HashMap;
import java.util.Map;
import Bosna_i_Hercegovina.JBihOS.jezgro.hardver_VALUE;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardver_VALUE 대역이다. */
public final class organizator_hardver implements hardver_VALUE {
    private final Map<Integer, Integer> hardver_port_VALUE = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Sadržaj_VALUE) {
        직렬기록.append(Sadržaj_VALUE);
        System.out.print(Sadržaj_VALUE);
    }

    @Override
    public int 포트바이트읽기(int hardver_broj_priključka) {
        Integer VALUE = hardver_port_VALUE.get(Integer.valueOf(hardver_broj_priključka));
        return VALUE == null ? 0 : VALUE.intValue();
    }

    @Override
    public void pisati_port_bajt(int hardver_broj_priključka, int VALUE) {
        hardver_port_VALUE.put(Integer.valueOf(hardver_broj_priključka), Integer.valueOf(VALUE & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // organizator 시험에서는 Dalje_stavka 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

