// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** সংযোগ_স্থাপনা(連結)·চেনেল_প্রবিষ্ট(通路): 상대와 이어진 TCP বাইট_মান 흐름의 종단. */
public final class সংযোগ {
    private final java.net.Socket 표준연결;
    সংযোগ(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static সংযোগ খোলো(String ঠিকনা, int 접속번호) throws 입출력예외 {
        try {
            return new সংযোগ(new java.net.Socket(ঠিকনা, 접속번호));
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public 출력흐름 নিৰ্গম() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public void 대기시간(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void বন্ধ_কৰক() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException ত্ৰুটি) { throw 예외변환.ইনপুট_আউটপুট(ত্ৰুটি); }
        catch (RuntimeException ত্ৰুটি) { throw 예외변환.নিষ্পাদন_আদেশ(ত্ৰুটি); }
    }
}
