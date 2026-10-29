// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Jungtinė_Karalystė.JGbrOS.organizuoti;

import java.util.HashMap;
import java.util.Map;
import Jungtinė_Karalystė.JGbrOS.branduolys.aparatūra_VALUE;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 aparatūra_VALUE 대역이다. */
public final class organizuoti_aparatūra implements aparatūra_VALUE {
    private final Map<Integer, Integer> aparatūra_jungtis_VALUE = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Turinys_VALUE) {
        직렬기록.append(Turinys_VALUE);
        System.out.print(Turinys_VALUE);
    }

    @Override
    public int 포트바이트읽기(int aparatūra_prievado_numeris) {
        Integer VALUE = aparatūra_jungtis_VALUE.get(Integer.valueOf(aparatūra_prievado_numeris));
        return VALUE == null ? 0 : VALUE.intValue();
    }

    @Override
    public void rašymas_jungtis_baitas(int aparatūra_prievado_numeris, int VALUE) {
        aparatūra_jungtis_VALUE.put(Integer.valueOf(aparatūra_prievado_numeris), Integer.valueOf(VALUE & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // organizuoti 시험에서는 toliau_prekė 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

