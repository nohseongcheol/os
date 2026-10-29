// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Aktionsmeldung, die die Ereignisverarbeitung der eigenen JVM erzeugt. */
public final class AktionMitteilung {
    private AktionMitteilung() {}
    public native String befehlText();
    public native BildschirmElement ereignisQuelltext();
    public native int Nummer();
}
