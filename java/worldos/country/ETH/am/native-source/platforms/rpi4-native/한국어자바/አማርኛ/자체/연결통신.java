// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package አማርኛ.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ግንኙነት መክፈቻ(String አድራሻ, int የወደብ_ቁጥር) throws ግቤት_ውጤት_ልዩነት {
        try { return ግንኙነት.መክፈቻ(አድራሻ, የወደብ_ቁጥር);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static 수신창구 수신열기(int የወደብ_ቁጥር) throws ግቤት_ውጤት_ልዩነት {
        try { return 수신창구.መክፈቻ(የወደብ_ቁጥር);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static Socket መገናኛ(String አድራሻ, int ወደብ_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try { return new Socket(አድራሻ, ወደብ_እሴት);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static ServerSocket 듣기(int ወደብ_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try { return new ServerSocket(ወደብ_እሴት);
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
    public static Socket 받기(ServerSocket አገልጋይ_እሴት) throws ግቤት_ውጤት_ልዩነት {
        try { return አገልጋይ_እሴት.accept();
        } catch (java.io.IOException ስህተት) { throw 예외변환.ግቤት_ውጤት(ስህተት); }
        catch (RuntimeException ስህተት) { throw 예외변환.ፈጽም_ትእዛዝ(ስህተት); }
    }
}
