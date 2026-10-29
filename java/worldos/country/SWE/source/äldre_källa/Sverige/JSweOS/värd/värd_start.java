// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Sverige.JSweOS.värd;

import Sverige.JSweOS.kärna.kärna;

public final class värd_start {
    private värd_start() {
    }

    public static void main(String[] parameter_argument) {
        kärna kärna_värde = new kärna(new värd_maskinvara());
        kärna_värde.Kör();
        kärna_värde.köra_steg();
    }
}

