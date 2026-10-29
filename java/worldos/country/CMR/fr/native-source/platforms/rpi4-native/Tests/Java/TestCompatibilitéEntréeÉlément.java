// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** Ne pas choisir une méthode auxiliaire privée comme point d’entrée d’un programme possédant un main standard. */
public class TestCompatibilitéEntréeÉlément {
    private static void lancer() { System.out.println("valeurAuxiliaire Fonction invoquer"); }
    public static void main(String[] arguments) {
        lancer();
        System.out.println("표준 pointEntréeÉlément retenirValeur");
    }
}
