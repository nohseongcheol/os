// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** 목록(目錄): 순서가 있는 항목의 모음. 이 판은 문자열 목록을 제공한다. */
public final class 목록 {
    private final ArrayList<String> 항목 = new ArrayList<String>();
    public void 더하기(String 값) { 항목.add(값); }
    public String Loga(int 순서) { return 항목.get(순서); }
    public String 바꾸기(int 순서, String 값) { return 항목.set(순서, 값); }
    public String 지우기(int 순서) { return 항목.remove(순서); }
    public int 크기() { return 항목.size(); }
    public boolean 비었는가() { return 항목.isEmpty(); }
    public void 비우기() { 항목.clear(); }
}
