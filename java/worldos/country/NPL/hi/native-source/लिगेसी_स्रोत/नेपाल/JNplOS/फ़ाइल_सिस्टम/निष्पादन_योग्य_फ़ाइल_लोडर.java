// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाल.JNplOS.फ़ाइल_सिस्टम;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian निष्पादित_करें_आदेश 파일의 머리부와 적재 구역을 검증한다. */
public final class निष्पादन_योग्य_फ़ाइल_लोडर {
    public static final class खंड_मान {
        private final int 종류;
        private final int ध्वज_मान;
        private final int पता;
        private final int फ़ाइल_पद;
        private final int आकार;

        खंड_मान(int 종류, int ध्वज_मान, int पता, int फ़ाइल_पद, int आकार) {
            this.종류 = 종류;
            this.ध्वज_मान = ध्वज_मान;
            this.पता = पता;
            this.फ़ाइल_पद = फ़ाइल_पद;
            this.आकार = आकार;
        }

        public int 종류() {
            return 종류;
        }

        public int ध्वज_मान() {
            return ध्वज_मान;
        }

        public int पता() {
            return पता;
        }

        public int फ़ाइल_पद() {
            return फ़ाइल_पद;
        }

        public int आकार() {
            return आकार;
        }
    }

    public static final class छवि {
        private final int प्रारंभ_पता;
        private final List<खंड_मान> 구역들;

        छवि(int प्रारंभ_पता, List<खंड_मान> 구역들) {
            this.प्रारंभ_पता = प्रारंभ_पता;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int प्रारंभ_पता() {
            return प्रारंभ_पता;
        }

        public List<खंड_मान> 구역들() {
            return 구역들;
        }
    }

    public छवि 검사(byte[] आँकड़े) {
        if (आँकड़े == null || आँकड़े.length < 52
                || आँकड़े[0] != 0x7f || आँकड़े[1] != 'E' || आँकड़े[2] != 'L' || आँकड़े[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (आँकड़े[4] != 1 || आँकड़े[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int प्रारंभ_पता = पार्स_करें_पूर्णांक(आँकड़े, 24);
        int खंड_तालिका_पद = पार्स_करें_पूर्णांक(आँकड़े, 32);
        int खंड_एन्ट्री_आकार = 짧은정수읽기(आँकड़े, 46);
        int 구역수 = 짧은정수읽기(आँकड़े, 48);
        if (खंड_एन्ट्री_आकार < 40 || खंड_तालिका_पद < 0
                || (long) खंड_तालिका_पद + (long) खंड_एन्ट्री_आकार * 구역수 > आँकड़े.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<खंड_मान> 구역들 = new ArrayList<खंड_मान>();
        for (int इंडेक्स = 0; इंडेक्स < 구역수; इंडेक्स++) {
            int स्थान = खंड_तालिका_पद + इंडेक्स * खंड_एन्ट्री_आकार;
            int 종류 = पार्स_करें_पूर्णांक(आँकड़े, स्थान + 4);
            int ध्वज_मान = पार्स_करें_पूर्णांक(आँकड़े, स्थान + 8);
            int पता = पार्स_करें_पूर्णांक(आँकड़े, स्थान + 12);
            int फ़ाइल_पद = पार्स_करें_पूर्णांक(आँकड़े, स्थान + 16);
            int आकार = पार्स_करें_पूर्णांक(आँकड़े, स्थान + 20);
            if (आकार < 0 || (종류 != 8 && ((long) फ़ाइल_पद + आकार > आँकड़े.length || फ़ाइल_पद < 0))) {
                throw new IllegalArgumentException("ELF खंड_मान आँकड़े 범위가 올바르지 않습니다.");
            }
            구역들.add(new खंड_मान(종류, ध्वज_मान, पता, फ़ाइल_पद, आकार));
        }
        return new छवि(प्रारंभ_पता, 구역들);
    }

    private int पार्स_करें_पूर्णांक(byte[] आँकड़े, int स्थान) {
        if (स्थान < 0 || स्थान > आँकड़े.length - 4) {
            throw new IllegalArgumentException("ELF पूर्णांक 범위를 벗어났습니다.");
        }
        return (आँकड़े[स्थान] & 0xff)
                | ((आँकड़े[स्थान + 1] & 0xff) << 8)
                | ((आँकड़े[स्थान + 2] & 0xff) << 16)
                | ((आँकड़े[स्थान + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] आँकड़े, int स्थान) {
        if (स्थान < 0 || स्थान > आँकड़े.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 पूर्णांक 범위를 벗어났습니다.");
        }
        return (आँकड़े[स्थान] & 0xff) | ((आँकड़े[स्थान + 1] & 0xff) << 8);
    }
}
