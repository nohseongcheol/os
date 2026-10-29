// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.värd;

import java.util.HashMap;
import java.util.Map;
import Danmark.JDnkOS.kärna.maskinvara_värde;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 maskinvara_värde 대역이다. */
public final class värd_maskinvara implements maskinvara_värde {
    private final Map<Integer, Integer> maskinvara_port_värde = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Innehåll_värde) {
        직렬기록.append(Innehåll_värde);
        System.out.print(Innehåll_värde);
    }

    @Override
    public int läsa_port_byte(int maskinvara_portnummer) {
        Integer värde = maskinvara_port_värde.get(Integer.valueOf(maskinvara_portnummer));
        return värde == null ? 0 : värde.intValue();
    }

    @Override
    public void skriva_port_byte(int maskinvara_portnummer, int värde) {
        maskinvara_port_värde.put(Integer.valueOf(maskinvara_portnummer), Integer.valueOf(värde & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // värd 시험에서는 Nästa_objekt 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

