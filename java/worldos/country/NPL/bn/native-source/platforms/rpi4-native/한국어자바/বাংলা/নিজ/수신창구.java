// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** 수신(受信)·পোর্ট_মান(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int পোর্ট_নম্বর) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준창구 = new java.net.ServerSocket(পোর্ট_নম্বর);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static 수신창구 খুলুন(int পোর্ট_নম্বর) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return new 수신창구(পোর্ট_নম্বর);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public সংযোগ 받기() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return new সংযোগ(표준창구.accept());
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public int পোর্ট_নম্বর() { return 표준창구.getLocalPort(); }
    public void টাইমআউট(int 밀리초) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void বন্ধ_করুন() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준창구.close();
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
}
