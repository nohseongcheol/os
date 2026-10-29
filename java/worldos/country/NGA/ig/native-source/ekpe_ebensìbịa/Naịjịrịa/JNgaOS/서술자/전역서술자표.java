// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ọnọdụ_valuu nkebì_valuu 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Bakgraụnd_valuu;
        private final int 한계;
        private final int òhèrè_valuu;

        조각(int Bakgraụnd_valuu, int 한계, int òhèrè_valuu) {
            this.Bakgraụnd_valuu = Bakgraụnd_valuu;
            this.한계 = 한계;
            this.òhèrè_valuu = òhèrè_valuu;
        }

        public int Bakgraụnd_valuu() { return Bakgraụnd_valuu; }
        public int 한계() { return 한계; }
        public int òhèrè_valuu() { return òhèrè_valuu; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Bakgraụnd_valuu, int 한계, int òhèrè_valuu) {
        조각들.add(new 조각(Bakgraụnd_valuu, 한계, òhèrè_valuu));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void Seti_Ngwa_ihe_dịadị() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

