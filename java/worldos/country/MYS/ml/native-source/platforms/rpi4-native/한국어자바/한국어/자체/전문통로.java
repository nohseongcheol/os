// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;

/** 전문(電文)·ചാനല്_എന്_ട്രി(通路): 경계를 가진 UDP 자료를 주고받는 അവസാനബിന്ദു. */
public final class 전문통로 {
    private final java.net.DatagramSocket 표준종단;
    private 전문통로(int പോര്_ട്ട്_നമ്പര്) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 표준종단 = 통신.തുറക്കുക(പോര്_ട്ട്_നമ്പര്);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public static 전문통로 തുറക്കുക(int പോര്_ട്ട്_നമ്പര്) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return new 전문통로(പോര്_ട്ട്_നമ്പര്);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public void അയയ്ക്കുക(String ഇമെയിൽ, int പോര്_ട്ട്_നമ്പര്, String ഡാറ്റാ) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 통신.അയയ്ക്കുക(표준종단, ഇമെയിൽ, പോര്_ട്ട്_നമ്പര്, ഡാറ്റാ);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public String 받기() throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { return 통신.받기(표준종단);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public void ടൈംഔട്ട്(int 밀리초) throws ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്_ഒഴിവാക്കൽ {
        try { 통신.ടൈംഔട്ട്(표준종단, 밀리초);
        } catch (java.io.IOException പിശക്) { throw 예외변환.ഇന്_പുട്ട്_ഔട്ട്_പുട്ട്(പിശക്); }
        catch (RuntimeException പിശക്) { throw 예외변환.നടപ്പാക്കുക_കമാന്_ഡ്(പിശക്); }
    }
    public int പോര്_ട്ട്_നമ്പര്() { return 표준종단.getLocalPort(); }
    public boolean 닫힘() { return 표준종단.isClosed(); }
    public void അടയ്ക്കു() { 통신.അടയ്ക്കു(표준종단); }
}
