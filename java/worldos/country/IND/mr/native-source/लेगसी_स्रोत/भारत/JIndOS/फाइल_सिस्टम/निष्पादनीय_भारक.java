// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.फाइल_सिस्टम;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** लहान-अंत क्रमाच्या ELF32 कार्यसंचिकांचे शीर्षक आणि भारणभाग तपासते. */
public final class निष्पादनीय_भारक {
    public static final class विभाग_मूल्य {
        private final int प्रकार_मूल्य;
        private final int ध्वजांकित_करा_मूल्य;
        private final int पत्ता;
        private final int संचिका_स्थान;
        private final int आकार;

        विभाग_मूल्य(int प्रकार_मूल्य, int ध्वजांकित_करा_मूल्य, int पत्ता, int संचिका_स्थान, int आकार) {
            this.प्रकार_मूल्य = प्रकार_मूल्य;
            this.ध्वजांकित_करा_मूल्य = ध्वजांकित_करा_मूल्य;
            this.पत्ता = पत्ता;
            this.संचिका_स्थान = संचिका_स्थान;
            this.आकार = आकार;
        }

        public int प्रकार_मूल्य() {
            return प्रकार_मूल्य;
        }

        public int ध्वजांकित_करा_मूल्य() {
            return ध्वजांकित_करा_मूल्य;
        }

        public int पत्ता() {
            return पत्ता;
        }

        public int संचिका_स्थान() {
            return संचिका_स्थान;
        }

        public int आकार() {
            return आकार;
        }
    }

    public static final class चित्र {
        private final int प्रारंभ_पत्ता;
        private final List<विभाग_मूल्य> विभाग_यादी;

        चित्र(int प्रारंभ_पत्ता, List<विभाग_मूल्य> विभाग_यादी) {
            this.प्रारंभ_पत्ता = प्रारंभ_पत्ता;
            this.विभाग_यादी = Collections.unmodifiableList(विभाग_यादी);
        }

        public int प्रारंभ_पत्ता() {
            return प्रारंभ_पत्ता;
        }

        public List<विभाग_मूल्य> विभाग_यादी() {
            return विभाग_यादी;
        }
    }

    public चित्र पडताळण्या(byte[] डेटा) {
        if (डेटा == null || डेटा.length < 52
                || डेटा[0] != 0x7f || डेटा[1] != 'E' || डेटा[2] != 'L' || डेटा[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (डेटा[4] != 1 || डेटा[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int प्रारंभ_पत्ता = पूर्णांक_पार्स_करा(डेटा, 24);
        int विभाग_सारणी_स्थान = पूर्णांक_पार्स_करा(डेटा, 32);
        int विभाग_प्रविष्टी_आकारा = लघु_पूर्णांक_वाचा(डेटा, 46);
        int विभाग_संख्या = लघु_पूर्णांक_वाचा(डेटा, 48);
        if (विभाग_प्रविष्टी_आकारा < 40 || विभाग_सारणी_स्थान < 0
                || (long) विभाग_सारणी_स्थान + (long) विभाग_प्रविष्टी_आकारा * विभाग_संख्या > डेटा.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<विभाग_मूल्य> विभाग_यादी = new ArrayList<विभाग_मूल्य>();
        for (int अनुक्रमणिका = 0; अनुक्रमणिका < विभाग_संख्या; अनुक्रमणिका++) {
            int जागा = विभाग_सारणी_स्थान + अनुक्रमणिका * विभाग_प्रविष्टी_आकारा;
            int प्रकार_मूल्य = पूर्णांक_पार्स_करा(डेटा, जागा + 4);
            int ध्वजांकित_करा_मूल्य = पूर्णांक_पार्स_करा(डेटा, जागा + 8);
            int पत्ता = पूर्णांक_पार्स_करा(डेटा, जागा + 12);
            int संचिका_स्थान = पूर्णांक_पार्स_करा(डेटा, जागा + 16);
            int आकार = पूर्णांक_पार्स_करा(डेटा, जागा + 20);
            if (आकार < 0 || (प्रकार_मूल्य != 8 && ((long) संचिका_स्थान + आकार > डेटा.length || संचिका_स्थान < 0))) {
                throw new IllegalArgumentException("ELF विभाग_मूल्य डेटा 범위가 올바르지 않습니다.");
            }
            विभाग_यादी.add(new विभाग_मूल्य(प्रकार_मूल्य, ध्वजांकित_करा_मूल्य, पत्ता, संचिका_स्थान, आकार));
        }
        return new चित्र(प्रारंभ_पत्ता, विभाग_यादी);
    }

    private int पूर्णांक_पार्स_करा(byte[] डेटा, int जागा) {
        if (जागा < 0 || जागा > डेटा.length - 4) {
            throw new IllegalArgumentException("ELF पूर्णांक 범위를 벗어났습니다.");
        }
        return (डेटा[जागा] & 0xff)
                | ((डेटा[जागा + 1] & 0xff) << 8)
                | ((डेटा[जागा + 2] & 0xff) << 16)
                | ((डेटा[जागा + 3] & 0xff) << 24);
    }

    private int लघु_पूर्णांक_वाचा(byte[] डेटा, int जागा) {
        if (जागा < 0 || जागा > डेटा.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 पूर्णांक 범위를 벗어났습니다.");
        }
        return (डेटा[जागा] & 0xff) | ((डेटा[जागा + 1] & 0xff) << 8);
    }
}
