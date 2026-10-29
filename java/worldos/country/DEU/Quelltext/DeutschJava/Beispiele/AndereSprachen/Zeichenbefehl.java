// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Deutsch.Java.Zeichen;

/** Kleiner Java-Einstieg, dessen Ergebnisse andere Sprachen von der Standardausgabe lesen können. */
public final class Zeichenbefehl {
    public static void main(String[] argumente) {
        if (argumente.length != 1) {
            System.err.println("사용법: Zeichenbefehl Zeichenkette");
            System.exit(2);
        }
        System.out.println(Zeichen.kodePunktAnzahl(argumente[0]));
    }
}
