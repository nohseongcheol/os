// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package NAM.JNamOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 kemo_Boleng karolo_Boleng 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Lemorago_Boleng;
        private final int 한계;
        private final int letlelesega_Boleng;

        조각(int Lemorago_Boleng, int 한계, int letlelesega_Boleng) {
            this.Lemorago_Boleng = Lemorago_Boleng;
            this.한계 = 한계;
            this.letlelesega_Boleng = letlelesega_Boleng;
        }

        public int Lemorago_Boleng() { return Lemorago_Boleng; }
        public int 한계() { return 한계; }
        public int letlelesega_Boleng() { return letlelesega_Boleng; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Lemorago_Boleng, int 한계, int letlelesega_Boleng) {
        조각들.add(new 조각(Lemorago_Boleng, 한계, letlelesega_Boleng));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void sete_boleng_jo_bo_rulaganyeditsweng_ruri() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

