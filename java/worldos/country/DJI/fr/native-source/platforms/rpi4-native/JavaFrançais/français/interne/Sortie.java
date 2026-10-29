// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;
/** Sortie standard du noyau autonome. Les paires de substitution UTF-16 sont envoyées en UTF-8 sur UART. */
public final class Sortie {
    private Sortie() {}
    public static void écrire(String texte) { System.out.print(texte); }
    public static void écrireLigne(String texte) { System.out.println(texte); }
    public static void écrireNuméro(int nombre) { System.out.println(nombre); }
}
