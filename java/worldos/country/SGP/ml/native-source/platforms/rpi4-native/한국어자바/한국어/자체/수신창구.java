// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 수신(受信)·പോര്_ട്ട്_മൂല്യം(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class 수신창구 {
    private final java.net.ServerSocket 표준창구;
    private 수신창구(int പോര്_ട്ട്_നമ്പര്) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준창구 = new java.net.ServerSocket(പോര്_ട്ട്_നമ്പര്);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static 수신창구 തുറക്കുക(int പോര്_ട്ട്_നമ്പര്) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return new 수신창구(പോര്_ട്ട്_നമ്പര്);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public കണക്ഷൻ 받기() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return new കണക്ഷൻ(표준창구.accept());
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public int പോര്_ട്ട്_നമ്പര്() { return 표준창구.getLocalPort(); }
    public void ടൈംഔട്ട്(int 밀리초) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public boolean 닫힘() { return 표준창구.isClosed(); }
    public void അടയ്ക്കു() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준창구.close();
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
}
