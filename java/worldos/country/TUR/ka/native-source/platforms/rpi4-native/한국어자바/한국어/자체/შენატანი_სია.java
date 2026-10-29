// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** შენატანი_სია(目錄): 순서가 있는 항목의 모음. 이 판은 სტრიქონი_მნიშვნელობა 목록을 제공한다. */
public final class შენატანი_სია {
    private final ArrayList<String> შენატანი_მნიშვნელობა = new ArrayList<String>();
    public void 더하기(String მნიშვნელობა) { შენატანი_მნიშვნელობა.add(მნიშვნელობა); }
    public String კითხვა(int დახარისხების_თანმიმდევრობა_მნიშვნელობა) { return შენატანი_მნიშვნელობა.get(დახარისხების_თანმიმდევრობა_მნიშვნელობა); }
    public String ჩანაცვლება_მნიშვნელობა(int დახარისხების_თანმიმდევრობა_მნიშვნელობა, String მნიშვნელობა) { return შენატანი_მნიშვნელობა.set(დახარისხების_თანმიმდევრობა_მნიშვნელობა, მნიშვნელობა); }
    public String 지우기(int დახარისხების_თანმიმდევრობა_მნიშვნელობა) { return შენატანი_მნიშვნელობა.remove(დახარისხების_თანმიმდევრობა_მნიშვნელობა); }
    public int ზომა() { return შენატანი_მნიშვნელობა.size(); }
    public boolean 비었는가() { return შენატანი_მნიშვნელობა.isEmpty(); }
    public void გასუფთავება_სარჩევი() { შენატანი_მნიშვნელობა.clear(); }
}
