// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package საქართველო.JGeoOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 სტატუსი_მნიშვნელობა სექცია_მნიშვნელობა 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ფონი_მნიშვნელობა;
        private final int 한계;
        private final int წვდომა_მნიშვნელობა;

        조각(int ფონი_მნიშვნელობა, int 한계, int წვდომა_მნიშვნელობა) {
            this.ფონი_მნიშვნელობა = ფონი_მნიშვნელობა;
            this.한계 = 한계;
            this.წვდომა_მნიშვნელობა = წვდომა_მნიშვნელობა;
        }

        public int ფონი_მნიშვნელობა() { return ფონი_მნიშვნელობა; }
        public int 한계() { return 한계; }
        public int წვდომა_მნიშვნელობა() { return წვდომა_მნიშვნელობა; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ფონი_მნიშვნელობა, int 한계, int წვდომა_მნიშვნელობა) {
        조각들.add(new 조각(ფონი_მნიშვნელობა, 한계, წვდომა_მნიშვნელობა));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ნაკრები_ნაგულისხმევი_მნიშვნელობა() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

