// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.መኽዘን_መሳርሒ;

import java.util.Arrays;

/** ATA 28비트 ትእዛዝ 계층과 같은 512바이트 논리 ክፋል_ዋጋ 장치다. */
public final class 고급기술결합장치 {
    public static final int ክፋል_መጠን = 512;
    private final byte[] ሓበሬታ;
    private final boolean ንምንባብ_ጥራይ_ዋጋ;

    public 고급기술결합장치(int 구역수, boolean ንምንባብ_ጥራይ_ዋጋ) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ክፋል_ዋጋ 수가 올바르지 않습니다.");
        }
        ሓበሬታ = new byte[Math.multiplyExact(구역수, ክፋል_መጠን)];
        this.ንምንባብ_ጥራይ_ዋጋ = ንምንባብ_ጥራይ_ዋጋ;
    }

    public int 구역수() {
        return ሓበሬታ.length / ክፋል_መጠን;
    }

    public void 읽기(int ክፋል_መሐበሪ, byte[] 받을곳) {
        범위확인(ክፋል_መሐበሪ, 받을곳);
        System.arraycopy(ሓበሬታ, ክፋል_መሐበሪ * ክፋል_መጠን, 받을곳, 0, ክፋል_መጠን);
    }

    public void ጸሓፍ(int ክፋል_መሐበሪ, byte[] 쓸자료) {
        if (ንምንባብ_ጥራይ_ዋጋ) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(ክፋል_መሐበሪ, 쓸자료);
        System.arraycopy(쓸자료, 0, ሓበሬታ, ክፋል_መሐበሪ * ክፋል_መጠን, ክፋል_መጠን);
    }

    public void 지우기() {
        if (ንምንባብ_ጥራይ_ዋጋ) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(ሓበሬታ, (byte) 0);
    }

    private void 범위확인(int ክፋል_መሐበሪ, byte[] 임시공간) {
        if (ክፋል_መሐበሪ < 0 || ክፋል_መሐበሪ >= 구역수() || 임시공간.length < ክፋል_መጠን) {
            throw new IllegalArgumentException("ATA ክፋል_ዋጋ 범위가 올바르지 않습니다.");
        }
    }
}

