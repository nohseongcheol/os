// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ਪੰਜਾਬੀ.자체;
import java.util.ArrayList;
/** ਦਾਖਲਾ_ਸੂਚੀ(目錄): 순서가 있는 항목의 모음. 이 판은 ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਕੀਮਤ 목록을 제공한다. */
public final class ਦਾਖਲਾ_ਸੂਚੀ {
    private final ArrayList<String> ਦਾਖਲਾ_ਕੀਮਤ = new ArrayList<String>();
    public void 더하기(String ਕੀਮਤ) { ਦਾਖਲਾ_ਕੀਮਤ.add(ਕੀਮਤ); }
    public String ਪੜ੍ਹਨ(int ਕ੍ਰਮ_ਕੀਮਤ) { return ਦਾਖਲਾ_ਕੀਮਤ.get(ਕ੍ਰਮ_ਕੀਮਤ); }
    public String ਸਥਾਨ_ਬਦਲੋ_ਕੀਮਤ(int ਕ੍ਰਮ_ਕੀਮਤ, String ਕੀਮਤ) { return ਦਾਖਲਾ_ਕੀਮਤ.set(ਕ੍ਰਮ_ਕੀਮਤ, ਕੀਮਤ); }
    public String 지우기(int ਕ੍ਰਮ_ਕੀਮਤ) { return ਦਾਖਲਾ_ਕੀਮਤ.remove(ਕ੍ਰਮ_ਕੀਮਤ); }
    public int ਆਕਾਰ() { return ਦਾਖਲਾ_ਕੀਮਤ.size(); }
    public boolean 비었는가() { return ਦਾਖਲਾ_ਕੀਮਤ.isEmpty(); }
    public void ਹਟਾਓ_ਤਤਕਰਾ() { ਦਾਖਲਾ_ਕੀਮਤ.clear(); }
}
