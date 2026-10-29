// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.येजमान;

import java.util.HashMap;
import java.util.Map;
import भारत.JIndOS.कर्नेल.हार्डवॅर_मोल;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 हार्डवॅर_मोल 대역이다. */
public final class येजमान_हार्डवॅर implements हार्डवॅर_मोल {
    private final Map<Integer, Integer> हार्डवॅर_पोर्ट_मोल = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String अनुक्रमणिका_मोल) {
        직렬기록.append(अनुक्रमणिका_मोल);
        System.out.print(अनुक्रमणिका_मोल);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer मोल = हार्डवॅर_पोर्ट_मोल.get(Integer.valueOf(포트번호));
        return मोल == null ? 0 : मोल.intValue();
    }

    @Override
    public void बरोवचें_पोर्ट_बायट(int 포트번호, int मोल) {
        हार्डवॅर_पोर्ट_मोल.put(Integer.valueOf(포트번호), Integer.valueOf(मोल & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // येजमान 시험에서는 फुडलें_आयटम 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

