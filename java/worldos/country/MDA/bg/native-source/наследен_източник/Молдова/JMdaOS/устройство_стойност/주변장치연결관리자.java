// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Молдова.JMdaOS.устройство_стойност;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI устройство_стойност 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class 주변장치연결관리자 {
    public static final class устройство_стойност {
        private final int доставчик_Идентификатор;
        private final int устройство_Идентификатор;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public устройство_стойност(int доставчик_Идентификатор, int устройство_Идентификатор, int 입출력바탕, int 개입중단번호) {
            this.доставчик_Идентификатор = доставчик_Идентификатор;
            this.устройство_Идентификатор = устройство_Идентификатор;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int доставчик_Идентификатор() { return доставчик_Идентификатор; }
        public int устройство_Идентификатор() { return устройство_Идентификатор; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<устройство_стойност> Устройства_Списък = new ArrayList<устройство_стойност>();

    public void 발견(устройство_стойност устройство_стойност) {
        Устройства_Списък.add(устройство_стойност);
    }

    public List<устройство_стойност> Устройства_Списък() {
        return Collections.unmodifiableList(Устройства_Списък);
    }

    public устройство_стойност Търсене_запис(int доставчик_Идентификатор, int устройство_Идентификатор) {
        for (устройство_стойност 후보 : Устройства_Списък) {
            if (후보.доставчик_Идентификатор == доставчик_Идентификатор && 후보.устройство_Идентификатор == устройство_Идентификатор) {
                return 후보;
            }
        }
        return null;
    }
}

