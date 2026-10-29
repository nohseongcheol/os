// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package EMzantsi_Afrika.JZafOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 imo_ixabiso icandelo_ixabiso 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Ngasemva_ixabiso;
        private final int 한계;
        private final int fikelela_ixabiso;

        조각(int Ngasemva_ixabiso, int 한계, int fikelela_ixabiso) {
            this.Ngasemva_ixabiso = Ngasemva_ixabiso;
            this.한계 = 한계;
            this.fikelela_ixabiso = fikelela_ixabiso;
        }

        public int Ngasemva_ixabiso() { return Ngasemva_ixabiso; }
        public int 한계() { return 한계; }
        public int fikelela_ixabiso() { return fikelela_ixabiso; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Ngasemva_ixabiso, int 한계, int fikelela_ixabiso) {
        조각들.add(new 조각(Ngasemva_ixabiso, 한계, fikelela_ixabiso));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void isethi_ixabiso_elisisiseko() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

