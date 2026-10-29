// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lääʹddjânnam.JFinOS.호스트;

import java.util.HashMap;
import java.util.Map;
import Lääʹddjânnam.JFinOS.핵심.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String 내용) {
        직렬기록.append(내용);
        System.out.print(내용);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer 값 = 포트값.get(Integer.valueOf(포트번호));
        return 값 == null ? 0 : 값.intValue();
    }

    @Override
    public void 포트바이트쓰기(int 포트번호, int 값) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(값 & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // 호스트 시험에서는 다음 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

