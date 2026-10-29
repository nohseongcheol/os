// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** SựThấtBạiSốHọc: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class SựThấtBạiSốHọc extends java.lang.ArithmeticException {
    public SựThấtBạiSốHọc() { super(); }
    public SựThấtBạiSốHọc(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
