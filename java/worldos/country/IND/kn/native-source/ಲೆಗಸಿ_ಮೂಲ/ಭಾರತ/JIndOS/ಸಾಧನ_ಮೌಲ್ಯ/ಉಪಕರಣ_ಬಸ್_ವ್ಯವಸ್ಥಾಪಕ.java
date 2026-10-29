// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ಭಾರತ.JIndOS.ಸಾಧನ_ಮೌಲ್ಯ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ಸಾಧನ_ಮೌಲ್ಯ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ಉಪಕರಣ_ಬಸ್_ವ್ಯವಸ್ಥಾಪಕ {
    public static final class ಸಾಧನ_ಮೌಲ್ಯ {
        private final int ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ;
        private final int ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ಸಾಧನ_ಮೌಲ್ಯ(int ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ, int ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ, int 입출력바탕, int 개입중단번호) {
            this.ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ = ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ;
            this.ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ = ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ() { return ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ; }
        public int ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ() { return ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ಸಾಧನ_ಮೌಲ್ಯ> ಸಾಧನಗಳು_ಪಟ್ಟಿ = new ArrayList<ಸಾಧನ_ಮೌಲ್ಯ>();

    public void 발견(ಸಾಧನ_ಮೌಲ್ಯ ಸಾಧನ_ಮೌಲ್ಯ) {
        ಸಾಧನಗಳು_ಪಟ್ಟಿ.add(ಸಾಧನ_ಮೌಲ್ಯ);
    }

    public List<ಸಾಧನ_ಮೌಲ್ಯ> ಸಾಧನಗಳು_ಪಟ್ಟಿ() {
        return Collections.unmodifiableList(ಸಾಧನಗಳು_ಪಟ್ಟಿ);
    }

    public ಸಾಧನ_ಮೌಲ್ಯ ಹುಡುಕಿ_ನಮೂದು(int ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ, int ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ) {
        for (ಸಾಧನ_ಮೌಲ್ಯ 후보 : ಸಾಧನಗಳು_ಪಟ್ಟಿ) {
            if (후보.ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ == ಮಾರಾಟಗಾರರು_ಗುರುತಿಸುವಿಕೆ && 후보.ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ == ಸಾಧನ_ಗುರುತಿಸುವಿಕೆ) {
                return 후보;
            }
        }
        return null;
    }
}

