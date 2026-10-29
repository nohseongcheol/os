// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Словаччина.JSvkOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Стан_значення розділ_значення_366e0bfa 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Фон_значення;
        private final int 한계;
        private final int доступ_значення;

        조각(int Фон_значення, int 한계, int доступ_значення) {
            this.Фон_значення = Фон_значення;
            this.한계 = 한계;
            this.доступ_значення = доступ_значення;
        }

        public int Фон_значення() { return Фон_значення; }
        public int 한계() { return 한계; }
        public int доступ_значення() { return доступ_значення; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int додавати_запис(int Фон_значення, int 한계, int доступ_значення) {
        조각들.add(new 조각(Фон_значення, 한계, доступ_значення));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void група_стандартне_значення() {
        조각들.clear();
        додавати_запис(0, 0, 0);
        додавати_запис(0, 0xfffff, 0x9a);
        додавати_запис(0, 0xfffff, 0x92);
        додавати_запис(0, 0xfffff, 0xfa);
        додавати_запис(0, 0xfffff, 0xf2);
    }
}

