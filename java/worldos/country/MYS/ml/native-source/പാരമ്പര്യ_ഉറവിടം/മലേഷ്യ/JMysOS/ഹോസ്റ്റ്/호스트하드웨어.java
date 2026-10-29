// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package മലേഷ്യ.JMysOS.ഹോസ്റ്റ്;

import java.util.HashMap;
import java.util.Map;
import മലേഷ്യ.JMysOS.കെര്_ണല്.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String ഉള്ളടക്കം_മൂല്യം) {
        직렬기록.append(ഉള്ളടക്കം_മൂല്യം);
        System.out.print(ഉള്ളടക്കം_മൂല്യം);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer മൂല്യം = 포트값.get(Integer.valueOf(포트번호));
        return മൂല്യം == null ? 0 : മൂല്യം.intValue();
    }

    @Override
    public void റൈറ്റ്_ചെയ്യുക_പോര്_ട്ട്_బైట్(int 포트번호, int മൂല്യം) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(മൂല്യം & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // ഹോസ്റ്റ് 시험에서는 അടുത്തത്_ഇനം 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

