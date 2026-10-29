// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·ఛానల్_ప్రవేశం(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int పోర్ట్_సంఖ్య) throws మూ_ఫ_మినహాయింపు {
        try { 표준종단 = 통신.తెరువు(పోర్ట్_సంఖ్య);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public static 전문통로 తెరువు(int పోర్ట్_సంఖ్య) throws మూ_ఫ_మినహాయింపు {
        try { return new 전문통로(పోర్ట్_సంఖ్య);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public void పంపు(String ఇమెయిల్, int పోర్ట్_సంఖ్య, String డేటా) throws మూ_ఫ_మినహాయింపు {
        try { 통신.పంపు(표준종단, ఇమెయిల్, పోర్ట్_సంఖ్య, డేటా);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public String 받기() throws మూ_ఫ_మినహాయింపు {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public void 대기시간(int 밀리초) throws మూ_ఫ_మినహాయింపు {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public int పోర్ట్_సంఖ్య() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void మూసివేయి() { 통신.మూసివేయి(표준종단); }
}
