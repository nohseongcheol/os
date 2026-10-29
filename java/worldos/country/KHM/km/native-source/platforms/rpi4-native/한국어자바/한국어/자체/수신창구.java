// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·ច្រក_តំលៃ(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int លេខរន្ធ) throws ចូល_ចេញ_ការលើកលែង {
        try { 표준창구 = new java.net.ServerSocket(លេខរន្ធ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public static 수신창구 បើក(int លេខរន្ធ) throws ចូល_ចេញ_ការលើកលែង {
        try { return new 수신창구(លេខរន្ធ);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public ការភ្ជាប់ 받기() throws ចូល_ចេញ_ការលើកលែង {
        try { return new ការភ្ជាប់(표준창구.accept());
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public int លេខរន្ធ() { return 표준창구.getLocalPort(); }
    public void អស់ម៉ោង(int 밀리초) throws ចូល_ចេញ_ការលើកលែង {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void បិទ() throws ចូល_ចេញ_ការលើកលែង {
        try { 표준창구.close();
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
}
