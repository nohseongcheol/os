// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Грузия.JGeoOS.устройство_ЗНАЧЕН;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI устройство_ЗНАЧЕН 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class периферийное_устройство_шина_менеджер {
    public static final class устройство_ЗНАЧЕН {
        private final int поставщик_идентификатор;
        private final int устройство_идентификатор;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public устройство_ЗНАЧЕН(int поставщик_идентификатор, int устройство_идентификатор, int 입출력바탕, int 개입중단번호) {
            this.поставщик_идентификатор = поставщик_идентификатор;
            this.устройство_идентификатор = устройство_идентификатор;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int поставщик_идентификатор() { return поставщик_идентификатор; }
        public int устройство_идентификатор() { return устройство_идентификатор; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<устройство_ЗНАЧЕН> Устройства_Список = new ArrayList<устройство_ЗНАЧЕН>();

    public void 발견(устройство_ЗНАЧЕН устройство_ЗНАЧЕН) {
        Устройства_Список.add(устройство_ЗНАЧЕН);
    }

    public List<устройство_ЗНАЧЕН> Устройства_Список() {
        return Collections.unmodifiableList(Устройства_Список);
    }

    public устройство_ЗНАЧЕН НАЙТИ_ввод(int поставщик_идентификатор, int устройство_идентификатор) {
        for (устройство_ЗНАЧЕН соискатель : Устройства_Список) {
            if (соискатель.поставщик_идентификатор == поставщик_идентификатор && соискатель.устройство_идентификатор == устройство_идентификатор) {
                return соискатель;
            }
        }
        return null;
    }
}

