// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Australia.JAusOS.host;

import java.util.HashMap;
import java.util.Map;
import Australia.JAusOS.Nucleo.hardware_VALORE;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardware_VALORE 대역이다. */
public final class host_hardware implements hardware_VALORE {
    private final Map<Integer, Integer> hardware_porta_VALORE = new HashMap<Integer, Integer>();
    private final StringBuilder seriale_LOG = new StringBuilder();

    @Override
    public void seriale_output(String Contenuto_VALORE) {
        seriale_LOG.append(Contenuto_VALORE);
        System.out.print(Contenuto_VALORE);
    }

    @Override
    public int 포트바이트읽기(int hardware_numero_di_porta) {
        Integer VALORE = hardware_porta_VALORE.get(Integer.valueOf(hardware_numero_di_porta));
        return VALORE == null ? 0 : VALORE.intValue();
    }

    @Override
    public void scrivere_porta_byte(int hardware_numero_di_porta, int VALORE) {
        hardware_porta_VALORE.put(Integer.valueOf(hardware_numero_di_porta), Integer.valueOf(VALORE & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // host 시험에서는 Avanti_articolo 사건을 기다리지 않고 즉시 반환한다.
    }

    public String seriale_LOG() {
        return seriale_LOG.toString();
    }
}

