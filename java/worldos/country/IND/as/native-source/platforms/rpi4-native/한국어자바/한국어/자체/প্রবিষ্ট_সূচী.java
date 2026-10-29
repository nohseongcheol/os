// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** প্রবিষ্ট_সূচী(目錄): 순서가 있는 항목의 모음. 이 판은 ষ্ট্ৰিং_মান 목록을 제공한다. */
public final class প্রবিষ্ট_সূচী {
    private final ArrayList<String> প্রবিষ্ট_মান = new ArrayList<String>();
    public void 더하기(String মান) { প্রবিষ্ট_মান.add(মান); }
    public String পড়া(int ক্ৰম_মান) { return প্রবিষ্ট_মান.get(ক্ৰম_মান); }
    public String পুনঃস্থাপন_কৰক_মান(int ক্ৰম_মান, String মান) { return প্রবিষ্ট_মান.set(ক্ৰম_মান, মান); }
    public String 지우기(int ক্ৰম_মান) { return প্রবিষ্ট_মান.remove(ক্ৰম_মান); }
    public int মাপ() { return প্রবিষ্ট_মান.size(); }
    public boolean 비었는가() { return প্রবিষ্ট_মান.isEmpty(); }
    public void পৰিষ্কাৰ_কৰক_সামগ্ৰী() { প্রবিষ্ট_মান.clear(); }
}
