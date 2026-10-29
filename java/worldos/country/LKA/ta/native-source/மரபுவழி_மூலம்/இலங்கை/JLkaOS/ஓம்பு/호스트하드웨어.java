// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package இலங்கை.JLkaOS.ஓம்பு;

import java.util.HashMap;
import java.util.Map;
import இலங்கை.JLkaOS.கரு.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String உள்ளடக்கம்_மதிப்பு) {
        직렬기록.append(உள்ளடக்கம்_மதிப்பு);
        System.out.print(உள்ளடக்கம்_மதிப்பு);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer மதிப்பு = 포트값.get(Integer.valueOf(포트번호));
        return மதிப்பு == null ? 0 : மதிப்பு.intValue();
    }

    @Override
    public void எழுது_முணையம்_பைட்(int 포트번호, int மதிப்பு) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(மதிப்பு & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // ஓம்பு 시험에서는 அடுத்து_உருப்படி 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

