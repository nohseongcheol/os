// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;

/** Prüft erwartete Bedingungen in ausführbaren Beispielen und Tests. */
public final class Prüfpunkte {
    private Prüfpunkte() {}
    public static void erfordern(boolean bedingung, String ursacheWert) {
        if (!bedingung) throw new UngültigArgumentAusnahme(ursacheWert);
    }
}
