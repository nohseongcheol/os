// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.vert;

import java.util.HashMap;
import java.util.Map;
import Svalbard_og_Jan_Mayen.JSjmOS.kjerne.maskinvare_VERDI;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 maskinvare_VERDI 대역이다. */
public final class vert_maskinvare implements maskinvare_VERDI {
    private final Map<Integer, Integer> maskinvare_port_VERDI = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Innhold_VERDI) {
        직렬기록.append(Innhold_VERDI);
        System.out.print(Innhold_VERDI);
    }

    @Override
    public int 포트바이트읽기(int maskinvare_portnummer) {
        Integer VERDI = maskinvare_port_VERDI.get(Integer.valueOf(maskinvare_portnummer));
        return VERDI == null ? 0 : VERDI.intValue();
    }

    @Override
    public void skrive_port_byte(int maskinvare_portnummer, int VERDI) {
        maskinvare_port_VERDI.put(Integer.valueOf(maskinvare_portnummer), Integer.valueOf(VERDI & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // vert 시험에서는 Neste_vare 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

