// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 абал_маани бөлүк_маани_366e0bfa 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Фон_маани;
        private final int 한계;
        private final int мүмкүндүк_алуу_маани;

        조각(int Фон_маани, int 한계, int мүмкүндүк_алуу_маани) {
            this.Фон_маани = Фон_маани;
            this.한계 = 한계;
            this.мүмкүндүк_алуу_маани = мүмкүндүк_алуу_маани;
        }

        public int Фон_маани() { return Фон_маани; }
        public int 한계() { return 한계; }
        public int мүмкүндүк_алуу_маани() { return мүмкүндүк_алуу_маани; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Фон_маани, int 한계, int мүмкүндүк_алуу_маани) {
        조각들.add(new 조각(Фон_маани, 한계, мүмкүндүк_алуу_маани));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void топ_жарыяланбаган_маани() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

