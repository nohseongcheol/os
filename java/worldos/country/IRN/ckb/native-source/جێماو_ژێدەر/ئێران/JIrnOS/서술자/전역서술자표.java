// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئێران.JIrnOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 دۆخ_نرخ بەش_نرخ 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int بن_زمینه_نرخ;
        private final int 한계;
        private final int دەسگەیشتن_نرخ;

        조각(int بن_زمینه_نرخ, int 한계, int دەسگەیشتن_نرخ) {
            this.بن_زمینه_نرخ = بن_زمینه_نرخ;
            this.한계 = 한계;
            this.دەسگەیشتن_نرخ = دەسگەیشتن_نرخ;
        }

        public int بن_زمینه_نرخ() { return بن_زمینه_نرخ; }
        public int 한계() { return 한계; }
        public int دەسگەیشتن_نرخ() { return دەسگەیشتن_نرخ; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int بن_زمینه_نرخ, int 한계, int دەسگەیشتن_نرخ) {
        조각들.add(new 조각(بن_زمینه_نرخ, 한계, دەسگەیشتن_نرخ));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void سێت_بەهای_گریمانە() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

