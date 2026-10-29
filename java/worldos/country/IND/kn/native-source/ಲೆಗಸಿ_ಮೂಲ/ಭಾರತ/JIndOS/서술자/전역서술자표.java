// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ಸ್ಥಿತಿ_ಮೌಲ್ಯ ವಿಭಾಗ_ಮೌಲ್ಯ 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ;
        private final int 한계;
        private final int ಪ್ರವೇಶ_ಮೌಲ್ಯ;

        조각(int ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ, int 한계, int ಪ್ರವೇಶ_ಮೌಲ್ಯ) {
            this.ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ = ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ;
            this.한계 = 한계;
            this.ಪ್ರವೇಶ_ಮೌಲ್ಯ = ಪ್ರವೇಶ_ಮೌಲ್ಯ;
        }

        public int ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ() { return ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ; }
        public int 한계() { return 한계; }
        public int ಪ್ರವೇಶ_ಮೌಲ್ಯ() { return ಪ್ರವೇಶ_ಮೌಲ್ಯ; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ, int 한계, int ಪ್ರವೇಶ_ಮೌಲ್ಯ) {
        조각들.add(new 조각(ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ, 한계, ಪ್ರವೇಶ_ಮೌಲ್ಯ));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ಸೆಟ್_ಅಕ್ಷಮ_ಬೆಲೆ() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

