// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Тоҷикистон.JTjkOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 вазъият_қимат қисмат_қимат 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Пасзамина_қимат;
        private final int 한계;
        private final int дастрасӣ_қимат;

        조각(int Пасзамина_қимат, int 한계, int дастрасӣ_қимат) {
            this.Пасзамина_қимат = Пасзамина_қимат;
            this.한계 = 한계;
            this.дастрасӣ_қимат = дастрасӣ_қимат;
        }

        public int Пасзамина_қимат() { return Пасзамина_қимат; }
        public int 한계() { return 한계; }
        public int дастрасӣ_қимат() { return дастрасӣ_қимат; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Пасзамина_қимат, int 한계, int дастрасӣ_қимат) {
        조각들.add(new 조각(Пасзамина_қимат, 한계, дастрасӣ_қимат));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void маҷмуъ_қимати_пешфарз() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

