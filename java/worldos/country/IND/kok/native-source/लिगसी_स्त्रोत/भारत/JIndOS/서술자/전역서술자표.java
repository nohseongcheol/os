// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 स्थिती_मोल_e10195a1 विभाग_मोल 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int फाटभूंय_मोल;
        private final int 한계;
        private final int ऍक्सॅस_मोल;

        조각(int फाटभूंय_मोल, int 한계, int ऍक्सॅस_मोल) {
            this.फाटभूंय_मोल = फाटभूंय_मोल;
            this.한계 = 한계;
            this.ऍक्सॅस_मोल = ऍक्सॅस_मोल;
        }

        public int फाटभूंय_मोल() { return फाटभूंय_मोल; }
        public int 한계() { return 한계; }
        public int ऍक्सॅस_मोल() { return ऍक्सॅस_मोल; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int फाटभूंय_मोल, int 한계, int ऍक्सॅस_मोल) {
        조각들.add(new 조각(फाटभूंय_मोल, 한계, ऍक्सॅस_मोल));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void संच_डिफॉल्ट_मोल() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

