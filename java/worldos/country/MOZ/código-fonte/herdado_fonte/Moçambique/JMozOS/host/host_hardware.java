// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Moçambique.JMozOS.host;

import java.util.HashMap;
import java.util.Map;
import Moçambique.JMozOS.Núcleo.hardware_VALOR;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 hardware_VALOR 대역이다. */
public final class host_hardware implements hardware_VALOR {
    private final Map<Integer, Integer> hardware_porta_VALOR = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Conteúdo_VALOR) {
        직렬기록.append(Conteúdo_VALOR);
        System.out.print(Conteúdo_VALOR);
    }

    @Override
    public int leitura_porta_byte(int hardware_número_da_porta) {
        Integer VALOR = hardware_porta_VALOR.get(Integer.valueOf(hardware_número_da_porta));
        return VALOR == null ? 0 : VALOR.intValue();
    }

    @Override
    public void gravar_porta_byte(int hardware_número_da_porta, int VALOR) {
        hardware_porta_VALOR.put(Integer.valueOf(hardware_número_da_porta), Integer.valueOf(VALOR & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // host 시험에서는 Avançar_item 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

