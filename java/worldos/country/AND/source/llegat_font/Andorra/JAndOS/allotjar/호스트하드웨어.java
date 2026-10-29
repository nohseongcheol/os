// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Andorra.JAndOS.allotjar;

import java.util.HashMap;
import java.util.Map;
import Andorra.JAndOS.nucli.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String contingut_VALOR) {
        직렬기록.append(contingut_VALOR);
        System.out.print(contingut_VALOR);
    }

    @Override
    public int tancar_port_byte(int 포트번호) {
        Integer VALOR = 포트값.get(Integer.valueOf(포트번호));
        return VALOR == null ? 0 : VALOR.intValue();
    }

    @Override
    public void escriure_port_byte(int 포트번호, int VALOR) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(VALOR & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // allotjar 시험에서는 Següent_element 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

