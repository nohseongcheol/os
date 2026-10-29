// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಹೋಸ್ಟ್;

import java.util.HashMap;
import java.util.Map;
import ಭಾರತ.JIndOS.ಕರ್ನಲ್.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String ವಿಷಯ_ಮೌಲ್ಯ) {
        직렬기록.append(ವಿಷಯ_ಮೌಲ್ಯ);
        System.out.print(ವಿಷಯ_ಮೌಲ್ಯ);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer ಮೌಲ್ಯ = 포트값.get(Integer.valueOf(포트번호));
        return ಮೌಲ್ಯ == null ? 0 : ಮೌಲ್ಯ.intValue();
    }

    @Override
    public void ಬರೆ_ಪೋರ್ಟ್_ಬೈಟ್(int 포트번호, int ಮೌಲ್ಯ) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(ಮೌಲ್ಯ & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // ಹೋಸ್ಟ್ 시험에서는 ಮುಂದೆ_ಅಂಶ 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

