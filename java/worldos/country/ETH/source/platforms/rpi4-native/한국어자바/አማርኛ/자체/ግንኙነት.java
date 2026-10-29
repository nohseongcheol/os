// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;

/** መገናኛ(連結)·ሰርጥ_ምዝግብ(通路): 상대와 이어진 TCP ባይት_እሴት 흐름의 종단. */
public final class ግንኙነት {
    private final java.net.Socket 표준연결;
    ግንኙነት(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static ግንኙነት መክፈቻ(String አድራሻ, int የወደብ_ቁጥር) throws ግቤት_ውጤት_ልዩነት {
        try {
            return new ግንኙነት(new java.net.Socket(አድራሻ, የወደብ_ቁጥር));
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public 입력흐름 입력() throws ግቤት_ውጤት_ልዩነት {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public 출력흐름 ውጤት() throws ግቤት_ውጤት_ልዩነት {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public void 대기시간(int 밀리초) throws ግቤት_ውጤት_ልዩነት {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public int የወደብ_ቁጥር() { return 표준연결.getPort(); }
    public int የአካባቢ_የወደብ_ቁጥር() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void መዝጊያ() throws ግቤት_ውጤት_ልዩነት {
        try { 표준연결.close();
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
}
