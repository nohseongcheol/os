// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.util.HashMap;
/** 사전(辭典): 찾는 말(열쇠)에 값을 대응시킨다. */
public final class 사전 {
    private final HashMap<String, String> Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = new HashMap<String, String>();
    public String 넣기(String 열쇠, String ᏧᎬᏩᎶᏗᏯ) { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.put(열쇠, ᏧᎬᏩᎶᏗᏯ); }
    public String ᎯᏩᏔ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ(String 열쇠) { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.get(열쇠); }
    public boolean 있는가(String 열쇠) { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.containsKey(열쇠); }
    public String 지우기(String 열쇠) { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.remove(열쇠); }
    public int ᎢᎩᏓ() { return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.size(); }
    public void ᎯᎵᎦᎵᏯ_ᏕᎦᎸᏛᎢ() { Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.clear(); }
}
