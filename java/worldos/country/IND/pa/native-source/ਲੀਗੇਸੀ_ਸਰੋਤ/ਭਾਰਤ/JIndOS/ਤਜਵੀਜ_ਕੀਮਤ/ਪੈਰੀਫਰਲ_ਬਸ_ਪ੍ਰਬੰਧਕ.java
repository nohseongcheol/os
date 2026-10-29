// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਭਾਰਤ.JIndOS.ਤਜਵੀਜ_ਕੀਮਤ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** PCI ਤਜਵੀਜ_ਕੀਮਤ 검색 결과와 BAR/IRQ 값을 관리한다. */
public final class ਪੈਰੀਫਰਲ_ਬਸ_ਪ੍ਰਬੰਧਕ {
    public static final class ਤਜਵੀਜ_ਕੀਮਤ {
        private final int 판매자식별자;
        private final int ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ;
        private final int 입출력바탕;
        private final int 개입중단번호;

        public ਤਜਵੀਜ_ਕੀਮਤ(int 판매자식별자, int ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ, int 입출력바탕, int 개입중단번호) {
            this.판매자식별자 = 판매자식별자;
            this.ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ = ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ;
            this.입출력바탕 = 입출력바탕;
            this.개입중단번호 = 개입중단번호;
        }

        public int 판매자식별자() { return 판매자식별자; }
        public int ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ() { return ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ; }
        public int 입출력바탕() { return 입출력바탕; }
        public int 개입중단번호() { return 개입중단번호; }
    }

    private final List<ਤਜਵੀਜ_ਕੀਮਤ> ਡਿਵਾਇਸ_ਸੂਚੀ = new ArrayList<ਤਜਵੀਜ_ਕੀਮਤ>();

    public void 발견(ਤਜਵੀਜ_ਕੀਮਤ ਤਜਵੀਜ_ਕੀਮਤ) {
        ਡਿਵਾਇਸ_ਸੂਚੀ.add(ਤਜਵੀਜ_ਕੀਮਤ);
    }

    public List<ਤਜਵੀਜ_ਕੀਮਤ> ਡਿਵਾਇਸ_ਸੂਚੀ() {
        return Collections.unmodifiableList(ਡਿਵਾਇਸ_ਸੂਚੀ);
    }

    public ਤਜਵੀਜ_ਕੀਮਤ ਲੱਭੋ_ਦਾਖਲਾ(int 판매자식별자, int ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ) {
        for (ਤਜਵੀਜ_ਕੀਮਤ 후보 : ਡਿਵਾਇਸ_ਸੂਚੀ) {
            if (후보.판매자식별자 == 판매자식별자 && 후보.ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ == ਤਜਵੀਜ_ਤਫ਼ਤੀਸ਼_ਕਰਨ_ਵਾਲਾ) {
                return 후보;
            }
        }
        return null;
    }
}

