// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ελλάδα.JGrcOS.συσκευή_τιμή;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI συσκευή_τιμή 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class βοήθημα_δίαυλος_Υπεύθυνος {
    public static final class συσκευή_τιμή {
        private final int προμηθευτής_αναγνωριστικό;
        private final int συσκευή_αναγνωριστικό;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public συσκευή_τιμή(int προμηθευτής_αναγνωριστικό, int συσκευή_αναγνωριστικό, int 입출력바탕, int 개입중단번호) {
            this.προμηθευτής_αναγνωριστικό = προμηθευτής_αναγνωριστικό;
            this.συσκευή_αναγνωριστικό = συσκευή_αναγνωριστικό;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int προμηθευτής_αναγνωριστικό() { return προμηθευτής_αναγνωριστικό; }
        public int συσκευή_αναγνωριστικό() { return συσκευή_αναγνωριστικό; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<συσκευή_τιμή> Συσκευές_Λίστα = new ArrayList<συσκευή_τιμή>();

    public void 발견(συσκευή_τιμή συσκευή_τιμή) {
        Συσκευές_Λίστα.add(συσκευή_τιμή);
    }

    public List<συσκευή_τιμή> Συσκευές_Λίστα() {
        return Collections.unmodifiableList(Συσκευές_Λίστα);
    }

    public συσκευή_τιμή Βρες_καταχώρηση(int προμηθευτής_αναγνωριστικό, int συσκευή_αναγνωριστικό) {
        for (συσκευή_τιμή 후보 : Συσκευές_Λίστα) {
            if (후보.προμηθευτής_αναγνωριστικό == προμηθευτής_αναγνωριστικό && 후보.συσκευή_αναγνωριστικό == συσκευή_αναγνωριστικό) {
                return 후보;
            }
        }
        return null;
    }
}

