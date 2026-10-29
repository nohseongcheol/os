// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** Vérifie les conditions attendues dans les exemples exécutables et les tests. */
public final class Contrôles {
    private Contrôles() {}
    public static void exiger(boolean condition, String valeurCause) {
        if (!condition) throw new ExceptionArgumentInvalide(valeurCause);
    }
}
