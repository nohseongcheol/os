// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Schaltfläche, die Aktionsmeldungen in der eigenen Oberfläche sendet. */
public final class schaltfläche extends BildschirmElement {
    public schaltfläche(String Text, int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert, AktionEmpfänger empfängerWert) {
        throw new StatuswertAusnahme("Die eigene JVM muss Schaltflächen über die deutsche API erstellen können.");
    }
    public native void aktionEmpfängerSetzen(AktionEmpfänger empfängerWert);
}
