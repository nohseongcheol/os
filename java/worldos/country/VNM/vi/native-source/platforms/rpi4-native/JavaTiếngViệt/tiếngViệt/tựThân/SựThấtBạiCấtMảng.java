// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** SựThấtBạiCấtMảng: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class SựThấtBạiCấtMảng extends java.lang.ArrayStoreException {
    public SựThấtBạiCấtMảng() { super(); }
    public SựThấtBạiCấtMảng(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
