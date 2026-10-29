// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਕੈਨੇਡਾ.JCanOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 ਸਥਿਤੀ_ਕੀਮਤ ਵਿਭਾਗ_ਕੀਮਤ 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int ਪਿਛੋਕੜ_ਕੀਮਤ;
        private final int 한계;
        private final int ਐਕਸੈਸ_ਕੀਮਤ;

        조각(int ਪਿਛੋਕੜ_ਕੀਮਤ, int 한계, int ਐਕਸੈਸ_ਕੀਮਤ) {
            this.ਪਿਛੋਕੜ_ਕੀਮਤ = ਪਿਛੋਕੜ_ਕੀਮਤ;
            this.한계 = 한계;
            this.ਐਕਸੈਸ_ਕੀਮਤ = ਐਕਸੈਸ_ਕੀਮਤ;
        }

        public int ਪਿਛੋਕੜ_ਕੀਮਤ() { return ਪਿਛੋਕੜ_ਕੀਮਤ; }
        public int 한계() { return 한계; }
        public int ਐਕਸੈਸ_ਕੀਮਤ() { return ਐਕਸੈਸ_ਕੀਮਤ; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int ਪਿਛੋਕੜ_ਕੀਮਤ, int 한계, int ਐਕਸੈਸ_ਕੀਮਤ) {
        조각들.add(new 조각(ਪਿਛੋਕੜ_ਕੀਮਤ, 한계, ਐਕਸੈਸ_ਕੀਮਤ));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void ਸੈਟ_ਡਿਫੌਲਟ_ਵੈਲਯੂ() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

