// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Somalia.JSomOS.kifaa_thamani;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI kifaa_thamani 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class kipembezo_basi_msimamizi {
    public static final class kifaa_thamani {
        private final int mchuuzi_kitambulishi;
        private final int kifaa_kitambulishi;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public kifaa_thamani(int mchuuzi_kitambulishi, int kifaa_kitambulishi, int 입출력바탕, int 개입중단번호) {
            this.mchuuzi_kitambulishi = mchuuzi_kitambulishi;
            this.kifaa_kitambulishi = kifaa_kitambulishi;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int mchuuzi_kitambulishi() { return mchuuzi_kitambulishi; }
        public int kifaa_kitambulishi() { return kifaa_kitambulishi; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<kifaa_thamani> Vifaa_Orodha = new ArrayList<kifaa_thamani>();

    public void 발견(kifaa_thamani kifaa_thamani) {
        Vifaa_Orodha.add(kifaa_thamani);
    }

    public List<kifaa_thamani> Vifaa_Orodha() {
        return Collections.unmodifiableList(Vifaa_Orodha);
    }

    public kifaa_thamani gundua_ingizo(int mchuuzi_kitambulishi, int kifaa_kitambulishi) {
        for (kifaa_thamani 후보 : Vifaa_Orodha) {
            if (후보.mchuuzi_kitambulishi == mchuuzi_kitambulishi && 후보.kifaa_kitambulishi == kifaa_kitambulishi) {
                return 후보;
            }
        }
        return null;
    }
}

