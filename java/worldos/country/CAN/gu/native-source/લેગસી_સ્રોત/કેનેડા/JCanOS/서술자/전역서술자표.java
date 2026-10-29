// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેનેડા.JCanOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 સ્થિતિ_મૂલ્ય_e10195a1 અનુભાગ_મૂલ્ય 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int વૉલપેપર_મૂલ્ય;
        private final int 한계;
        private final int ઍક્સેસ_મૂલ્ય;

        조각(int વૉલપેપર_મૂલ્ય, int 한계, int ઍક્સેસ_મૂલ્ય) {
            this.વૉલપેપર_મૂલ્ય = વૉલપેપર_મૂલ્ય;
            this.한계 = 한계;
            this.ઍક્સેસ_મૂલ્ય = ઍક્સેસ_મૂલ્ય;
        }

        public int વૉલપેપર_મૂલ્ય() { return વૉલપેપર_મૂલ્ય; }
        public int 한계() { return 한계; }
        public int ઍક્સેસ_મૂલ્ય() { return ઍક્સેસ_મૂલ્ય; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int વૉલપેપર_મૂલ્ય, int 한계, int ઍક્સેસ_મૂલ્ય) {
        조각들.add(new 조각(વૉલપેપર_મૂલ્ય, 한계, ઍક્સેસ_મૂલ્ય));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void સેટ_ડિફૉલ્ટ_મૂલ્ય() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

