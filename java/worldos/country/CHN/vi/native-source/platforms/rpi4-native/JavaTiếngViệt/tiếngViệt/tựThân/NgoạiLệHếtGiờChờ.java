// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệHếtGiờChờ: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệHếtGiờChờ extends NgoạiLệĐầuRaĐầuVào {
    public NgoạiLệHếtGiờChờ() { super(); }
    public NgoạiLệHếtGiờChờ(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
