// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkmenistan.JTkmOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ýagdaý_baha bölüm_baha_366e0bfa 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Fon_baha;
        private final int 한계;
        private final int ygtyýarlylyk_baha;

        조각(int Fon_baha, int 한계, int ygtyýarlylyk_baha) {
            this.Fon_baha = Fon_baha;
            this.한계 = 한계;
            this.ygtyýarlylyk_baha = ygtyýarlylyk_baha;
        }

        public int Fon_baha() { return Fon_baha; }
        public int 한계() { return 한계; }
        public int ygtyýarlylyk_baha() { return ygtyýarlylyk_baha; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Fon_baha, int 한계, int ygtyýarlylyk_baha) {
        조각들.add(new 조각(Fon_baha, 한계, ygtyýarlylyk_baha));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void köplük_öňünden_kabul_edilen_baha() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

