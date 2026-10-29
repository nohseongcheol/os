// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệViệcThựcThi: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệViệcThựcThi extends java.lang.RuntimeException {
    public NgoạiLệViệcThựcThi() { super(); }
    public NgoạiLệViệcThựcThi(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
