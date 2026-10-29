// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 күй_мән бөлім_мән_366e0bfa 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Фон_мән;
        private final int 한계;
        private final int қатынас_мән;

        조각(int Фон_мән, int 한계, int қатынас_мән) {
            this.Фон_мән = Фон_мән;
            this.한계 = 한계;
            this.қатынас_мән = қатынас_мән;
        }

        public int Фон_мән() { return Фон_мән; }
        public int 한계() { return 한계; }
        public int қатынас_мән() { return қатынас_мән; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int қосу_енгізу(int Фон_мән, int 한계, int қатынас_мән) {
        조각들.add(new 조각(Фон_мән, 한계, қатынас_мән));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void жинақ_әдепкі_мән() {
        조각들.clear();
        қосу_енгізу(0, 0, 0);
        қосу_енгізу(0, 0xfffff, 0x9a);
        қосу_енгізу(0, 0xfffff, 0x92);
        қосу_енгізу(0, 0xfffff, 0xfa);
        қосу_енгізу(0, 0xfffff, 0xf2);
    }
}

