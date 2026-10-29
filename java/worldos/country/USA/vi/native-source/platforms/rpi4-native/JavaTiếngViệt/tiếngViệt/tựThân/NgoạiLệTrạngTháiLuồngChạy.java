// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệTrạngTháiLuồngChạy: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệTrạngTháiLuồngChạy extends java.lang.IllegalThreadStateException {
    public NgoạiLệTrạngTháiLuồngChạy() { super(); }
    public NgoạiLệTrạngTháiLuồngChạy(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
