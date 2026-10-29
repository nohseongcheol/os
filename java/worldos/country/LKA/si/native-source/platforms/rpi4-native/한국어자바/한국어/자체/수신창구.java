// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·තොට_අගය(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int 접속번호) throws 입출력예외 {
        try { 표준창구 = new java.net.ServerSocket(접속번호);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static 수신창구 විවෘත_කරන්න(int 접속번호) throws 입출력예외 {
        try { return new 수신창구(접속번호);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public සබැඳුම 받기() throws 입출력예외 {
        try { return new සබැඳුම(표준창구.accept());
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public int 접속번호() { return 표준창구.getLocalPort(); }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void වසන්න() throws 입출력예외 {
        try { 표준창구.close();
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
}
