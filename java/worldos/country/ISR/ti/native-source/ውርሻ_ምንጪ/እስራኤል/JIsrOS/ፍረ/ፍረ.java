// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.ፍረ;

import እስራኤል.JIsrOS.기억공간.ማህደር_ዝኽረት_ኣካያዲ;
import እስራኤል.JIsrOS.기억공간.ገጽ_ኣካያዲ;
import እስራኤል.JIsrOS.입력.입력관리자;
import እስራኤል.JIsrOS.작업.መስርሕ_ዋጋ;
import እስራኤል.JIsrOS.작업.배정기;
import እስራኤል.JIsrOS.체계호출.체계호출;
import እስራኤል.JIsrOS.ናይ_ፋይል_ስርዓት.파일서술자표;
import እስራኤል.JIsrOS.ናይ_ፋይል_ስርዓት.ናይ_ፋይል_ስርዓት;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class ፍረ {
    private final ሃርድዌር_ዋጋ መሳርሒ_ዋጋ;
    private final ማህደር_ዝኽረት_ኣካያዲ 기억공간 = new ማህደር_ዝኽረት_ኣካያዲ(32 * 1024 * 1024);
    private final ገጽ_ኣካያዲ 쪽관리 = new ገጽ_ኣካያዲ();
    private final ናይ_ፋይል_ስርዓት ናይ_ፋይል_ስርዓት = new ናይ_ፋይል_ስርዓት();
    private final 배정기 배정기 = new 배정기(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final መስርሕ_ዋጋ 첫과정;
    private final 체계호출 체계호출;

    public ፍረ(ሃርድዌር_ዋጋ መሳርሒ_ዋጋ) {
        this.መሳርሒ_ዋጋ = መሳርሒ_ዋጋ;
        첫과정 = 배정기.첫과정(new 파일서술자표(ናይ_ፋይል_ስርዓት));
        체계호출 = new 체계호출(ናይ_ፋይል_ስርዓት, 쪽관리, 배정기, መሳርሒ_ዋጋ, 입력관리);
    }

    public void ኣኺድ() {
        መሳርሒ_ዋጋ.직렬출력("=== JIsrOS 관리 ፍረ_ዋጋ ===\n");
    }

    public void 한단계실행() {
        መሳርሒ_ዋጋ.중앙처리장치멈춤();
    }

    public ማህደር_ዝኽረት_ኣካያዲ 기억공간() {
        return 기억공간;
    }

    public ገጽ_ኣካያዲ 쪽관리() {
        return 쪽관리;
    }

    public ናይ_ፋይል_ስርዓት ናይ_ፋይል_ስርዓት() {
        return ናይ_ፋይል_ስርዓት;
    }

    public 배정기 배정기() {
        return 배정기;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public መስርሕ_ዋጋ 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
