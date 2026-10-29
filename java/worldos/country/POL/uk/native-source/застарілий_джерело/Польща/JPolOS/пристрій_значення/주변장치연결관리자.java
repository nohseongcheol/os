// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Польща.JPolOS.пристрій_значення;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI пристрій_значення 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class пристрій_значення {
        private final int постачальник_ідентифікатор;
        private final int пристрій_ідентифікатор;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public пристрій_значення(int постачальник_ідентифікатор, int пристрій_ідентифікатор, int 입출력바탕, int 개입중단번호) {
            this.постачальник_ідентифікатор = постачальник_ідентифікатор;
            this.пристрій_ідентифікатор = пристрій_ідентифікатор;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int постачальник_ідентифікатор() { return постачальник_ідентифікатор; }
        public int пристрій_ідентифікатор() { return пристрій_ідентифікатор; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<пристрій_значення> Пристрої_список = new ArrayList<пристрій_значення>();

    public void 발견(пристрій_значення пристрій_значення) {
        Пристрої_список.add(пристрій_значення);
    }

    public List<пристрій_значення> Пристрої_список() {
        return Collections.unmodifiableList(Пристрої_список);
    }

    public пристрій_значення Знайти_запис(int постачальник_ідентифікатор, int пристрій_ідентифікатор) {
        for (пристрій_значення кандидат : Пристрої_список) {
            if (кандидат.постачальник_ідентифікатор == постачальник_ідентифікатор && кандидат.пристрій_ідентифікатор == пристрій_ідентифікатор) {
                return кандидат;
            }
        }
        return null;
    }
}

