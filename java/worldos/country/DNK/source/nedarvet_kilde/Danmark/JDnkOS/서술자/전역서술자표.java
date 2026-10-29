// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 status_VÆRDI sektion_VÆRDI 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Baggrund_VÆRDI;
        private final int 한계;
        private final int åbne_VÆRDI;

        조각(int Baggrund_VÆRDI, int 한계, int åbne_VÆRDI) {
            this.Baggrund_VÆRDI = Baggrund_VÆRDI;
            this.한계 = 한계;
            this.åbne_VÆRDI = åbne_VÆRDI;
        }

        public int Baggrund_VÆRDI() { return Baggrund_VÆRDI; }
        public int 한계() { return 한계; }
        public int åbne_VÆRDI() { return åbne_VÆRDI; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int tilføj_post(int Baggrund_VÆRDI, int 한계, int åbne_VÆRDI) {
        조각들.add(new 조각(Baggrund_VÆRDI, 한계, åbne_VÆRDI));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void sæt_standardværdi() {
        조각들.clear();
        tilføj_post(0, 0, 0);
        tilføj_post(0, 0xfffff, 0x9a);
        tilføj_post(0, 0xfffff, 0x92);
        tilføj_post(0, 0xfffff, 0xfa);
        tilføj_post(0, 0xfffff, 0xf2);
    }
}

