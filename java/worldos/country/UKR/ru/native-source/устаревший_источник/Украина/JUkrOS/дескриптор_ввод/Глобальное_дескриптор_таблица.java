// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украина.JUkrOS.дескриптор_ввод;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Состояние_ЗНАЧЕН раздел_ЗНАЧЕН_366e0bfa 설정값을 보관한다. */
public final class Глобальное_дескриптор_таблица {
    public static final class блок_ЗНАЧЕН_652d4b53 {
        private final int фон_ЗНАЧЕН;
        private final int 한계;
        private final int доступ_ЗНАЧЕН;

        блок_ЗНАЧЕН_652d4b53(int фон_ЗНАЧЕН, int 한계, int доступ_ЗНАЧЕН) {
            this.фон_ЗНАЧЕН = фон_ЗНАЧЕН;
            this.한계 = 한계;
            this.доступ_ЗНАЧЕН = доступ_ЗНАЧЕН;
        }

        public int фон_ЗНАЧЕН() { return фон_ЗНАЧЕН; }
        public int 한계() { return 한계; }
        public int доступ_ЗНАЧЕН() { return доступ_ЗНАЧЕН; }
    }

    private final List<блок_ЗНАЧЕН_652d4b53> 조각들 = new ArrayList<блок_ЗНАЧЕН_652d4b53>();

    public int добавить_ввод(int фон_ЗНАЧЕН, int 한계, int доступ_ЗНАЧЕН) {
        조각들.add(new блок_ЗНАЧЕН_652d4b53(фон_ЗНАЧЕН, 한계, доступ_ЗНАЧЕН));
        return (조각들.size() - 1) * 8;
    }

    public List<блок_ЗНАЧЕН_652d4b53> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void сет_значение_по_умолчанию() {
        조각들.clear();
        добавить_ввод(0, 0, 0);
        добавить_ввод(0, 0xfffff, 0x9a);
        добавить_ввод(0, 0xfffff, 0x92);
        добавить_ввод(0, 0xfffff, 0xfa);
        добавить_ввод(0, 0xfffff, 0xf2);
    }
}

