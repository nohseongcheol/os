// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Estados_Unidos.JUsaOS.device_VALUE;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI device_VALUE 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class aksesorya_bus_tagapamahala {
    public static final class device_VALUE {
        private final int vendor_tagakilala;
        private final int device_tagakilala;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public device_VALUE(int vendor_tagakilala, int device_tagakilala, int 입출력바탕, int 개입중단번호) {
            this.vendor_tagakilala = vendor_tagakilala;
            this.device_tagakilala = device_tagakilala;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int vendor_tagakilala() { return vendor_tagakilala; }
        public int device_tagakilala() { return device_tagakilala; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<device_VALUE> Mga_Device_list = new ArrayList<device_VALUE>();

    public void 발견(device_VALUE device_VALUE) {
        Mga_Device_list.add(device_VALUE);
    }

    public List<device_VALUE> Mga_Device_list() {
        return Collections.unmodifiableList(Mga_Device_list);
    }

    public device_VALUE FIND_pagpasok(int vendor_tagakilala, int device_tagakilala) {
        for (device_VALUE 후보 : Mga_Device_list) {
            if (후보.vendor_tagakilala == vendor_tagakilala && 후보.device_tagakilala == device_tagakilala) {
                return 후보;
            }
        }
        return null;
    }
}

