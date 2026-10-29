// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.መሳሪያ_እሴት;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI መሳሪያ_እሴት 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ማሟያ_ባስ_አስተዳዳሪ {
    public static final class መሳሪያ_እሴት {
        private final int አቅራቢ_መለያ;
        private final int መሳሪያ_መለያ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public መሳሪያ_እሴት(int አቅራቢ_መለያ, int መሳሪያ_መለያ, int 입출력바탕, int 개입중단번호) {
            this.አቅራቢ_መለያ = አቅራቢ_መለያ;
            this.መሳሪያ_መለያ = መሳሪያ_መለያ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int አቅራቢ_መለያ() { return አቅራቢ_መለያ; }
        public int መሳሪያ_መለያ() { return መሳሪያ_መለያ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<መሳሪያ_እሴት> መሳሪያዎች_ዝርዝር = new ArrayList<መሳሪያ_እሴት>();

    public void 발견(መሳሪያ_እሴት መሳሪያ_እሴት) {
        መሳሪያዎች_ዝርዝር.add(መሳሪያ_እሴት);
    }

    public List<መሳሪያ_እሴት> መሳሪያዎች_ዝርዝር() {
        return Collections.unmodifiableList(መሳሪያዎች_ዝርዝር);
    }

    public መሳሪያ_እሴት አግኝ_ምዝግብ(int አቅራቢ_መለያ, int መሳሪያ_መለያ) {
        for (መሳሪያ_እሴት 후보 : መሳሪያዎች_ዝርዝር) {
            if (후보.አቅራቢ_መለያ == አቅራቢ_መለያ && 후보.መሳሪያ_መለያ == መሳሪያ_መለያ) {
                return 후보;
            }
        }
        return null;
    }
}

