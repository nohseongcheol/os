// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package இந்தியா.JIndOS.화면;

import java.util.Arrays;

/** VGA 문자 방식과 같은 80x25 문자 화면 모형이다. */
public final class எழுத்துக்குறி_காட்சி {
    public static final int 너비 = 80;
    public static final int 높이 = 25;
    private final char[] 문자들 = new char[너비 * 높이];
    private int 가로;
    private int வெர்டிகல்_நிலை;

    public எழுத்துக்குறி_காட்சி() {
        அழி_உள்ளீடு();
    }

    public void வெளியீட்டு_இடம்(String உள்ளடக்கம்_மதிப்பு) {
        for (int அடைவு = 0; அடைவு < உள்ளடக்கம்_மதிப்பு.length(); அடைவு++) {
            char 문자 = உள்ளடக்கம்_மதிப்பு.charAt(அடைவு);
            if (문자 == '\n') {
                가로 = 0;
                வெர்டிகல்_நிலை++;
            } else {
                문자출력(가로++, வெர்டிகல்_நிலை, 문자);
            }
            if (가로 >= 너비) {
                가로 = 0;
                வெர்டிகல்_நிலை++;
            }
            if (வெர்டிகல்_நிலை >= 높이) {
                위로밀기();
            }
        }
    }

    public char 문자(int 가로, int வெர்டிகல்_நிலை) {
        சரிபார்_நிலை(가로, வெர்டிகல்_நிலை);
        return 문자들[வெர்டிகல்_நிலை * 너비 + 가로];
    }

    public void அழி_உள்ளீடு() {
        Arrays.fill(문자들, ' ');
        가로 = 0;
        வெர்டிகல்_நிலை = 0;
    }

    private void 문자출력(int 가로, int வெர்டிகல்_நிலை, char 문자) {
        சரிபார்_நிலை(가로, வெர்டிகல்_நிலை);
        문자들[வெர்டிகல்_நிலை * 너비 + 가로] = 문자;
    }

    private void 위로밀기() {
        System.arraycopy(문자들, 너비, 문자들, 0, 너비 * (높이 - 1));
        Arrays.fill(문자들, 너비 * (높이 - 1), 문자들.length, ' ');
        வெர்டிகல்_நிலை = 높이 - 1;
    }

    private void சரிபார்_நிலை(int 가로, int வெர்டிகல்_நிலை) {
        if (가로 < 0 || 가로 >= 너비 || வெர்டிகல்_நிலை < 0 || வெர்டிகல்_நிலை >= 높이) {
            throw new IllegalArgumentException("화면 위치가 올바르지 않습니다.");
        }
    }
}

