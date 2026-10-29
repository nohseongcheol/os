// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 stand_VALUE seksie_VALUE 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int muur_VALUE;
        private final int 한계;
        private final int toegang_VALUE;

        조각(int muur_VALUE, int 한계, int toegang_VALUE) {
            this.muur_VALUE = muur_VALUE;
            this.한계 = 한계;
            this.toegang_VALUE = toegang_VALUE;
        }

        public int muur_VALUE() { return muur_VALUE; }
        public int 한계() { return 한계; }
        public int toegang_VALUE() { return toegang_VALUE; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int muur_VALUE, int 한계, int toegang_VALUE) {
        조각들.add(new 조각(muur_VALUE, 한계, toegang_VALUE));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void stel_verstekwaarde() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

