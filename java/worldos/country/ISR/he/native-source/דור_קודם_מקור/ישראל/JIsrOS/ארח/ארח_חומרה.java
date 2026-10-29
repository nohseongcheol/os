// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ישראל.JIsrOS.ארח;

import java.util.HashMap;
import java.util.Map;
import ישראל.JIsrOS.ליבה.חומרה_ערך_9591fb0a;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 חומרה_ערך_9591fb0a 대역이다. */
public final class ארח_חומרה implements חומרה_ערך_9591fb0a {
    private final Map<Integer, Integer> חומרה_הסב_ערך = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String תוכן_ערך) {
        직렬기록.append(תוכן_ערך);
        System.out.print(תוכן_ערך);
    }

    @Override
    public int 포트바이트읽기(int חומרה_מספר_יציאה) {
        Integer ערך = חומרה_הסב_ערך.get(Integer.valueOf(חומרה_מספר_יציאה));
        return ערך == null ? 0 : ערך.intValue();
    }

    @Override
    public void כתיבה_הסב_בית(int חומרה_מספר_יציאה, int ערך) {
        חומרה_הסב_ערך.put(Integer.valueOf(חומרה_מספר_יציאה), Integer.valueOf(ערך & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // ארח 시험에서는 הבא_פריט 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

