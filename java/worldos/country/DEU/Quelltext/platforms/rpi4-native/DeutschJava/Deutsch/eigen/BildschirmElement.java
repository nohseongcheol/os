// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Gemeinsamer Vertrag für Anzeigeobjekte der eigenen JVM; bewahrt keine Standard-Swing-Objekte auf. */
public abstract class BildschirmElement {
    public native String textLesen();
    public native void textSchreiben(String Text);
    public native void grenzenSetzen(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert);
}
