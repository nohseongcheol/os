// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package કેન્યા.JKenOS.હોસ્ટ;

import કેન્યા.JKenOS.કર્નેલ.કર્નેલ;

public final class હોસ્ટ_બૂટ {
    private હોસ્ટ_બૂટ() {
    }

    public static void main(String[] પેરામીટર_દલીલ) {
        કર્નેલ કર્નેલ_મૂલ્ય = new કર્નેલ(new હોસ્ટ_હાર્ડવેર());
        કર્નેલ_મૂલ્ય.ચલાવો_2();
        કર્નેલ_મૂલ્ય.한단계실행();
    }
}

