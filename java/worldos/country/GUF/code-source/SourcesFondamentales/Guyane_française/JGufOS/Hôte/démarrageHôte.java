// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Guyane_française.JGufOS.Hôte;

import Guyane_française.JGufOS.Noyau.Noyau;

public final class démarrageHôte {
    private démarrageHôte() {
    }

    public static void main(String[] argumentParamètre) {
        Noyau valeurNoyau = new Noyau(new MatérielHôte());
        valeurNoyau.lancer();
        valeurNoyau.exécuterÉtape();
    }
}

