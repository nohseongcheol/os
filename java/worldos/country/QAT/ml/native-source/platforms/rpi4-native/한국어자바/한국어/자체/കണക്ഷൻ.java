// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** കണക്ടു്_ചെയ്യുക(連結)·ചാനല്_എന്_ട്രി(通路): 상대와 이어진 TCP బైట్_മൂല്യം 흐름의 അവസാനബിന്ദു. */
public final class കണക്ഷൻ {
    private final java.net.Socket 표준연결;
    കണക്ഷൻ(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static കണക്ഷൻ തുറക്കുക(String ഇമെയിൽ, int പോര്_ട്ട്_നമ്പര്) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try {
            return new കണക്ഷൻ(new java.net.Socket(ഇമെയിൽ, പോര്_ട്ട്_നമ്പര്));
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public ഇന്_പുട്ട്_തുടര്_ച്ച 입력() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return new ഇന്_പുട്ട്_തുടര്_ച്ച(표준연결.getInputStream());
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public ഔട്ട്പുട്ട്_തുടര്_ച്ച ഫലം() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return new ഔട്ട്പുട്ട്_തുടര്_ച്ച(표준연결.getOutputStream());
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public void ടൈംഔട്ട്(int 밀리초) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public int പോര്_ട്ട്_നമ്പര്() { return 표준연결.getPort(); }
    public int ലോക്കല്_പോര്_ട്ട്_നമ്പര്() { return 표준연결.getLocalPort(); }
    public boolean 닫힘() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void അടയ്ക്കു() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준연결.close();
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
}
