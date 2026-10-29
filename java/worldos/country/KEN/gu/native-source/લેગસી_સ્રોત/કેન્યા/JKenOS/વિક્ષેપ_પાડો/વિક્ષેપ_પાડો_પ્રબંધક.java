// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેન્યા.JKenOS.વિક્ષેપ_પાડો;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class વિક્ષેપ_પાડો_પ્રબંધક {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean સક્રિય;

    public void રજિસ્ટર_કરો_પ્રવેશ(int અનુક્રમણિકા, 개입중단처리기 처리기) {
        번호확인(અનુક્રમણિકા);
        처리기들[અનુક્રમણિકા] = 처리기;
    }

    public void રિલીઝ_સંગ્રહ(int અનુક્રમણિકા) {
        번호확인(અનુક્રમણિકા);
        처리기들[અનુક્રમણિકા] = null;
    }

    public int વિતરિત_કરો_મૂલ્ય(int અનુક્રમણિકા, int 저장된쌓임주소) {
        번호확인(અનુક્રમણિકા);
        if (!સક્રિય) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[અનુક્રમણિકા];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.પ્રક્રિયા_મૂલ્ય_પ્રવેશ(저장된쌓임주소);
    }

    public void ચાલુ_કરો() {
        સક્રિય = true;
    }

    public void નિષ્ક્રિય_કરો() {
        સક્રિય = false;
    }

    public boolean ઇન્ટરમિટેંટ_સક્રિય() {
        return સક્રિય;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int અનુક્રમણિકા) {
        if (અનુક્રમણિકા < 0 || અનુક્રમણિકા >= 처리기들.length) {
            throw new IllegalArgumentException("વિક્ષેપ_પાડો 번호가 올바르지 않습니다.");
        }
    }
}

