// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** ngoạiLệ: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class ngoạiLệ extends java.lang.Exception {
    public ngoạiLệ() { super(); }
    public ngoạiLệ(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
