// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Гърция.JGrcOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Състояние_стойност раздел_стойност 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Фон_стойност;
        private final int 한계;
        private final int достъп_стойност;

        조각(int Фон_стойност, int 한계, int достъп_стойност) {
            this.Фон_стойност = Фон_стойност;
            this.한계 = 한계;
            this.достъп_стойност = достъп_стойност;
        }

        public int Фон_стойност() { return Фон_стойност; }
        public int 한계() { return 한계; }
        public int достъп_стойност() { return достъп_стойност; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int добавям_запис(int Фон_стойност, int 한계, int достъп_стойност) {
        조각들.add(new 조각(Фон_стойност, 한계, достъп_стойност));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void набор_стойност_по_подразбиране() {
        조각들.clear();
        добавям_запис(0, 0, 0);
        добавям_запис(0, 0xfffff, 0x9a);
        добавям_запис(0, 0xfffff, 0x92);
        добавям_запис(0, 0xfffff, 0xfa);
        добавям_запис(0, 0xfffff, 0xf2);
    }
}

