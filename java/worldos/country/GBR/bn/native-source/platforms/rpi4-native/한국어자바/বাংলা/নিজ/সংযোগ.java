// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;

/** সংযোগ_স্থাপনা(連結)·চ্যানেল_ভুক্তি(通路): 상대와 이어진 TCP বাইট_মান 흐름의 종단. */
public final class সংযোগ {
    private final java.net.Socket 표준연결;
    সংযোগ(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static সংযোগ খুলুন(String ইমেইল, int পোর্ট_নম্বর) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try {
            return new সংযোগ(new java.net.Socket(ইমেইল, পোর্ট_নম্বর));
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public 입력흐름 입력() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public 출력흐름 নির্গম() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public void টাইমআউট(int 밀리초) throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
    public int পোর্ট_নম্বর() { return 표준연결.getPort(); }
    public int স্থানীয়_পোর্ট_নম্বর() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void বন্ধ_করুন() throws ইনপুট_আউটপুট_ব্যতিক্রম {
        try { 표준연결.close();
        } catch (java.io.IOException ত্রুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্রুটি); }
        catch (RuntimeException ত্রুটি) { throw 예외변환.কার্যকর_করুন_আদেশ(ত্রুটি); }
    }
}
