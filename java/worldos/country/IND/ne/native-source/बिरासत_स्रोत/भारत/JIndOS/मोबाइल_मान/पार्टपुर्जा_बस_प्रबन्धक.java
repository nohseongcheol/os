// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.मोबाइल_मान;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI मोबाइल_मान 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class पार्टपुर्जा_बस_प्रबन्धक {
    public static final class मोबाइल_मान {
        private final int 판매자식별자;
        private final int मोबाइल_परिचायक;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public मोबाइल_मान(int 판매자식별자, int मोबाइल_परिचायक, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.मोबाइल_परिचायक = मोबाइल_परिचायक;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int मोबाइल_परिचायक() { return मोबाइल_परिचायक; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<मोबाइल_मान> यन्त्रहरू_सूची = new ArrayList<मोबाइल_मान>();

    public void 발견(मोबाइल_मान मोबाइल_मान) {
        यन्त्रहरू_सूची.add(मोबाइल_मान);
    }

    public List<मोबाइल_मान> यन्त्रहरू_सूची() {
        return Collections.unmodifiableList(यन्त्रहरू_सूची);
    }

    public मोबाइल_मान खोज_गर्नुहोस्_प्रविष्टि(int 판매자식별자, int मोबाइल_परिचायक) {
        for (मोबाइल_मान 후보 : यन्त्रहरू_सूची) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.मोबाइल_परिचायक == मोबाइल_परिचायक) {
                return 후보;
            }
        }
        return null;
    }
}

