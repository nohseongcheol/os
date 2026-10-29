// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.기억공간;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

/** 4 KiB ገጽ_ዋጋ 연결과 ጸሓፍ 시 복사를 제공한다. */
public final class ገጽ_ኣካያዲ {
    public static final int መጠን_ገፅ = 4096;

    private static final class ገጽ_ዋጋ {
        private byte[] ሓበሬታ = new byte[መጠን_ገፅ];
        private int 참조수 = 1;
        private boolean 쓰기가능 = true;
        private boolean 쓰기시복사;
    }

    public static final class ኣድራሻ_ቦታ {
        private final Map<Integer, ገጽ_ዋጋ> ገጽ_ሰሌዳ = new HashMap<Integer, ገጽ_ዋጋ>();
    }

    public ኣድራሻ_ቦታ 새주소공간() {
        return new ኣድራሻ_ቦታ();
    }

    public void ብካርታ_ኣርዒ_ገጽ(ኣድራሻ_ቦታ 공간, int መሳሊ_ኣድራሻ, boolean 쓰기가능) {
        int መሐበሪ = 쪽번호(መሳሊ_ኣድራሻ);
        ገጽ_ዋጋ 새쪽 = new ገጽ_ዋጋ();
        새쪽.쓰기가능 = 쓰기가능;
        공간.ገጽ_ሰሌዳ.put(Integer.valueOf(መሐበሪ), 새쪽);
    }

    public ኣድራሻ_ቦታ 쓰기시복사복제(ኣድራሻ_ቦታ 원본) {
        ኣድራሻ_ቦታ 복제본 = new ኣድራሻ_ቦታ();
        for (Map.Entry<Integer, ገጽ_ዋጋ> ምእታው_ዋጋ : 원본.ገጽ_ሰሌዳ.entrySet()) {
            ገጽ_ዋጋ 공유쪽 = ምእታው_ዋጋ.getValue();
            공유쪽.참조수++;
            if (공유쪽.쓰기가능) {
                공유쪽.쓰기가능 = false;
                공유쪽.쓰기시복사 = true;
            }
            복제본.ገጽ_ሰሌዳ.put(ምእታው_ዋጋ.getKey(), 공유쪽);
        }
        return 복제본;
    }

    public byte 바이트읽기(ኣድራሻ_ቦታ 공간, int መሳሊ_ኣድራሻ) {
        ገጽ_ዋጋ ዕላማ = ርኸብ_ገጽ(공간, መሳሊ_ኣድራሻ);
        return ዕላማ.ሓበሬታ[Math.floorMod(መሳሊ_ኣድራሻ, መጠን_ገፅ)];
    }

    public void ጸሓፍ_ባይት_ዋጋ(ኣድራሻ_ቦታ 공간, int መሳሊ_ኣድራሻ, byte ዋጋ) {
        int መሐበሪ = 쪽번호(መሳሊ_ኣድራሻ);
        ገጽ_ዋጋ ዕላማ = ርኸብ_ገጽ(공간, መሳሊ_ኣድራሻ);
        if (!ዕላማ.쓰기가능) {
            if (!ዕላማ.쓰기시복사) {
                throw new IllegalStateException("읽기 전용 쪽입니다.");
            }
            ዕላማ = ፍጠር_ግላዊ_ገጽ(공간, መሐበሪ, ዕላማ);
        }
        ዕላማ.ሓበሬታ[Math.floorMod(መሳሊ_ኣድራሻ, መጠን_ገፅ)] = ዋጋ;
    }

    public void 범위개인쓰기(ኣድራሻ_ቦታ 공간, int ጀምር_ኣድራሻ, int መጠን) {
        if (መጠን < 0) {
            throw new IllegalArgumentException("크기가 음수입니다.");
        }
        int ኣቑም_ኣድራሻ = Math.addExact(ጀምር_ኣድራሻ, መጠን);
        for (int ኣድራሻ = ጀምር_ኣድራሻ; ኣድራሻ < ኣቑም_ኣድራሻ; ኣድራሻ = (쪽번호(ኣድራሻ) + 1) * መጠን_ገፅ) {
            int መሐበሪ = 쪽번호(ኣድራሻ);
            ገጽ_ዋጋ ዕላማ = ርኸብ_ገጽ(공간, ኣድራሻ);
            if (ዕላማ.쓰기시복사) {
                ፍጠር_ግላዊ_ገጽ(공간, መሐበሪ, ዕላማ);
            } else {
                ዕላማ.쓰기가능 = true;
            }
        }
    }

    public void 범위쓰기(ኣድራሻ_ቦታ 공간, int ጀምር_ኣድራሻ, byte[] ሓበሬታ) {
        for (int መሐበሪ = 0; መሐበሪ < ሓበሬታ.length; መሐበሪ++) {
            ጸሓፍ_ባይት_ዋጋ(공간, ጀምር_ኣድራሻ + መሐበሪ, ሓበሬታ[መሐበሪ]);
        }
    }

    private ገጽ_ዋጋ ፍጠር_ግላዊ_ገጽ(ኣድራሻ_ቦታ 공간, int መሐበሪ, ገጽ_ዋጋ 공유쪽) {
        ገጽ_ዋጋ ግላዊ_ገጽ = new ገጽ_ዋጋ();
        ግላዊ_ገጽ.ሓበሬታ = Arrays.copyOf(공유쪽.ሓበሬታ, 공유쪽.ሓበሬታ.length);
        ግላዊ_ገጽ.쓰기가능 = true;
        ግላዊ_ገጽ.쓰기시복사 = false;
        공유쪽.참조수--;
        공간.ገጽ_ሰሌዳ.put(Integer.valueOf(መሐበሪ), ግላዊ_ገጽ);
        return ግላዊ_ገጽ;
    }

    private ገጽ_ዋጋ ርኸብ_ገጽ(ኣድራሻ_ቦታ 공간, int ኣድራሻ) {
        ገጽ_ዋጋ ዕላማ = 공간.ገጽ_ሰሌዳ.get(Integer.valueOf(쪽번호(ኣድራሻ)));
        if (ዕላማ == null) {
            throw new IllegalStateException("연결되지 않은 가상 주소입니다.");
        }
        return ዕላማ;
    }

    private int 쪽번호(int ኣድራሻ) {
        if (ኣድራሻ < 0) {
            throw new IllegalArgumentException("주소가 음수입니다.");
        }
        return ኣድራሻ / መጠን_ገፅ;
    }
}

