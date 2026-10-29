// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 अवस्था_मान खंड_मान 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int वॉलपेपर_मान;
        private final int 한계;
        private final int पहुँच_मान;

        조각(int वॉलपेपर_मान, int 한계, int पहुँच_मान) {
            this.वॉलपेपर_मान = वॉलपेपर_मान;
            this.한계 = 한계;
            this.पहुँच_मान = पहुँच_मान;
        }

        public int वॉलपेपर_मान() { return वॉलपेपर_मान; }
        public int 한계() { return 한계; }
        public int पहुँच_मान() { return पहुँच_मान; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int जोड़ें_एन्ट्री(int वॉलपेपर_मान, int 한계, int पहुँच_मान) {
        조각들.add(new 조각(वॉलपेपर_मान, 한계, पहुँच_मान));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void सेट_डिफ़ॉल्ट_मान() {
        조각들.clear();
        जोड़ें_एन्ट्री(0, 0, 0);
        जोड़ें_एन्ट्री(0, 0xfffff, 0x9a);
        जोड़ें_एन्ट्री(0, 0xfffff, 0x92);
        जोड़ें_एन्ट्री(0, 0xfffff, 0xfa);
        जोड़ें_एन्ट्री(0, 0xfffff, 0xf2);
    }
}

