// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static සබැඳුම විවෘත_කරන්න(String යොමුව, int 접속번호) throws 입출력예외 {
        try { return සබැඳුම.විවෘත_කරන්න(යොමුව, 접속번호);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.විවෘත_කරන්න(접속번호);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static Socket සම්බන්ද_වන්න(String යොමුව, int තොට_අගය) throws 입출력예외 {
        try { return new Socket(යොමුව, තොට_අගය);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static ServerSocket 듣기(int තොට_අගය) throws 입출력예외 {
        try { return new ServerSocket(තොට_අගය);
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
    public static Socket 받기(ServerSocket සේවාදායකය_අගය) throws 입출력예외 {
        try { return සේවාදායකය_අගය.accept();
        } catch (java.io.IOException දෝෂය) { throw 예외변환.ආදාන_ප්_රතිදාන(දෝෂය); }
        catch (RuntimeException දෝෂය) { throw 예외변환.ක්_රියාත්මක_කරන්න_විධානය(දෝෂය); }
    }
}
