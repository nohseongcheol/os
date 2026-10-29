// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** NgoạiLệCácCận: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class NgoạiLệCácCận extends java.lang.IndexOutOfBoundsException {
    public NgoạiLệCácCận() { super(); }
    public NgoạiLệCácCận(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
