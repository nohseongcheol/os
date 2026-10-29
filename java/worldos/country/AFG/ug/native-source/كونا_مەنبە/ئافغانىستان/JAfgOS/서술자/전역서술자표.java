// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ئافغانىستان.JAfgOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ھالەت_قىممىتى بۆلۈم_قىممىتى 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int تەگلىك_قىممىتى;
        private final int 한계;
        private final int زىيارەت_قىممىتى;

        조각(int تەگلىك_قىممىتى, int 한계, int زىيارەت_قىممىتى) {
            this.تەگلىك_قىممىتى = تەگلىك_قىممىتى;
            this.한계 = 한계;
            this.زىيارەت_قىممىتى = زىيارەت_قىممىتى;
        }

        public int تەگلىك_قىممىتى() { return تەگلىك_قىممىتى; }
        public int 한계() { return 한계; }
        public int زىيارەت_قىممىتى() { return زىيارەت_قىممىتى; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int تەگلىك_قىممىتى, int 한계, int زىيارەت_قىممىتى) {
        조각들.add(new 조각(تەگلىك_قىممىتى, 한계, زىيارەت_قىممىتى));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void توپ_سۈكۈتتىكى_قىممەت() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

