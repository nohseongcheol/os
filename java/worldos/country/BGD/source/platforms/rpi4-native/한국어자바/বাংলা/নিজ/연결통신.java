// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
import java.net.*;
public final class 연결통신 {
    private 연결통신() {}
    public static সংযোগ খুলুন(String ইমেইল, int পোর্ট_নম্বর) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return সংযোগ.খুলুন(ইমেইল, পোর্ট_নম্বর);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static 수신창구 수신열기(int পোর্ট_নম্বর) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return 수신창구.খুলুন(পোর্ট_নম্বর);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static Socket সংযোগ_স্থাপনা(String ইমেইল, int পোর্ট_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return new Socket(ইমেইল, পোর্ট_মান);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static ServerSocket 듣기(int পোর্ট_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return new ServerSocket(পোর্ট_মান);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static Socket 받기(ServerSocket সার্ভার_মান) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return সার্ভার_মান.accept();
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
}
