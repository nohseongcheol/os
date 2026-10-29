// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Кыргызстан.JKgzOS.түзмөк_маани;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI түзмөк_маани 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class перифериялык_түзмөк_шина_башкаруучу {
    public static final class түзмөк_маани {
        private final int 판매자식별자;
        private final int түзмөк_аныктагыч;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public түзмөк_маани(int 판매자식별자, int түзмөк_аныктагыч, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.түзмөк_аныктагыч = түзмөк_аныктагыч;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int түзмөк_аныктагыч() { return түзмөк_аныктагыч; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<түзмөк_маани> Түзмөктөр_Тизме = new ArrayList<түзмөк_маани>();

    public void 발견(түзмөк_маани түзмөк_маани) {
        Түзмөктөр_Тизме.add(түзмөк_маани);
    }

    public List<түзмөк_маани> Түзмөктөр_Тизме() {
        return Collections.unmodifiableList(Түзмөктөр_Тизме);
    }

    public түзмөк_маани табуу_киргизме_жазуу(int 판매자식별자, int түзмөк_аныктагыч) {
        for (түзмөк_маани 후보 : Түзмөктөр_Тизме) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.түзмөк_аныктагыч == түзмөк_аныктагыч) {
                return 후보;
            }
        }
        return null;
    }
}

