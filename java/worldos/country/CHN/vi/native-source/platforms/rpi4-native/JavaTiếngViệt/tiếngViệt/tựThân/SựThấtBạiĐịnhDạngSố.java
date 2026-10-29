// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** SựThấtBạiĐịnhDạngSố: ngoại lệ có thể khai báo, ném và bắt qua API tiếng Việt. */
public class SựThấtBạiĐịnhDạngSố extends NgoạiLệĐốiSốKhôngHợpLệ {
    public SựThấtBạiĐịnhDạngSố() { super(); }
    public SựThấtBạiĐịnhDạngSố(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
