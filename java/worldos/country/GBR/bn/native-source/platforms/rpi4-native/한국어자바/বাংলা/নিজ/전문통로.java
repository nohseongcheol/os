// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** 전문(電文)·চ্যানেল_ভুক্তি(通路): 경계를 가진 UDP 자료를 주고받는 종단. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int পোর্ট_নম্বর) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준종단 = 통신.খুলুন(পোর্ট_নম্বর);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public static 전문통로 খুলুন(int পোর্ট_নম্বর) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return new 전문통로(পোর্ট_নম্বর);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public void পাঠান(String ইমেইল, int পোর্ট_নম্বর, String ডাটা) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 통신.পাঠান(표준종단, ইমেইল, পোর্ট_নম্বর, ডাটা);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public String 받기() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public void টাইমআউট(int 밀리초) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 통신.টাইমআউট(표준종단, 밀리초);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public int পোর্ট_নম্বর() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void বন্ধ_করুন() { 통신.বন্ধ_করুন(표준종단); }
}
