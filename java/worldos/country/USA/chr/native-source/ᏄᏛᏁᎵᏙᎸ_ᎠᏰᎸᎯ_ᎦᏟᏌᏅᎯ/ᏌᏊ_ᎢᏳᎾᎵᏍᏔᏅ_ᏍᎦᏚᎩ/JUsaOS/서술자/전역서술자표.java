// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ᏄᏍᏗᏓᏅ_ᏧᎬᏩᎶᏗᏯ ᎤᏓᎯᏢᎢ_ᏧᎬᏩᎶᏗᏯ 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ;
        private final int 한계;
        private final int ᎬᏴᏍᏗ_ᏧᎬᏩᎶᏗᏯ;

        조각(int ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ, int 한계, int ᎬᏴᏍᏗ_ᏧᎬᏩᎶᏗᏯ) {
            this.ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ = ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ;
            this.한계 = 한계;
            this.ᎬᏴᏍᏗ_ᏧᎬᏩᎶᏗᏯ = ᎬᏴᏍᏗ_ᏧᎬᏩᎶᏗᏯ;
        }

        public int ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ() { return ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ; }
        public int 한계() { return 한계; }
        public int ᎬᏴᏍᏗ_ᏧᎬᏩᎶᏗᏯ() { return ᎬᏴᏍᏗ_ᏧᎬᏩᎶᏗᏯ; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ, int 한계, int ᎬᏴᏍᏗ_ᏧᎬᏩᎶᏗᏯ) {
        조각들.add(new 조각(ᎠᏍᏆᏚᎸ_ᎦᏯᎸᏗ_ᏧᎬᏩᎶᏗᏯ, 한계, ᎬᏴᏍᏗ_ᏧᎬᏩᎶᏗᏯ));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ᎦᎪᏗ_ᎠᏓᏁᏟᏴᏍᏗᏍᎩ_ᏧᎬᏩᎶᏗᏯ() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

