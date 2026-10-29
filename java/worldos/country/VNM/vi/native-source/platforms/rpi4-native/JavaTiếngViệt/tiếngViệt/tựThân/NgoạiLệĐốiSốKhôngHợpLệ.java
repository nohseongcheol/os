// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệĐốiSốKhôngHợpLệ: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệĐốiSốKhôngHợpLệ extends java.lang.IllegalArgumentException {
    public NgoạiLệĐốiSốKhôngHợpLệ() { super(); }
    public NgoạiLệĐốiSốKhôngHợpLệ(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
