// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украіна.JUkrOS.вузел;

import java.util.HashMap;
import java.util.Map;
import Украіна.JUkrOS.ядро.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String кантэнт_значэнне) {
        직렬기록.append(кантэнт_значэнне);
        System.out.print(кантэнт_значэнне);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer значэнне = 포트값.get(Integer.valueOf(포트번호));
        return значэнне == null ? 0 : значэнне.intValue();
    }

    @Override
    public void напісаць_порт_байт(int 포트번호, int значэнне) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(значэнне & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // вузел 시험에서는 다음 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

