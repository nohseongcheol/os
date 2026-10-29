// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;

/** 수신(受信)·ወደብ_እሴት(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int የወደብ_ቁጥር) throws ግቤት_ውጤት_ልዩነት {
        try { 표준창구 = new java.net.ServerSocket(የወደብ_ቁጥር);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static 수신창구 መክፈቻ(int የወደብ_ቁጥር) throws ግቤት_ውጤት_ልዩነት {
        try { return new 수신창구(የወደብ_ቁጥር);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public ግንኙነት 받기() throws ግቤት_ውጤት_ልዩነት {
        try { return new ግንኙነት(표준창구.accept());
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public int የወደብ_ቁጥር() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws ግቤት_ውጤት_ልዩነት {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void መዝጊያ() throws ግቤት_ውጤት_ልዩነት {
        try { 표준창구.close();
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
}
