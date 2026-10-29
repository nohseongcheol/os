// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package English.Native;
/** Command-line arguments supplied by the built-in JVM to the entry method; excludes the class name. */
public final class Arguments {
    private Arguments() {}
    public static native int itemCount();
    public static native String text(int ordinalIndex) throws BoundsException;
}
