// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેનેડા.JCanOS.ફાઇલ_સિસ્ટમ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 ડિફૉલ્ટ_મૂલ્ય 분할 영역을 읽는다. */
public final class 기본분할영역표 {
    public static final class વિભાજન_મૂલ્ય {
        private final int 종류;
        private final long પ્રારંભ_અનુભાગ;
        private final long 구역수;

        વિભાજન_મૂલ્ય(int 종류, long પ્રારંભ_અનુભાગ, long 구역수) {
            this.종류 = 종류;
            this.પ્રારંભ_અનુભાગ = પ્રારંભ_અનુભાગ;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long પ્રારંભ_અનુભાગ() { return પ્રારંભ_અનુભાગ; }
        public long 구역수() { return 구역수; }
    }

    public List<વિભાજન_મૂલ્ય> વાંચો(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<વિભાજન_મૂલ્ય> પરિમાણ = new ArrayList<વિભાજન_મૂલ્ય>();
        for (int અનુક્રમણિકા = 0; અનુક્રમણિકા < 4; અનુક્રમણિકા++) {
            int સ્થાન = 446 + અનુક્રમણિકા * 16;
            int 종류 = 첫구역[સ્થાન + 4] & 0xff;
            long ચલાવો_2 = 작은순서정수(첫구역, સ્થાન + 8);
            long માપ = 작은순서정수(첫구역, સ્થાન + 12);
            if (종류 != 0 && માપ != 0) {
                પરિમાણ.add(new વિભાજન_મૂલ્ય(종류, ચલાવો_2, માપ));
            }
        }
        return Collections.unmodifiableList(પરિમાણ);
    }

    private long 작은순서정수(byte[] ડેટા, int સ્થાન) {
        return (ડેટા[સ્થાન] & 0xffL)
                | ((ડેટા[સ્થાન + 1] & 0xffL) << 8)
                | ((ડેટા[સ્થાન + 2] & 0xffL) << 16)
                | ((ડેટા[સ્થાન + 3] & 0xffL) << 24);
    }
}

