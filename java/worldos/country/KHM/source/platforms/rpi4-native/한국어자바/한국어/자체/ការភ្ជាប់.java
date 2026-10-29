// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** ភ្ជាប់(連結)·កាណាល់_ការបញ្ចូល(通路): 상대와 이어진 TCP បៃ_តំលៃ 흐름의 종단. */
public final class ការភ្ជាប់ {
    private final java.net.Socket 표준연결;
    ការភ្ជាប់(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static ការភ្ជាប់ បើក(String អ៊ីម៉ែល, int លេខរន្ធ) throws ចូល_ចេញ_ការលើកលែង {
        try {
            return new ការភ្ជាប់(new java.net.Socket(អ៊ីម៉ែល, លេខរន្ធ));
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public 입력흐름 입력() throws ចូល_ចេញ_ការលើកលែង {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public 출력흐름 លទ្ធផល() throws ចូល_ចេញ_ការលើកលែង {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public void អស់ម៉ោង(int 밀리초) throws ចូល_ចេញ_ការលើកលែង {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
    public int លេខរន្ធ() { return 표준연결.getPort(); }
    public int ក្នុងតំបន់_លេខរន្ធ() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void បិទ() throws ចូល_ចេញ_ការលើកលែង {
        try { 표준연결.close();
        } catch (java.io.IOException កំហុស) { throw 예외변환.ចូល_ចេញ(កំហុស); }
        catch (RuntimeException កំហុស) { throw 예외변환.អនុវត្ត_ពាក្យបញ្ជា(កំហុស); }
    }
}
