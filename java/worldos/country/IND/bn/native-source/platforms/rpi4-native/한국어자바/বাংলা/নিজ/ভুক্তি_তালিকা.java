// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
import java.util.ArrayList;
/** ভুক্তি_তালিকা(目錄): 순서가 있는 항목의 모음. 이 판은 স্ট্রিং_মান 목록을 제공한다. */
public final class ভুক্তি_তালিকা {
    private final ArrayList<String> ভুক্তি_মান = new ArrayList<String>();
    public void 더하기(String মান) { ভুক্তি_মান.add(মান); }
    public String পড়া(int ক্রম_মান) { return ভুক্তি_মান.get(ক্রম_মান); }
    public String প্রতিস্থাপন_করা_মান(int ক্রম_মান, String মান) { return ভুক্তি_মান.set(ক্রম_মান, মান); }
    public String মুছুন_ভুক্তি(int ক্রম_মান) { return ভুক্তি_মান.remove(ক্রম_মান); }
    public int আকার() { return ভুক্তি_মান.size(); }
    public boolean তথ্য_প্রযুক্তি_খালি_মান() { return ভুক্তি_মান.isEmpty(); }
    public void মুছে_দিন_সূচী() { ভুক্তি_মান.clear(); }
}
