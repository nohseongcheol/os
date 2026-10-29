// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 ବିଭାଗ_ମୂଲ୍ୟ 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ;
        private final int 한계;
        private final int ପ୍ରବେଶ_ମୂଲ୍ୟ;

        조각(int ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ, int 한계, int ପ୍ରବେଶ_ମୂଲ୍ୟ) {
            this.ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ = ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ;
            this.한계 = 한계;
            this.ପ୍ରବେଶ_ମୂଲ୍ୟ = ପ୍ରବେଶ_ମୂଲ୍ୟ;
        }

        public int ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ() { return ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ; }
        public int 한계() { return 한계; }
        public int ପ୍ରବେଶ_ମୂଲ୍ୟ() { return ପ୍ରବେଶ_ମୂଲ୍ୟ; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ, int 한계, int ପ୍ରବେଶ_ମୂଲ୍ୟ) {
        조각들.add(new 조각(ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ, 한계, ପ୍ରବେଶ_ମୂଲ୍ୟ));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ସେଟ୍_ଡିଫଲ୍ଟ_ମାନ() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

