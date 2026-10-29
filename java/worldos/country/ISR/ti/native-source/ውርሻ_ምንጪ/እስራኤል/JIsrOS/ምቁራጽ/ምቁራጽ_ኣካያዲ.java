// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.ምቁራጽ;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class ምቁራጽ_ኣካያዲ {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean ንቑሕ;

    public void 등록(int መሐበሪ, 개입중단처리기 처리기) {
        번호확인(መሐበሪ);
        처리기들[መሐበሪ] = 처리기;
    }

    public void ፍታሕ_መኽዘን(int መሐበሪ) {
        번호확인(መሐበሪ);
        처리기들[መሐበሪ] = null;
    }

    public int ኣከፋፍል_ዋጋ(int መሐበሪ, int 저장된쌓임주소) {
        번호확인(መሐበሪ);
        if (!ንቑሕ) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[መሐበሪ];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.መስርሕ_ዋጋ_ምእታው(저장된쌓임주소);
    }

    public void ኣኽእል() {
        ንቑሕ = true;
    }

    public void ኣደቕስ() {
        ንቑሕ = false;
    }

    public boolean 활성인가() {
        return ንቑሕ;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int መሐበሪ) {
        if (መሐበሪ < 0 || መሐበሪ >= 처리기들.length) {
            throw new IllegalArgumentException("ምቁራጽ 번호가 올바르지 않습니다.");
        }
    }
}

