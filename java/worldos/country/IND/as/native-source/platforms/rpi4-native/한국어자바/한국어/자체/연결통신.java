// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static সংযোগ খোলো(String ঠিকনা, int 접속번호) throws 입출력예외 {
        try { return সংযোগ.খোলো(ঠিকনা, 접속번호);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static 수신창구 수신열기(int 접속번호) throws 입출력예외 {
        try { return 수신창구.খোলো(접속번호);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static Socket সংযোগ_স্থাপনা(String ঠিকনা, int পৰ্ট_মান) throws 입출력예외 {
        try { return new Socket(ঠিকনা, পৰ্ট_মান);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static ServerSocket 듣기(int পৰ্ট_মান) throws 입출력예외 {
        try { return new ServerSocket(পৰ্ট_মান);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public static Socket 받기(ServerSocket ছাৰ্ভাৰ_মান) throws 입출력예외 {
        try { return ছাৰ্ভাৰ_মান.accept();
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
}
