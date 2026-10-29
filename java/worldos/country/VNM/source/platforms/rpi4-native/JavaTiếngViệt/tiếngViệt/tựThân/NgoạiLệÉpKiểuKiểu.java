// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệÉpKiểuKiểu: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệÉpKiểuKiểu extends java.lang.ClassCastException {
    public NgoạiLệÉpKiểuKiểu() { super(); }
    public NgoạiLệÉpKiểuKiểu(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
