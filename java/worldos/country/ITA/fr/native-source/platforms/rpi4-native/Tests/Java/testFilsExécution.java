// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
class valeurCompteur {
    int nombre;
    synchronized void ajouterValeurs() { int valeurAvantCôté = nombre; Thread.yield(); nombre = valeurAvantCôté + 1; }
}
class ActionTâche implements Runnable {
    valeurCompteur référenceCompteur; ActionTâche(valeurCompteur référenceCompteur) { this.référenceCompteur = référenceCompteur; }
    public void run() { for (int i = 0; i < 20; i++) référenceCompteur.ajouterValeurs(); }
}
class valeurFilExécution extends Thread { public void run() { synchronized (testFilsExécution.valeurVerrou) { testFilsExécution.estTerminé = 1; } } }
public class testFilsExécution {
    static Object valeurVerrou = new Object(); static int estTerminé;
    public static void main(String[] a) throws Exception {
        valeurCompteur référenceCompteur = new valeurCompteur(); Thread valeurUn = new Thread(new ActionTâche(référenceCompteur)); Thread valeurDeux = new Thread(new ActionTâche(référenceCompteur));
        valeurUn.start(); valeurDeux.start(); valeurUn.join(); valeurDeux.join(); System.out.println(référenceCompteur.nombre); System.out.println(valeurUn.isAlive());
        valeurFilExécution élémentListeTroisième = new valeurFilExécution(); élémentListeTroisième.start(); élémentListeTroisième.join(); System.out.println(estTerminé);
        try { valeurUn.start(); } catch (IllegalThreadStateException e) { System.out.println("재시작 rejeterValeur"); }
        System.out.println("valeurFilExécution estTerminé");
    }
}
