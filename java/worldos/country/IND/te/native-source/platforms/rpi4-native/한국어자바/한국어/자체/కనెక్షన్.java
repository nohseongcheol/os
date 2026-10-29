// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** కనెక్టుచేయి(連結)·ఛానల్_ప్రవేశం(通路): 상대와 이어진 TCP బైట్_మూల్యం 흐름의 종단. */
public final class కనెక్షన్ {
    private final java.net.Socket 표준연결;
    కనెక్షన్(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static కనెక్షన్ తెరువు(String ఇమెయిల్, int పోర్ట్_సంఖ్య) throws మూ_ఫ_మినహాయింపు {
        try {
            return new కనెక్షన్(new java.net.Socket(ఇమెయిల్, పోర్ట్_సంఖ్య));
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public 입력흐름 입력() throws మూ_ఫ_మినహాయింపు {
        try { return new 입력흐름(표준연결.getInputStream());
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public 출력흐름 అవుట్పుట్() throws మూ_ఫ_మినహాయింపు {
        try { return new 출력흐름(표준연결.getOutputStream());
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public void 대기시간(int 밀리초) throws మూ_ఫ_మినహాయింపు {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
    public int పోర్ట్_సంఖ్య() { return 표준연결.getPort(); }
    public int స్థానిక_పోర్ట్_సంఖ్య() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void మూసివేయి() throws మూ_ఫ_మినహాయింపు {
        try { 표준연결.close();
        } catch (java.io.IOException దోషం) { throw 예외변환.మూ_ఫ(దోషం); }
        catch (RuntimeException దోషం) { throw 예외변환.అమలు_చేయి_ఆదేశం(దోషం); }
    }
}
