// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import እስራኤል.JIsrOS.기억공간.ገጽ_ኣካያዲ;
import እስራኤል.JIsrOS.ናይ_ፋይል_ስርዓት.파일서술자표;

/** መስርሕ_ዋጋ 식별자와 라운드로빈 ኣዳልው 대기열을 관리한다. */
public final class 배정기 {
    private final ገጽ_ኣካያዲ 쪽관리;
    private final Map<Integer, መስርሕ_ዋጋ> መስርሕ_ዝርዝር = new HashMap<Integer, መስርሕ_ዋጋ>();
    private final Queue<መስርሕ_ዋጋ> 준비대기열 = new ArrayDeque<መስርሕ_ዋጋ>();
    private int 다음식별자 = 1;

    public 배정기(ገጽ_ኣካያዲ 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public መስርሕ_ዋጋ 첫과정(파일서술자표 파일서술자) {
        መስርሕ_ዋጋ 새과정 = new መስርሕ_ዋጋ(ምምዳብ_ፈላዪ(), 0, 쪽관리.새주소공간(), 파일서술자);
        መስርሕ_ዝርዝር.put(Integer.valueOf(새과정.ፈላዪ_ዋጋ_5b7b8b77()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public መስርሕ_ዋጋ 복제(መስርሕ_ዋጋ 부모) {
        መስርሕ_ዋጋ ቆልዓ_ዋጋ = new መስርሕ_ዋጋ(
                ምምዳብ_ፈላዪ(),
                부모.ፈላዪ_ዋጋ_5b7b8b77(),
                쪽관리.쓰기시복사복제(부모.ኣድራሻ_ቦታ()),
                부모.파일서술자().복제());
        ቆልዓ_ዋጋ.프로그램끝설정(부모.프로그램끝());
        መስርሕ_ዝርዝር.put(Integer.valueOf(ቆልዓ_ዋጋ.ፈላዪ_ዋጋ_5b7b8b77()), ቆልዓ_ዋጋ);
        준비대기열.offer(ቆልዓ_ዋጋ);
        return ቆልዓ_ዋጋ;
    }

    public መስርሕ_ዋጋ 다음과정() {
        int 검사수 = 준비대기열.size();
        for (int መሐበሪ = 0; መሐበሪ < 검사수; መሐበሪ++) {
            መስርሕ_ዋጋ 다음 = 준비대기열.poll();
            if (다음 != null && (다음.ደረጃ_ዋጋ() == መስርሕ_ደረጃ.ኣዳልው || 다음.ደረጃ_ዋጋ() == መስርሕ_ደረጃ.ተግብር_ትእዛዝ)) {
                다음.እኩብ_ደረጃ(መስርሕ_ደረጃ.ተግብር_ትእዛዝ);
                준비대기열.offer(다음);
                return 다음;
            }
        }
        return null;
    }

    public int 자식기다리기(መስርሕ_ዋጋ 부모, int ቆልዓ_ፈላዪ, boolean 기다리지않음) {
        for (መስርሕ_ዋጋ 후보 : መስርሕ_ዝርዝር.values()) {
            if (후보.부모식별자() != 부모.ፈላዪ_ዋጋ_5b7b8b77()) {
                continue;
            }
            if (ቆልዓ_ፈላዪ > 0 && 후보.ፈላዪ_ዋጋ_5b7b8b77() != ቆልዓ_ፈላዪ) {
                continue;
            }
            if (후보.ደረጃ_ዋጋ() == መስርሕ_ደረጃ.ውጻእ_መተግበሪ) {
                int 결과 = (후보.종료값() & 0xff) << 8;
                መስርሕ_ዝርዝር.remove(Integer.valueOf(후보.ፈላዪ_ዋጋ_5b7b8b77()));
                return 결과;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public መስርሕ_ዋጋ ርኸብ_መስርሕ(int ፈላዪ_ዋጋ_5b7b8b77) {
        return መስርሕ_ዝርዝር.get(Integer.valueOf(ፈላዪ_ዋጋ_5b7b8b77));
    }

    private int ምምዳብ_ፈላዪ() {
        return 다음식별자++;
    }
}
