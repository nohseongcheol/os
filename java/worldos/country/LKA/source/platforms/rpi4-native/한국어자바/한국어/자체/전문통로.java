// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·නාලිකාව_පිවිසුම(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int 접속번호) throws 입출력예외 {
        try { 표준종단 = 통신.විවෘත_කරන්න(접속번호);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static 전문통로 විවෘත_කරන්න(int 접속번호) throws 입출력예외 {
        try { return new 전문통로(접속번호);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public void ඊමේල්(String යොමුව, int 접속번호, String දත්ත) throws 입출력예외 {
        try { 통신.ඊමේල්(표준종단, යොමුව, 접속번호, දත්ත);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public String 받기() throws 입출력예외 {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 통신.대기시간(표준종단, 밀리초);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public int 접속번호() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void වසන්න() { 통신.වසන්න(표준종단); }
}
