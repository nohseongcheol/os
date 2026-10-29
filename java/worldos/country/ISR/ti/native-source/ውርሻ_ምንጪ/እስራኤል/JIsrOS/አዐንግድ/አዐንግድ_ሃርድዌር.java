// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.አዐንግድ;

import java.util.HashMap;
import java.util.Map;
import እስራኤል.JIsrOS.ፍረ.ሃርድዌር_ዋጋ;

/** 일반 JVM에서 관리 커널을 결정적으로 시험하는 ሃርድዌር_ዋጋ 대역이다. */
public final class አዐንግድ_ሃርድዌር implements ሃርድዌር_ዋጋ {
    private final Map<Integer, Integer> ሃርድዌር_ወደብ_ዋጋ = new HashMap<Integer, Integer>();
    private final StringBuilder 직렬기록 = new StringBuilder();

    @Override
    public void 직렬출력(String ትሕዝቶ_ዋጋ) {
        직렬기록.append(ትሕዝቶ_ዋጋ);
        System.out.print(ትሕዝቶ_ዋጋ);
    }

    @Override
    public int 포트바이트읽기(int 포트번호) {
        Integer ዋጋ = ሃርድዌር_ወደብ_ዋጋ.get(Integer.valueOf(포트번호));
        return ዋጋ == null ? 0 : ዋጋ.intValue();
    }

    @Override
    public void ጸሓፍ_ወደብ_ባይት(int 포트번호, int ዋጋ) {
        ሃርድዌር_ወደብ_ዋጋ.put(Integer.valueOf(포트번호), Integer.valueOf(ዋጋ & 0xff));
    }

    @Override
    public void 중앙처리장치멈춤() {
        // አዐንግድ 시험에서는 다음 사건을 기다리지 않고 즉시 반환한다.
    }

    public String 직렬기록() {
        return 직렬기록.toString();
    }
}

