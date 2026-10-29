// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệCácCậnMảng: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệCácCậnMảng extends NgoạiLệCácCận {
    public NgoạiLệCácCậnMảng() { super(); }
    public NgoạiLệCácCậnMảng(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
