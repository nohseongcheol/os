// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.Ostalari;

import java.util.HashMap;
import java.util.Map;
import Espainia.JEspOS.nukleo.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String eduki_balio) {
        직렬기록.append(eduki_balio);
        System.out.print(eduki_balio);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer balio = 포트값.get(Integer.valueOf(포트번호));
        return balio == null ? 0 : balio.intValue();
    }

    @Override
    public void idatzi_ataka_byte(int 포트번호, int balio) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(balio & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // Ostalari 시험에서는 Hurrengoa_elementu 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

