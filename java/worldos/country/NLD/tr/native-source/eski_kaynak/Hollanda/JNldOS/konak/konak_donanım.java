// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hollanda.JNldOS.konak;

import java.util.HashMap;
import java.util.Map;
import Hollanda.JNldOS.Çekirdek.donanım_değer;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 donanım_değer 대역이다. */
public final class konak_donanım implements donanım_değer {
    private final Map<Integer, Integer> donanım_taşımak_değer = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String içerik_değer) {
        직렬기록.append(içerik_değer);
        System.out.print(içerik_değer);
    }

    @Override
    public int 포트바이트읽기(int donanım_bağlantı_noktası_numarası) {
        Integer değer = donanım_taşımak_değer.get(Integer.valueOf(donanım_bağlantı_noktası_numarası));
        return değer == null ? 0 : değer.intValue();
    }

    @Override
    public void yazma_taşımak_bayt(int donanım_bağlantı_noktası_numarası, int değer) {
        donanım_taşımak_değer.put(Integer.valueOf(donanım_bağlantı_noktası_numarası), Integer.valueOf(değer & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // konak 시험에서는 Sonraki_öğe 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

