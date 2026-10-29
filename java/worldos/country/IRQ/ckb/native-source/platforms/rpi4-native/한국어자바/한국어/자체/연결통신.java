// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static گرێدان کردنەوە(String ناونیشان, int 접속번호) throws 입출력예외 {
        try { return گرێدان.کردنەوە(ناونیشان, 접속번호);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.کردنەوە(접속번호);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public static Socket لكاندن(String ناونیشان, int دەرگا_نرخ) throws 입출력예외 {
        try { return new Socket(ناونیشان, دەرگا_نرخ);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public static ServerSocket 듣기(int دەرگا_نرخ) throws 입출력예외 {
        try { return new ServerSocket(دەرگا_نرخ);
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
    public static Socket 받기(ServerSocket ڕاژەکار_نرخ) throws 입출력예외 {
        try { return ڕاژەکار_نرخ.accept();
        } catch (java.io.IOException هەڵە) { throw 예외변환.I_O(هەڵە); }
        catch (RuntimeException هەڵە) { throw 예외변환.جێبەجێکردن_فەرمان(هەڵە); }
    }
}
