// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.vært;

import java.util.HashMap;
import java.util.Map;
import Danmark.JDnkOS.kerne.hardware_VÆRDI;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardware_VÆRDI 대역이다. */
public final class vært_hardware implements hardware_VÆRDI {
    private final Map<Integer, Integer> hardware_port_VÆRDI = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Indhold_VÆRDI) {
        직렬기록.append(Indhold_VÆRDI);
        System.out.print(Indhold_VÆRDI);
    }

    @Override
    public int 포트바이트읽기(int hardware_portnummer) {
        Integer VÆRDI = hardware_port_VÆRDI.get(Integer.valueOf(hardware_portnummer));
        return VÆRDI == null ? 0 : VÆRDI.intValue();
    }

    @Override
    public void skrive_port_byte(int hardware_portnummer, int VÆRDI) {
        hardware_port_VÆRDI.put(Integer.valueOf(hardware_portnummer), Integer.valueOf(VÆRDI & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // vært 시험에서는 Næste_vare 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

