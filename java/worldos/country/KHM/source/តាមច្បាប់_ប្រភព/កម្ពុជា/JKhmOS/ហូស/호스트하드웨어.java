// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ហូស;

import java.util.HashMap;
import java.util.Map;
import កម្ពុជា.JKhmOS.ខឺណេល.하드웨어;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 하드웨어 대역이다. */
public final class 호스트하드웨어 implements 하드웨어 {
    private final Map<Integer, Integer> 포트값 = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String មាតិកា_តំលៃ) {
        직렬기록.append(មាតិកា_តំលៃ);
        System.out.print(មាតិកា_តំលៃ);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer តំលៃ = 포트값.get(Integer.valueOf(포트번호));
        return តំលៃ == null ? 0 : តំលៃ.intValue();
    }

    @Override
    public void សរសេរ_ច្រក_បៃ(int 포트번호, int តំលៃ) {
        포트값.put(Integer.valueOf(포트번호), Integer.valueOf(តំលៃ & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // ហូស 시험에서는 បន្ទាប់_ធាតុ 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

