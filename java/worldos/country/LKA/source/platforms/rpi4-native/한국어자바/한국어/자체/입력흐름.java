// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 입력(入力)과 දහර_අගය: 순서대로 들어오는 바이트를 읽는 නාලිකාව_පිවිසුම. */
public final class 입력흐름 {
    private final java.io.InputStream 표준흐름;
    입력흐름(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int කියවීම() throws 입출력예외 {
        try { return 표준흐름.read();
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public int කියවීම(byte[] දත්ත) throws 입출력예외 {
        try { return 표준흐름.read(දත්ත);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public int කියවීම(byte[] දත්ත, int ක්_රියාත්මක_කරන්න_2, int දිග_අගය) throws 입출력예외 {
        try { return 표준흐름.read(දත්ත, ක්_රියාත්මක_කරන්න_2, දිග_අගය);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public void වසන්න() throws 입출력예외 {
        try { 표준흐름.close();
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
}
