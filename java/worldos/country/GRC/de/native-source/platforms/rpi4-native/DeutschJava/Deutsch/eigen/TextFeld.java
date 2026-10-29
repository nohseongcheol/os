// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Grafikelement der deutschen API, das die eigene JVM direkt erzeugt und zeichnet. */
public final class TextFeld extends BildschirmElement {
    public TextFeld(String Text, int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert) {
        throw new StatuswertAusnahme("Die eigene JVM muss Bildschirmelemente über die deutsche API erstellen können.");
    }
}
