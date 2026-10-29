// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Deutsch.eigen;
/** Festes, von der eigenen JVM angebundenes ABI; weder JNI noch ein Lader für beliebige native Methoden. */
public final class betriebskernWert {
    private betriebskernWert() {}
    public static native int millisekunden();
    public static native int fürAbbildWarten();
    public static native int bildschirmBreite();
    public static native int bildschirmHöhe();
    public static native int rechteck(int waagerechtPosition, int senkrechtPosition, int breiteSpannweite, int höheWert, int farbeWert);
}
