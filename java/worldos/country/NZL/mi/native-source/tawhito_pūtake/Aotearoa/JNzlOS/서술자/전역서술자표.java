// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 tūnga_uara wāhanga_uara 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Papamuri_uara;
        private final int 한계;
        private final int uru_uara;

        조각(int Papamuri_uara, int 한계, int uru_uara) {
            this.Papamuri_uara = Papamuri_uara;
            this.한계 = 한계;
            this.uru_uara = uru_uara;
        }

        public int Papamuri_uara() { return Papamuri_uara; }
        public int 한계() { return 한계; }
        public int uru_uara() { return uru_uara; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Papamuri_uara, int 한계, int uru_uara) {
        조각들.add(new 조각(Papamuri_uara, 한계, uru_uara));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void huinga_uara_taunoa() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

