// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.dalal;

import java.util.HashMap;
import java.util.Map;
import Senegaal.JSenOS.xoox.jumtukaay_xëyma;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 jumtukaay_xëyma 대역이다. */
public final class dalal_jumtukaay implements jumtukaay_xëyma {
    private final Map<Integer, Integer> jumtukaay_jël_xëyma = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Këmb_xëyma) {
        직렬기록.append(Këmb_xëyma);
        System.out.print(Këmb_xëyma);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer xëyma = jumtukaay_jël_xëyma.get(Integer.valueOf(포트번호));
        return xëyma == null ? 0 : xëyma.intValue();
    }

    @Override
    public void biir_jël_okte(int 포트번호, int xëyma) {
        jumtukaay_jël_xëyma.put(Integer.valueOf(포트번호), Integer.valueOf(xëyma & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // dalal 시험에서는 다음 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

