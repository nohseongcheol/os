// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ipò_iye abala_iye 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Àgbétẹ́lẹ̀_iye;
        private final int 한계;
        private final int wáyè_sí_iye;

        조각(int Àgbétẹ́lẹ̀_iye, int 한계, int wáyè_sí_iye) {
            this.Àgbétẹ́lẹ̀_iye = Àgbétẹ́lẹ̀_iye;
            this.한계 = 한계;
            this.wáyè_sí_iye = wáyè_sí_iye;
        }

        public int Àgbétẹ́lẹ̀_iye() { return Àgbétẹ́lẹ̀_iye; }
        public int 한계() { return 한계; }
        public int wáyè_sí_iye() { return wáyè_sí_iye; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Àgbétẹ́lẹ̀_iye, int 한계, int wáyè_sí_iye) {
        조각들.add(new 조각(Àgbétẹ́lẹ̀_iye, 한계, wáyè_sí_iye));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ọ̀wọ̀_àdáwọ̀() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

