// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Svalbard_og_Jan_Mayen.JSjmOS.vert;

import Svalbard_og_Jan_Mayen.JSjmOS.kjerne.kjerne;

public final class vert_oppstart {
    private vert_oppstart() {
    }

    public static void main(String[] parameter_argument) {
        kjerne kjerne_VERDI = new kjerne(new vert_maskinvare());
        kjerne_VERDI.Kjør_2();
        kjerne_VERDI.Utfør_trinn();
    }
}

