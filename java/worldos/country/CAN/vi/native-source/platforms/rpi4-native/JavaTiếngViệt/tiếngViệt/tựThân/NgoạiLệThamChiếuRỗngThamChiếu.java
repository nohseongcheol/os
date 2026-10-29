// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệThamChiếuRỗngThamChiếu: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệThamChiếuRỗngThamChiếu extends java.lang.NullPointerException {
    public NgoạiLệThamChiếuRỗngThamChiếu() { super(); }
    public NgoạiLệThamChiếuRỗngThamChiếu(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
