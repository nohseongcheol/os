// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.హోస్ట్;

import java.util.HashMap;
import java.util.Map;
import భారతదేశం.JIndOS.కెర్నల్.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String విషయం_మూల్యం) {
        직렬기록.append(విషయం_మూల్యం);
        System.out.print(విషయం_మూల్యం);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer మూల్యం = 포트값.get(Integer.valueOf(포트번호));
        return మూల్యం == null ? 0 : మూల్యం.intValue();
    }

    @Override
    public void వ్రాయి_పోర్టు_బైట్(int 포트번호, int మూల్యం) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(మూల్యం & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // హోస్ట్ 시험에서는 తదుపరి_అంశం 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

