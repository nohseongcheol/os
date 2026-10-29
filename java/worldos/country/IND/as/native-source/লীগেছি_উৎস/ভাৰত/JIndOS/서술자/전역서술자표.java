// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ভাৰত.JIndOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 অৱস্থা_মান শাখা_মান_366e0bfa 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int পটভূমি_মান;
        private final int 한계;
        private final int প্ৰৱেশ_কৰক_মান;

        조각(int পটভূমি_মান, int 한계, int প্ৰৱেশ_কৰক_মান) {
            this.পটভূমি_মান = পটভূমি_মান;
            this.한계 = 한계;
            this.প্ৰৱেশ_কৰক_মান = প্ৰৱেশ_কৰক_মান;
        }

        public int পটভূমি_মান() { return পটভূমি_মান; }
        public int 한계() { return 한계; }
        public int প্ৰৱেশ_কৰক_মান() { return প্ৰৱেশ_কৰক_মান; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int পটভূমি_মান, int 한계, int প্ৰৱেশ_কৰক_মান) {
        조각들.add(new 조각(পটভূমি_মান, 한계, প্ৰৱেশ_কৰক_মান));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ছেট_ডিফ_ল্ট_মান() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

