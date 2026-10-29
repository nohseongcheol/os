// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.आयोजक;

import java.util.HashMap;
import java.util.Map;
import नेपाल.JNplOS.कर्नेल.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String सामग्री_मान) {
        직렬기록.append(सामग्री_मान);
        System.out.print(सामग्री_मान);
    }

    @Override
    public int पढें_पोर्ट_बाइट(int 포트번호) {
        Integer मान = 포트값.get(Integer.valueOf(포트번호));
        return मान == null ? 0 : मान.intValue();
    }

    @Override
    public void लिखना_पोर्ट_बाइट(int 포트번호, int मान) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(मान & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // आयोजक 시험에서는 अगला_आइटम 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

