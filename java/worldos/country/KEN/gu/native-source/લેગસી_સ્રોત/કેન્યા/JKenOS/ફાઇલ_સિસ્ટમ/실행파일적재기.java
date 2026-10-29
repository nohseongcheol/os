// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેન્યા.JKenOS.ફાઇલ_સિસ્ટમ;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian અમલ_કરો_આદેશ 파일의 머리부와 적재 구역을 검증한다. */
public final class 실행파일적재기 {
    public static final class અનુભાગ_મૂલ્ય {
        private final int 종류;
        private final int ફ્લેગ_મૂલ્ય;
        private final int સરનામું;
        private final int ફાઇલ_સ્થિતિ_2aa21a9a;
        private final int માપ;

        અનુભાગ_મૂલ્ય(int 종류, int ફ્લેગ_મૂલ્ય, int સરનામું, int ફાઇલ_સ્થિતિ_2aa21a9a, int માપ) {
            this.종류 = 종류;
            this.ફ્લેગ_મૂલ્ય = ફ્લેગ_મૂલ્ય;
            this.સરનામું = સરનામું;
            this.ફાઇલ_સ્થિતિ_2aa21a9a = ફાઇલ_સ્થિતિ_2aa21a9a;
            this.માપ = માપ;
        }

        public int 종류() {
            return 종류;
        }

        public int ફ્લેગ_મૂલ્ય() {
            return ફ્લેગ_મૂલ્ય;
        }

        public int સરનામું() {
            return સરનામું;
        }

        public int ફાઇલ_સ્થિતિ_2aa21a9a() {
            return ફાઇલ_સ્થિતિ_2aa21a9a;
        }

        public int માપ() {
            return માપ;
        }
    }

    public static final class છબી {
        private final int પ્રારંભ_સરનામું;
        private final List<અનુભાગ_મૂલ્ય> 구역들;

        છબી(int પ્રારંભ_સરનામું, List<અનુભાગ_મૂલ્ય> 구역들) {
            this.પ્રારંભ_સરનામું = પ્રારંભ_સરનામું;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int પ્રારંભ_સરનામું() {
            return પ્રારંભ_સરનામું;
        }

        public List<અનુભાગ_મૂલ્ય> 구역들() {
            return 구역들;
        }
    }

    public છબી 검사(byte[] ડેટા) {
        if (ડેટા == null || ડેટા.length < 52
                || ડેટા[0] != 0x7f || ડેટા[1] != 'E' || ડેટા[2] != 'L' || ડેટા[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (ડેટા[4] != 1 || ડેટા[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int પ્રારંભ_સરનામું = પાર્સ_કરો_પૂર્ણાંક(ડેટા, 24);
        int અનુભાગ_કોષ્ટક_સ્થિતિ = પાર્સ_કરો_પૂર્ણાંક(ડેટા, 32);
        int અનુભાગ_પ્રવેશ_આકાર = 짧은정수읽기(ડેટા, 46);
        int 구역수 = 짧은정수읽기(ડેટા, 48);
        if (અનુભાગ_પ્રવેશ_આકાર < 40 || અનુભાગ_કોષ્ટક_સ્થિતિ < 0
                || (long) અનુભાગ_કોષ્ટક_સ્થિતિ + (long) અનુભાગ_પ્રવેશ_આકાર * 구역수 > ડેટા.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<અનુભાગ_મૂલ્ય> 구역들 = new ArrayList<અનુભાગ_મૂલ્ય>();
        for (int અનુક્રમણિકા = 0; અનુક્રમણિકા < 구역수; અનુક્રમણિકા++) {
            int સ્થાન = અનુભાગ_કોષ્ટક_સ્થિતિ + અનુક્રમણિકા * અનુભાગ_પ્રવેશ_આકાર;
            int 종류 = પાર્સ_કરો_પૂર્ણાંક(ડેટા, સ્થાન + 4);
            int ફ્લેગ_મૂલ્ય = પાર્સ_કરો_પૂર્ણાંક(ડેટા, સ્થાન + 8);
            int સરનામું = પાર્સ_કરો_પૂર્ણાંક(ડેટા, સ્થાન + 12);
            int ફાઇલ_સ્થિતિ_2aa21a9a = પાર્સ_કરો_પૂર્ણાંક(ડેટા, સ્થાન + 16);
            int માપ = પાર્સ_કરો_પૂર્ણાંક(ડેટા, સ્થાન + 20);
            if (માપ < 0 || (종류 != 8 && ((long) ફાઇલ_સ્થિતિ_2aa21a9a + માપ > ડેટા.length || ફાઇલ_સ્થિતિ_2aa21a9a < 0))) {
                throw new IllegalArgumentException("ELF અનુભાગ_મૂલ્ય ડેટા 범위가 올바르지 않습니다.");
            }
            구역들.add(new અનુભાગ_મૂલ્ય(종류, ફ્લેગ_મૂલ્ય, સરનામું, ફાઇલ_સ્થિતિ_2aa21a9a, માપ));
        }
        return new છબી(પ્રારંભ_સરનામું, 구역들);
    }

    private int પાર્સ_કરો_પૂર્ણાંક(byte[] ડેટા, int સ્થાન) {
        if (સ્થાન < 0 || સ્થાન > ડેટા.length - 4) {
            throw new IllegalArgumentException("ELF પૂર્ણાંક 범위를 벗어났습니다.");
        }
        return (ડેટા[સ્થાન] & 0xff)
                | ((ડેટા[સ્થાન + 1] & 0xff) << 8)
                | ((ડેટા[સ્થાન + 2] & 0xff) << 16)
                | ((ડેટા[સ્થાન + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] ડેટા, int સ્થાન) {
        if (સ્થાન < 0 || સ્થાન > ડેટા.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 પૂર્ણાંક 범위를 벗어났습니다.");
        }
        return (ડેટા[સ્થાન] & 0xff) | ((ડેટા[સ્થાન + 1] & 0xff) << 8);
    }
}
