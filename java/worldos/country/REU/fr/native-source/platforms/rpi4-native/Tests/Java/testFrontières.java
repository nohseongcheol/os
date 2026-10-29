// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import java.io.*;
public class testFrontières {
    static int valeurÉchec() { throw new IllegalStateException("Tâche 중 exception"); }
    public static void main(String[] a) throws Exception {
        Object tableauTexteClair = new Object[2]; System.out.println(tableauTexteClair instanceof String[]);
        try { String[] résultatInvalide = (String[])tableauTexteClair; } catch (ClassCastException e) { System.out.println("valeurTableau convertirValeur Contrôles"); }
        Object[] listeTexte = new String[2];
        try { listeTexte[0] = Integer.valueOf(1); } catch (ArrayStoreException e) { System.out.println("valeurTableau valeurType Contrôles"); }
        try { System.arraycopy(new Object[] {"앞", Integer.valueOf(1)}, 0, listeTexte, 0, 2); } catch (ArrayStoreException e) { System.out.println("copierValeur valeurType Contrôles"); }
        System.out.println((String)listeTexte[0]);
        try { "texte".substring(0, -1); } catch (StringIndexOutOfBoundsException e) { System.out.println("Caractères rogner"); }
        Integer valeurUn = Integer.valueOf(127), valeurDeux = Integer.valueOf(127); System.out.println(valeurUn == valeurDeux);
        Object valeurVerrou = new Object(); try { synchronized (valeurVerrou) { valeurÉchec(); } } catch (IllegalStateException e) { System.out.println("valeurVerrou exception"); }
        synchronized (valeurVerrou) { System.out.println("valeurVerrou 회수"); }
        byte[] Données = {0, (byte)128, (byte)255, 10};
        FileOutputStream Sortie = new FileOutputStream("valeurOctet.bin"); Sortie.write(Données); Sortie.flush(); Sortie.close();
        FileInputStream valeurEntrée = new FileInputStream("valeurOctet.bin"); byte[] lireRésultat = new byte[8];
        System.out.println(valeurEntrée.read(lireRésultat, 2, 4)); System.out.println(lireRésultat[3] + ":" + lireRésultat[4]);
        System.out.println(valeurEntrée.read(lireRésultat)); System.out.println(valeurEntrée.read(lireRésultat, 0, 0)); valeurEntrée.close();
        try { valeurEntrée.read(); } catch (IOException e) { System.out.println("닫힌 Fichier"); }
    }
}
