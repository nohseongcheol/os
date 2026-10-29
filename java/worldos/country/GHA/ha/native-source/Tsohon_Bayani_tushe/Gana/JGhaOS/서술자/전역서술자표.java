// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Gana.JGhaOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Matsayi_Daraja Sashi_Daraja 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Bi_bango_Daraja;
        private final int 한계;
        private final int isa_Daraja;

        조각(int Bi_bango_Daraja, int 한계, int isa_Daraja) {
            this.Bi_bango_Daraja = Bi_bango_Daraja;
            this.한계 = 한계;
            this.isa_Daraja = isa_Daraja;
        }

        public int Bi_bango_Daraja() { return Bi_bango_Daraja; }
        public int 한계() { return 한계; }
        public int isa_Daraja() { return isa_Daraja; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Bi_bango_Daraja, int 한계, int isa_Daraja) {
        조각들.add(new 조각(Bi_bango_Daraja, 한계, isa_Daraja));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void zubi_Tanadaddiyar_daraja() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

