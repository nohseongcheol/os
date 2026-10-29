// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package യുണൈറ്റഡ്_അറബ്_എമിറൈറ്റ്_സ്.JAreOS.മൊബൈൽ_മൂല്യം;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI മൊബൈൽ_മൂല്യം 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class സഹായകം_ബസ്_മാനേജര് {
    public static final class മൊബൈൽ_മൂല്യം {
        private final int വെണ്ടർ_ఐడెంటిఫయర్;
        private final int മൊബൈൽ_ఐడెంటిఫయర్;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public മൊബൈൽ_മൂല്യം(int വെണ്ടർ_ఐడెంటిఫయర్, int മൊബൈൽ_ఐడెంటిఫయర్, int 입출력바탕, int 개입중단번호) {
            this.വെണ്ടർ_ఐడెంటిఫయర్ = വെണ്ടർ_ఐడెంటిఫయర్;
            this.മൊബൈൽ_ఐడెంటిఫయర్ = മൊബൈൽ_ఐడెంటిఫయర్;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int വെണ്ടർ_ఐడెంటిఫయర్() { return വെണ്ടർ_ఐడెంటిఫయర్; }
        public int മൊബൈൽ_ఐడెంటిఫయర్() { return മൊബൈൽ_ఐడెంటిఫయర్; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<മൊബൈൽ_മൂല്യം> ഉപാധികള്_ലിസ്റ്റ് = new ArrayList<മൊബൈൽ_മൂല്യം>();

    public void 발견(മൊബൈൽ_മൂല്യം മൊബൈൽ_മൂല്യം) {
        ഉപാധികള്_ലിസ്റ്റ്.add(മൊബൈൽ_മൂല്യം);
    }

    public List<മൊബൈൽ_മൂല്യം> ഉപാധികള്_ലിസ്റ്റ്() {
        return Collections.unmodifiableList(ഉപാധികള്_ലിസ്റ്റ്);
    }

    public മൊബൈൽ_മൂല്യം കണ്ടെത്തുക_എന്_ട്രി(int വെണ്ടർ_ఐడెంటిఫయర్, int മൊബൈൽ_ఐడెంటిఫయర్) {
        for (മൊബൈൽ_മൂല്യം 후보 : ഉപാധികള്_ലിസ്റ്റ്) {
            if (후보.വെണ്ടർ_ఐడెంటిఫయర్ == വെണ്ടർ_ఐడెంటిఫయర్ && 후보.മൊബൈൽ_ఐడెంటిఫయర్ == മൊബൈൽ_ఐడెంటిఫయర్) {
                return 후보;
            }
        }
        return null;
    }
}

