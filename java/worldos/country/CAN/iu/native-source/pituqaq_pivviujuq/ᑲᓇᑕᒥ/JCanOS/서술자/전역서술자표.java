// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 qanuilinganiq_atuutilik sukuttia_atuutilik 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ungataa_atuutilik;
        private final int 한계;
        private final int pili_atuutilik;

        조각(int ungataa_atuutilik, int 한계, int pili_atuutilik) {
            this.ungataa_atuutilik = ungataa_atuutilik;
            this.한계 = 한계;
            this.pili_atuutilik = pili_atuutilik;
        }

        public int ungataa_atuutilik() { return ungataa_atuutilik; }
        public int 한계() { return 한계; }
        public int pili_atuutilik() { return pili_atuutilik; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ungataa_atuutilik, int 한계, int pili_atuutilik) {
        조각들.add(new 조각(ungataa_atuutilik, 한계, pili_atuutilik));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void attiqsimaniit_Aturniliuvagiiqtut() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

