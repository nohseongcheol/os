// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Украіна.JUkrOS.прылада_значэнне;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI прылада_значэнне 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class камплектацыя_шына_менеджар {
    public static final class прылада_значэнне {
        private final int пастаўшчык_ідэнтыфікатар;
        private final int прылада_ідэнтыфікатар;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public прылада_значэнне(int пастаўшчык_ідэнтыфікатар, int прылада_ідэнтыфікатар, int 입출력바탕, int 개입중단번호) {
            this.пастаўшчык_ідэнтыфікатар = пастаўшчык_ідэнтыфікатар;
            this.прылада_ідэнтыфікатар = прылада_ідэнтыфікатар;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int пастаўшчык_ідэнтыфікатар() { return пастаўшчык_ідэнтыфікатар; }
        public int прылада_ідэнтыфікатар() { return прылада_ідэнтыфікатар; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<прылада_значэнне> Прылады_Спіс = new ArrayList<прылада_значэнне>();

    public void 발견(прылада_значэнне прылада_значэнне) {
        Прылады_Спіс.add(прылада_значэнне);
    }

    public List<прылада_значэнне> Прылады_Спіс() {
        return Collections.unmodifiableList(Прылады_Спіс);
    }

    public прылада_значэнне выявіць_увядзенне(int пастаўшчык_ідэнтыфікатар, int прылада_ідэнтыфікатар) {
        for (прылада_значэнне 후보 : Прылады_Спіс) {
            if (후보.пастаўшчык_ідэнтыфікатар == пастаўшчык_ідэнтыфікатар && 후보.прылада_ідэнтыфікатар == прылада_ідэнтыфікатар) {
                return 후보;
            }
        }
        return null;
    }
}

