// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.хост;

import java.util.HashMap;
import java.util.Map;
import Србија.JSrbOS.језгро.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String Садржај_вриједност) {
        직렬기록.append(Садржај_вриједност);
        System.out.print(Садржај_вриједност);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer вриједност = 포트값.get(Integer.valueOf(포트번호));
        return вриједност == null ? 0 : вриједност.intValue();
    }

    @Override
    public void писати_порт_бајт(int 포트번호, int вриједност) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(вриједност & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // хост 시험에서는 Даље_ставка 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

