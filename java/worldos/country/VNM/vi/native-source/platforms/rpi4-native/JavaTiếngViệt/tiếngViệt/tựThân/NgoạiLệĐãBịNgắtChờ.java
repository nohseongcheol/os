// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package tiếngViệt.tựThân;

/** Biểu thị sự gián đoạn thao tác đang chờ một luồng, không phải kết thúc bản thân tác vụ. */
public class NgoạiLệĐãBịNgắtChờ extends java.lang.InterruptedException {
    public NgoạiLệĐãBịNgắtChờ() { super(); }
    public NgoạiLệĐãBịNgắtChờ(String môTả) { super(môTả); }
    public String môTả() { return getMessage(); }
}
