// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** कनॅक्ट(連結)·चॅनल_प्रवेश(通路): 상대와 이어진 TCP बायट_मोल 흐름의 종단. */
public final class कनॅक्शन {
    private final java.net.Socket 표준연결;
    कनॅक्शन(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static कनॅक्शन उगडचें(String नामो, int 접속번호) throws 입출력예외 {
        try {
            return new कनॅक्शन(new java.net.Socket(नामो, 접속번호));
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public 입력흐름 입력() throws 입출력예외 {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public 출력흐름 출력() throws 입출력예외 {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public void कालबाह्य(int 밀리초) throws 입출력예외 {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
    public int 접속번호() { return 표준연결.getPort(); }
    public int 지역접속번호() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void शेवट() throws 입출력예외 {
        try { 표준연결.close();
        } catch (java.io.IOException चूक) { throw 예외변환.I_O(चूक); }
        catch (RuntimeException चूक) { throw 예외변환.पाळो_दिवचो_आदेश(चूक); }
    }
}
