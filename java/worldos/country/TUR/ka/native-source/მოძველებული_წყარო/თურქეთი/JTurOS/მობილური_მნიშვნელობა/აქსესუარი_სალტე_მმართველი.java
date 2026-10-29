// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package თურქეთი.JTurOS.მობილური_მნიშვნელობა;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI მობილური_მნიშვნელობა 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class აქსესუარი_სალტე_მმართველი {
    public static final class მობილური_მნიშვნელობა {
        private final int 판매자식별자;
        private final int მობილური_იდენტიფიკატორი;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public მობილური_მნიშვნელობა(int 판매자식별자, int მობილური_იდენტიფიკატორი, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.მობილური_იდენტიფიკატორი = მობილური_იდენტიფიკატორი;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int მობილური_იდენტიფიკატორი() { return მობილური_იდენტიფიკატორი; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<მობილური_მნიშვნელობა> მოწყობილობები_სია = new ArrayList<მობილური_მნიშვნელობა>();

    public void 발견(მობილური_მნიშვნელობა მობილური_მნიშვნელობა) {
        მოწყობილობები_სია.add(მობილური_მნიშვნელობა);
    }

    public List<მობილური_მნიშვნელობა> მოწყობილობები_სია() {
        return Collections.unmodifiableList(მოწყობილობები_სია);
    }

    public მობილური_მნიშვნელობა ძებნა_შენატანი(int 판매자식별자, int მობილური_იდენტიფიკატორი) {
        for (მობილური_მნიშვნელობა 후보 : მოწყობილობები_სია) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.მობილური_იდენტიფიკატორი == მობილური_იდენტიფიკატორი) {
                return 후보;
            }
        }
        return null;
    }
}

