// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import français.Java.Caractères;

/** Petit point d’entrée Java dont d’autres langages peuvent lire le résultat sur la sortie standard. */
public final class CommandeTexte {
    public static void main(String[] arguments) {
        if (arguments.length != 1) {
            System.err.println("사용법: CommandeTexte Chaîne");
            System.exit(2);
        }
        System.out.println(Caractères.nombreÉlémentsPointCode(arguments[0]));
    }
}
