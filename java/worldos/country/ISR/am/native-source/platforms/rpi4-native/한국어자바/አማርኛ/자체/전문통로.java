// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;

/** 전문(電文)·ሰርጥ_ምዝግብ(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int የወደብ_ቁጥር) throws ግቤት_ውጤት_ልዩነት {
        try { 표준종단 = 통신.መክፈቻ(የወደብ_ቁጥር);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static 전문통로 መክፈቻ(int የወደብ_ቁጥር) throws ግቤት_ውጤት_ልዩነት {
        try { return new 전문통로(የወደብ_ቁጥር);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public void ላክ(String አድራሻ, int የወደብ_ቁጥር, String ውሂብ) throws ግቤት_ውጤት_ልዩነት {
        try { 통신.ላክ(표준종단, አድራሻ, የወደብ_ቁጥር, ውሂብ);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public String 받기() throws ግቤት_ውጤት_ልዩነት {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public void 대기시간(int 밀리초) throws ግቤት_ውጤት_ልዩነት {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public int የወደብ_ቁጥር() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void መዝጊያ() { 통신.መዝጊያ(표준종단); }
}
