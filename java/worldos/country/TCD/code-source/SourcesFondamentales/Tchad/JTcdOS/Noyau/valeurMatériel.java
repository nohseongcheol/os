// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Tchad.JTcdOS.Noyau;

/** Seule frontière entre le noyau géré en Java et le code propre au processeur. */
public interface valeurMatériel {
    void sortieSériel(String valeurContenuValeur);

    int lireOctetPort(int numéroPortMatériel);

    void écrireOctetPort(int numéroPortMatériel, int valeur);

    void cPUArrêterMachine();
}

