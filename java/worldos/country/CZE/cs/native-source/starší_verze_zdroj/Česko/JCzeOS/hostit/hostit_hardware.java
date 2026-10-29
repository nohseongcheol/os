// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Česko.JCzeOS.hostit;

import java.util.HashMap;
import java.util.Map;
import Česko.JCzeOS.jádro.hardware_HODNOTA;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardware_HODNOTA 대역이다. */
public final class hostit_hardware implements hardware_HODNOTA {
    private final Map<Integer, Integer> hardware_port_HODNOTA = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Obsah_HODNOTA) {
        직렬기록.append(Obsah_HODNOTA);
        System.out.print(Obsah_HODNOTA);
    }

    @Override
    public int 포트바이트읽기(int hardware_číslo_portu) {
        Integer HODNOTA = hardware_port_HODNOTA.get(Integer.valueOf(hardware_číslo_portu));
        return HODNOTA == null ? 0 : HODNOTA.intValue();
    }

    @Override
    public void zápis_port_bajt(int hardware_číslo_portu, int HODNOTA) {
        hardware_port_HODNOTA.put(Integer.valueOf(hardware_číslo_portu), Integer.valueOf(HODNOTA & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // hostit 시험에서는 Další_zboží 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

