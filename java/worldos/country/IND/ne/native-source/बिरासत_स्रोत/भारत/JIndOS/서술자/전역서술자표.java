// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 स्थिति_मान सेक्सन_मान 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int वालपेपर_मान;
        private final int 한계;
        private final int पहुँच_मान;

        조각(int वालपेपर_मान, int 한계, int पहुँच_मान) {
            this.वालपेपर_मान = वालपेपर_मान;
            this.한계 = 한계;
            this.पहुँच_मान = पहुँच_मान;
        }

        public int वालपेपर_मान() { return वालपेपर_मान; }
        public int 한계() { return 한계; }
        public int पहुँच_मान() { return पहुँच_मान; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int वालपेपर_मान, int 한계, int पहुँच_मान) {
        조각들.add(new 조각(वालपेपर_मान, 한계, पहुँच_मान));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void सेट_पूर्वनिर्धारित_मान() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

