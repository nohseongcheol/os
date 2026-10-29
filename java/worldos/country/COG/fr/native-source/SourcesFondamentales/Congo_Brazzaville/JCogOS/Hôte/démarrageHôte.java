// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Congo_Brazzaville.JCogOS.Hôte;

import Congo_Brazzaville.JCogOS.Noyau.Noyau;

public final class démarrageHôte {
    private démarrageHôte() {
    }

    public static void main(String[] argumentParamètre) {
        Noyau valeurNoyau = new Noyau(new MatérielHôte());
        valeurNoyau.lancer();
        valeurNoyau.exécuterÉtape();
    }
}

