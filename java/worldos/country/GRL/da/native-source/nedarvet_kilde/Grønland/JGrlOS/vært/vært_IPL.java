// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Grønland.JGrlOS.vært;

import Grønland.JGrlOS.kerne.kerne;

public final class vært_IPL {
    private vært_IPL() {
    }

    public static void main(String[] parameter_argument) {
        kerne kerne_VÆRDI = new kerne(new vært_hardware());
        kerne_VÆRDI.Kør_2();
        kerne_VÆRDI.Udfør_trin();
    }
}

