// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Giao ước chung cho đối tượng màn hình của JVM tự xây dựng; không giữ đối tượng Swing tiêu chuẩn. */
public abstract class PhầnTửMànHình {
    public native String đọcVănBản();
    public native void ghiVănBản(String vănBản);
    public native void đặtGiáTrịCácCận(int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int giáTrịCao);
}
