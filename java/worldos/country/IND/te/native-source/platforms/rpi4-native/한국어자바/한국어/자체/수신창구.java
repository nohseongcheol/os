// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·పోర్టు_మూల్యం(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int పోర్ట్_సంఖ్య) throws మూ_ఫ_మినహాయింపు {
        try { 표준창구 = new java.net.ServerSocket(పోర్ట్_సంఖ్య);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static 수신창구 తెరువు(int పోర్ట్_సంఖ్య) throws మూ_ఫ_మినహాయింపు {
        try { return new 수신창구(పోర్ట్_సంఖ్య);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public కనెక్షన్ 받기() throws మూ_ఫ_మినహాయింపు {
        try { return new కనెక్షన్(표준창구.accept());
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public int పోర్ట్_సంఖ్య() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws మూ_ఫ_మినహాయింపు {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void మూసివేయి() throws మూ_ఫ_మినహాయింపు {
        try { 표준창구.close();
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
}
