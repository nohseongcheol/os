// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** SựThấtBạiCỡMảngÂm: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class SựThấtBạiCỡMảngÂm extends java.lang.NegativeArraySizeException {
    public SựThấtBạiCỡMảngÂm() { super(); }
    public SựThấtBạiCỡMảngÂm(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
