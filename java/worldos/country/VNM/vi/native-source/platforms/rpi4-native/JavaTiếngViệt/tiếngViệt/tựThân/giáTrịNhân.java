// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** ABI cố định do JVM tự xây dựng nối vào; không phải JNI hay bộ nạp phương thức native tùy ý. */
public final class giáTrịNhân {
    private giáTrịNhân() {}
    public static native int miliGiây();
    public static native int chờẢnhCho();
    public static native int rộngMànHình();
    public static native int caoMànHình();
    public static native int hìnhChữNhật(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int giáTrịCao, int giáTrịMàu);
}
