// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Грција.JGrcOS.уред_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI уред_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class додаток_магистрала_управник {
    public static final class уред_VALUE {
        private final int добавувач_идентификатор;
        private final int уред_идентификатор;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public уред_VALUE(int добавувач_идентификатор, int уред_идентификатор, int 입출력바탕, int 개입중단번호) {
            this.добавувач_идентификатор = добавувач_идентификатор;
            this.уред_идентификатор = уред_идентификатор;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int добавувач_идентификатор() { return добавувач_идентификатор; }
        public int уред_идентификатор() { return уред_идентификатор; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<уред_VALUE> Уреди_Список = new ArrayList<уред_VALUE>();

    public void 발견(уред_VALUE уред_VALUE) {
        Уреди_Список.add(уред_VALUE);
    }

    public List<уред_VALUE> Уреди_Список() {
        return Collections.unmodifiableList(Уреди_Список);
    }

    public уред_VALUE FIND_внес(int добавувач_идентификатор, int уред_идентификатор) {
        for (уред_VALUE 후보 : Уреди_Список) {
            if (후보.добавувач_идентификатор == добавувач_идентификатор && 후보.уред_идентификатор == уред_идентификатор) {
                return 후보;
            }
        }
        return null;
    }
}

