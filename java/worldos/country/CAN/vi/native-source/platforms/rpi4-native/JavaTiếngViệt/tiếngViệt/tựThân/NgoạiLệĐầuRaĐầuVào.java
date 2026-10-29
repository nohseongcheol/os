// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệĐầuRaĐầuVào: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệĐầuRaĐầuVào extends java.io.IOException {
    public NgoạiLệĐầuRaĐầuVào() { super(); }
    public NgoạiLệĐầuRaĐầuVào(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
