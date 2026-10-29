// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.құрылғы_мән;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI құрылғы_мән 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class периферия_құрылғысы_шина_менеджер {
    public static final class құрылғы_мән {
        private final int жеткізуші_идентификатор;
        private final int құрылғы_идентификатор;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public құрылғы_мән(int жеткізуші_идентификатор, int құрылғы_идентификатор, int 입출력바탕, int 개입중단번호) {
            this.жеткізуші_идентификатор = жеткізуші_идентификатор;
            this.құрылғы_идентификатор = құрылғы_идентификатор;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int жеткізуші_идентификатор() { return жеткізуші_идентификатор; }
        public int құрылғы_идентификатор() { return құрылғы_идентификатор; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<құрылғы_мән> Құрылғылар_Тізім = new ArrayList<құрылғы_мән>();

    public void 발견(құрылғы_мән құрылғы_мән) {
        Құрылғылар_Тізім.add(құрылғы_мән);
    }

    public List<құрылғы_мән> Құрылғылар_Тізім() {
        return Collections.unmodifiableList(Құрылғылар_Тізім);
    }

    public құрылғы_мән Табу_енгізу(int жеткізуші_идентификатор, int құрылғы_идентификатор) {
        for (құрылғы_мән 후보 : Құрылғылар_Тізім) {
            if (후보.жеткізуші_идентификатор == жеткізуші_идентификатор && 후보.құрылғы_идентификатор == құрылғы_идентификатор) {
                return 후보;
            }
        }
        return null;
    }
}

