// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.ArrayList;
/** Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ(目錄): 순서가 있는 항목의 모음. 이 판은 ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ 목록을 제공한다. */
public final class Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏕᎦᏅᏅᏛ {
    private final ArrayList<String> Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = new ArrayList<String>();
    public void 더하기(String ᏧᎬᏩᎶᏗᏯ) { Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.add(ᏧᎬᏩᎶᏗᏯ); }
    public String 읽기(int ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ) { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.get(ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ); }
    public String ᎯᏁᏟᏴᏍᏓ_ᏧᎬᏩᎶᏗᏯ(int ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ, String ᏧᎬᏩᎶᏗᏯ) { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.set(ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ, ᏧᎬᏩᎶᏗᏯ); }
    public String 지우기(int ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ) { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.remove(ᏗᎦᏅᏃᏙᏗ_ᏕᎦᏅᏃᏛᎢ_ᏧᎬᏩᎶᏗᏯ); }
    public int ᎢᎩᏓ() { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.size(); }
    public boolean 비었는가() { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.isEmpty(); }
    public void ᎯᎵᎦᎵᏯ_ᏕᎦᎸᏛᎢ() { Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.clear(); }
}
