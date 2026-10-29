// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
interface peutCalculer { int valeur(); }
class valeurArrièrePlan { static int préparer = 7; int nombre; String nom; valeurArrièrePlan(int nombre) { this.nombre = nombre; nom = "valeurArrièrePlan"; } int valeur() { return nombre; } }
class valeurBranche extends valeurArrièrePlan implements peutCalculer { valeurBranche(int nombre) { super(nombre); nom = "valeurBranche"; } public int valeur() { return nombre * préparer; } }
public class testObjets {
    static int étatValeurInitialValeur = valeurArrièrePlan.préparer + 2;
    static int branche(int nombre) { switch (nombre) { case 1: return 12; case 2: return 23; case 3: return 34; default: return -1; } }
    static int valeurClairsemé(int nombre) { switch (nombre) { case -1: return 91; case 100: return 92; default: return 90; } }
    public static void main(String[] arguments) {
        valeurBranche opérandeDeuxième = new valeurBranche(6); valeurArrièrePlan opérandeTroisième = opérandeDeuxième; peutCalculer opérandeQuatrième = opérandeDeuxième;
        System.out.println(étatValeurInitialValeur + ":" + opérandeDeuxième.nom + ":" + opérandeTroisième.valeur() + ":" + opérandeQuatrième.valeur());
        System.out.println((opérandeTroisième instanceof valeurBranche) + ":" + (opérandeTroisième instanceof peutCalculer) + ":" + branche(2) + ":" + valeurClairsemé(100));
        Object[] valeurTableau = new Object[3]; valeurTableau[0] = opérandeDeuxième; valeurTableau[1] = "한글😀"; System.gc();
        System.out.println(((valeurBranche)valeurTableau[0]).valeur()); System.out.println((String)valeurTableau[1]);
        int[] listeNombreÉléments = {1, 2, 3, 4}; System.arraycopy(listeNombreÉléments, 0, listeNombreÉléments, 1, 3); System.out.println(listeNombreÉléments[3]);
        byte[] valeurOctet = new byte[1]; valeurOctet[0] = (byte)255; char[] Caractères = {'한'}; short[] estCourt = {(short)65535}; boolean[] valeurBooléen = {true};
        System.out.println(valeurOctet[0] + ":" + Caractères[0] + ":" + estCourt[0] + ":" + valeurBooléen[0]);
    }
}
