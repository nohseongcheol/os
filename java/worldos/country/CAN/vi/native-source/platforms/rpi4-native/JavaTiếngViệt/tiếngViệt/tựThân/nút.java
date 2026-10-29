// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;
/** Nút gửi thông báo hành động trên màn hình của hệ thống. */
public final class nút extends PhầnTửMànHình {
    public nút(String vănBản, int vịTríNgang, int vịTríDọc, int khoảngTrảiRộng, int giáTrịCao, BộNhậnHànhĐộng giáTrịBộNhận) {
        throw new NgoạiLệTrạngThái("JVM riêng phải hỗ trợ tạo nút qua API tiếng Việt.");
    }
    public native void đặtGiáTrịBộNhậnHànhĐộng(BộNhậnHànhĐộng giáTrịBộNhận);
}
