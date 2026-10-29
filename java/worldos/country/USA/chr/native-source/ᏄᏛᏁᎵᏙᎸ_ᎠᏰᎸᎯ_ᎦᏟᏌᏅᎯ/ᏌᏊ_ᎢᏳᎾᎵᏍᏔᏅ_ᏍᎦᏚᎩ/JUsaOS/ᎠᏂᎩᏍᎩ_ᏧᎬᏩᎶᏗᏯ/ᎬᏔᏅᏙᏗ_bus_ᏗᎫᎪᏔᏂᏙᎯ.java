// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ᎬᏔᏅᏙᏗ_bus_ᏗᎫᎪᏔᏂᏙᎯ {
    public static final class ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ {
        private final int 판매자식별자;
        private final int ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ(int 판매자식별자, int ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ = ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ() { return ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ> ᏥᏂᏕᎬᏅᏗᏓᎾ_ᏕᎦᏅᏅᏛ = new ArrayList<ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ>();

    public void 발견(ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ) {
        ᏥᏂᏕᎬᏅᏗᏓᎾ_ᏕᎦᏅᏅᏛ.add(ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ);
    }

    public List<ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ> ᏥᏂᏕᎬᏅᏗᏓᎾ_ᏕᎦᏅᏅᏛ() {
        return Collections.unmodifiableList(ᏥᏂᏕᎬᏅᏗᏓᎾ_ᏕᎦᏅᏅᏛ);
    }

    public ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ ᎯᏩᏔ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(int 판매자식별자, int ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ) {
        for (ᎠᏂᎩᏍᎩ_ᏧᎬᏩᎶᏗᏯ 후보 : ᏥᏂᏕᎬᏅᏗᏓᎾ_ᏕᎦᏅᏅᏛ) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ == ᎠᏂᎩᏍᎩ_ᎠᏓᏙᎵᎩ) {
                return 후보;
            }
        }
        return null;
    }
}

