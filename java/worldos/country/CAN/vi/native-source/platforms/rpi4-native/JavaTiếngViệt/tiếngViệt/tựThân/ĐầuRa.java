// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Đầu ra tiêu chuẩn của nhân độc lập. Cặp thay thế UTF-16 được gửi qua UART dưới dạng UTF-8. */
public final class ĐầuRa {
    private ĐầuRa() {}
    public static void ghi(String vănBản) { System.out.print(vănBản); }
    public static void ghiDòng(String vănBản) { System.out.println(vănBản); }
    public static void ghiSố(int trịSố) { System.out.println(trịSố); }
}
