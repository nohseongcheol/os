// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.мобилӣ_қимат;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI мобилӣ_қимат 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class дастгоҳи_ҷонибӣ_гузаргоҳ_мудир {
    public static final class мобилӣ_қимат {
        private final int 판매자식별자;
        private final int мобилӣ_идентификатор;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public мобилӣ_қимат(int 판매자식별자, int мобилӣ_идентификатор, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.мобилӣ_идентификатор = мобилӣ_идентификатор;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int мобилӣ_идентификатор() { return мобилӣ_идентификатор; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<мобилӣ_қимат> Дастгоҳҳо_Рӯйхат = new ArrayList<мобилӣ_қимат>();

    public void 발견(мобилӣ_қимат мобилӣ_қимат) {
        Дастгоҳҳо_Рӯйхат.add(мобилӣ_қимат);
    }

    public List<мобилӣ_қимат> Дастгоҳҳо_Рӯйхат() {
        return Collections.unmodifiableList(Дастгоҳҳо_Рӯйхат);
    }

    public мобилӣ_қимат ёфтан_ворида(int 판매자식별자, int мобилӣ_идентификатор) {
        for (мобилӣ_қимат 후보 : Дастгоҳҳо_Рӯйхат) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.мобилӣ_идентификатор == мобилӣ_идентификатор) {
                return 후보;
            }
        }
        return null;
    }
}

