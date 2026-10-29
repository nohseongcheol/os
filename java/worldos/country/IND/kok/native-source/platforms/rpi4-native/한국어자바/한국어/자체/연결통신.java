// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static कनॅक्शन उगडचें(String नामो, int 접속번호) throws 입출력예외 {
        try { return कनॅक्शन.उगडचें(नामो, 접속번호);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.उगडचें(접속번호);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static Socket कनॅक्ट(String नामो, int पोर्ट_मोल) throws 입출력예외 {
        try { return new Socket(नामो, पोर्ट_मोल);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static ServerSocket 듣기(int पोर्ट_मोल) throws 입출력예외 {
        try { return new ServerSocket(पोर्ट_मोल);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public static Socket 받기(ServerSocket सर्वर_मोल) throws 입출력예외 {
        try { return सर्वर_मोल.accept();
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
}
