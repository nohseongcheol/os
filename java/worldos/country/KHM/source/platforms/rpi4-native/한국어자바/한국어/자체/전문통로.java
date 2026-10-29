// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·កាណាល់_ការបញ្ចូល(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int លេខរន្ធ) throws ចូល_ចេញ_ការលើកលែង {
        try { 표준종단 = 통신.បើក(លេខរន្ធ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static 전문통로 បើក(int លេខរន្ធ) throws ចូល_ចេញ_ការលើកលែង {
        try { return new 전문통로(លេខរន្ធ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public void ផ្ញើ(String អ៊ីម៉ែល, int លេខរន្ធ, String ទិន្នន័យ) throws ចូល_ចេញ_ការលើកលែង {
        try { 통신.ផ្ញើ(표준종단, អ៊ីម៉ែល, លេខរន្ធ, ទិន្នន័យ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public String 받기() throws ចូល_ចេញ_ការលើកលែង {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public void អស់ម៉ោង(int 밀리초) throws ចូល_ចេញ_ការលើកលែង {
        try { 통신.អស់ម៉ោង(표준종단, 밀리초);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public int លេខរន្ធ() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void បិទ() { 통신.បិទ(표준종단); }
}
