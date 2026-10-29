// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.मोबायल_मोल;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI मोबायल_मोल 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class एक्सेसरी_बस_वेवस्थापक {
    public static final class मोबायल_मोल {
        private final int 판매자식별자;
        private final int मोबायल_वळखुपी;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public मोबायल_मोल(int 판매자식별자, int मोबायल_वळखुपी, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.मोबायल_वळखुपी = मोबायल_वळखुपी;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int मोबायल_वळखुपी() { return मोबायल_वळखुपी; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<मोबायल_मोल> डिव्हायस_सुची = new ArrayList<मोबायल_मोल>();

    public void 발견(मोबायल_मोल मोबायल_मोल) {
        डिव्हायस_सुची.add(मोबायल_मोल);
    }

    public List<मोबायल_मोल> डिव्हायस_सुची() {
        return Collections.unmodifiableList(डिव्हायस_सुची);
    }

    public मोबायल_मोल FIND_प्रवेश(int 판매자식별자, int मोबायल_वळखुपी) {
        for (मोबायल_मोल 후보 : डिव्हायस_सुची) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.मोबायल_वळखुपी == मोबायल_वळखुपी) {
                return 후보;
            }
        }
        return null;
    }
}

