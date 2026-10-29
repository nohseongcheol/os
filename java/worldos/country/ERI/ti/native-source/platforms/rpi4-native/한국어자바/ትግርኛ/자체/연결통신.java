// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ትግርኛ.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static ርክብ ክፈት(String ኣድራሻ, int 접속번호) throws 입출력예외 {
        try { return ርክብ.ክፈት(ኣድራሻ, 접속번호);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.ክፈት(접속번호);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static Socket ኣላግብ(String ኣድራሻ, int ወደብ_ዋጋ) throws 입출력예외 {
        try { return new Socket(ኣድራሻ, ወደብ_ዋጋ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static ServerSocket 듣기(int ወደብ_ዋጋ) throws 입출력예외 {
        try { return new ServerSocket(ወደብ_ዋጋ);
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
    public static Socket 받기(ServerSocket ኣገልጋሊ_ዋጋ) throws 입출력예외 {
        try { return ኣገልጋሊ_ዋጋ.accept();
        } catch (java.io.IOException ጌጋ) { throw 예외변환.입출력(ጌጋ); }
        catch (RuntimeException ጌጋ) { throw 예외변환.ተግብር_ትእዛዝ(ጌጋ); }
    }
}
