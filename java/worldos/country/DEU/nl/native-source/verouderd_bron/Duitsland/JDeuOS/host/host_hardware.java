// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Duitsland.JDeuOS.host;

import java.util.HashMap;
import java.util.Map;
import Duitsland.JDeuOS.Kern.hardware_WAARDE;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardware_WAARDE 대역이다. */
public final class host_hardware implements hardware_WAARDE {
    private final Map<Integer, Integer> hardware_poort_WAARDE = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Inhoud_WAARDE) {
        직렬기록.append(Inhoud_WAARDE);
        System.out.print(Inhoud_WAARDE);
    }

    @Override
    public int 포트바이트읽기(int hardware_poortnummer) {
        Integer WAARDE = hardware_poort_WAARDE.get(Integer.valueOf(hardware_poortnummer));
        return WAARDE == null ? 0 : WAARDE.intValue();
    }

    @Override
    public void schrijven_poort_byte(int hardware_poortnummer, int WAARDE) {
        hardware_poort_WAARDE.put(Integer.valueOf(hardware_poortnummer), Integer.valueOf(WAARDE & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // host 시험에서는 Volgende_item 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

