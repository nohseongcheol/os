// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኤርትራ.JEriOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ደረጃ_ዋጋ ክፋል_ዋጋ 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ድሕረባይታ_ዋጋ;
        private final int 한계;
        private final int ፍቓድ_ዋጋ_2dd0017b;

        조각(int ድሕረባይታ_ዋጋ, int 한계, int ፍቓድ_ዋጋ_2dd0017b) {
            this.ድሕረባይታ_ዋጋ = ድሕረባይታ_ዋጋ;
            this.한계 = 한계;
            this.ፍቓድ_ዋጋ_2dd0017b = ፍቓድ_ዋጋ_2dd0017b;
        }

        public int ድሕረባይታ_ዋጋ() { return ድሕረባይታ_ዋጋ; }
        public int 한계() { return 한계; }
        public int ፍቓድ_ዋጋ_2dd0017b() { return ፍቓድ_ዋጋ_2dd0017b; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ድሕረባይታ_ዋጋ, int 한계, int ፍቓድ_ዋጋ_2dd0017b) {
        조각들.add(new 조각(ድሕረባይታ_ዋጋ, 한계, ፍቓድ_ዋጋ_2dd0017b));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void እኩብ_ንቡር_ዋጋ() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

