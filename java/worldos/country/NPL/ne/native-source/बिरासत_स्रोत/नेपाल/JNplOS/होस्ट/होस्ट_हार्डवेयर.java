// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.होस्ट;

import java.util.HashMap;
import java.util.Map;
import नेपाल.JNplOS.कर्णेल.हार्डवेयर_मान;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 हार्डवेयर_मान 대역이다. */
public final class होस्ट_हार्डवेयर implements हार्डवेयर_मान {
    private final Map<Integer, Integer> हार्डवेयर_पोर्ट_मान = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String सामग्री_मान) {
        직렬기록.append(सामग्री_मान);
        System.out.print(सामग्री_मान);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer मान = हार्डवेयर_पोर्ट_मान.get(Integer.valueOf(포트번호));
        return मान == null ? 0 : मान.intValue();
    }

    @Override
    public void लेख्नुहोस्_पोर्ट_बाइट(int 포트번호, int मान) {
        हार्डवेयर_पोर्ट_मान.put(Integer.valueOf(포트번호), Integer.valueOf(मान & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // होस्ट 시험에서는 अर्को_वस्तु 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

