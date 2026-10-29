// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COD.JCodOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 imimerere_agaciro igice_agaciro 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Imbuganyuma_agaciro;
        private final int 한계;
        private final int kwinjira_agaciro;

        조각(int Imbuganyuma_agaciro, int 한계, int kwinjira_agaciro) {
            this.Imbuganyuma_agaciro = Imbuganyuma_agaciro;
            this.한계 = 한계;
            this.kwinjira_agaciro = kwinjira_agaciro;
        }

        public int Imbuganyuma_agaciro() { return Imbuganyuma_agaciro; }
        public int 한계() { return 한계; }
        public int kwinjira_agaciro() { return kwinjira_agaciro; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int 추가(int Imbuganyuma_agaciro, int 한계, int kwinjira_agaciro) {
        조각들.add(new 조각(Imbuganyuma_agaciro, 한계, kwinjira_agaciro));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void itsinda_agaciro_gasanzweho() {
        조각들.clear();
        추가(0, 0, 0);
        추가(0, 0xfffff, 0x9a);
        추가(0, 0xfffff, 0x92);
        추가(0, 0xfffff, 0xfa);
        추가(0, 0xfffff, 0xf2);
    }
}

