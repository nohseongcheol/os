// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેન્યા.JKenOS.સંગ્રહ_ડિવાઇસ;

import java.util.Arrays;

/** ATA 28비트 આદેશ 계층과 같은 512바이트 논리 અનુભાગ_મૂલ્ય 장치다. */
public final class 고급기술결합장치 {
    public static final int અનુભાગ_આકાર = 512;
    private final byte[] ડેટા;
    private final boolean ફક્ત_વાંચવા_માટે_મૂલ્ય;

    public 고급기술결합장치(int 구역수, boolean ફક્ત_વાંચવા_માટે_મૂલ્ય) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("અનુભાગ_મૂલ્ય 수가 올바르지 않습니다.");
        }
        ડેટા = new byte[Math.multiplyExact(구역수, અનુભાગ_આકાર)];
        this.ફક્ત_વાંચવા_માટે_મૂલ્ય = ફક્ત_વાંચવા_માટે_મૂલ્ય;
    }

    public int 구역수() {
        return ડેટા.length / અનુભાગ_આકાર;
    }

    public void વાંચો(int અનુભાગ_અનુક્રમણિકા, byte[] 받을곳) {
        범위확인(અનુભાગ_અનુક્રમણિકા, 받을곳);
        System.arraycopy(ડેટા, અનુભાગ_અનુક્રમણિકા * અનુભાગ_આકાર, 받을곳, 0, અનુભાગ_આકાર);
    }

    public void લખો(int અનુભાગ_અનુક્રમણિકા, byte[] 쓸자료) {
        if (ફક્ત_વાંચવા_માટે_મૂલ્ય) {
            throw new IllegalStateException("વાંચો 전용 장치입니다.");
        }
        범위확인(અનુભાગ_અનુક્રમણિકા, 쓸자료);
        System.arraycopy(쓸자료, 0, ડેટા, અનુભાગ_અનુક્રમણિકા * અનુભાગ_આકાર, અનુભાગ_આકાર);
    }

    public void 지우기() {
        if (ફક્ત_વાંચવા_માટે_મૂલ્ય) {
            throw new IllegalStateException("વાંચો 전용 장치입니다.");
        }
        Arrays.fill(ડેટા, (byte) 0);
    }

    private void 범위확인(int અનુભાગ_અનુક્રમણિકા, byte[] 임시공간) {
        if (અનુભાગ_અનુક્રમણિકા < 0 || અનુભાગ_અનુક્રમણિકા >= 구역수() || 임시공간.length < અનુભાગ_આકાર) {
            throw new IllegalArgumentException("ATA અનુભાગ_મૂલ્ય 범위가 올바르지 않습니다.");
        }
    }
}

