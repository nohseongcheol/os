// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package യുണൈറ്റഡ്_അറബ്_എമിറൈറ്റ്_സ്.JAreOS.작업;

import യുണൈറ്റഡ്_അറബ്_എമിറൈറ്റ്_സ്.JAreOS.기억공간.പേജ്_മാനേജര്;
import യുണൈറ്റഡ്_അറബ്_എമിറൈറ്റ്_സ്.JAreOS.ഫയല്_സിസ്റ്റം.파일서술자표;

public final class പ്രോസസ്_മൂല്യം {
    private final int ఐడెంటిఫయర్_മൂല്യം;
    private final int 부모식별자;
    private final പേജ്_മാനേജര്.ഇമെയിൽ_സ്ഥലം ഇമെയിൽ_സ്ഥലം;
    private final 파일서술자표 파일서술자;
    private പ്രോസസ്_അവസ്ഥ അവസ്ഥ_മൂല്യം = പ്രോസസ്_അവസ്ഥ.തയ്യാറാക്കുക;
    private int പുറത്തുകടക്കൽ_കോഡ്;
    private int പ്രോഗ്രാം_ഇടവേള = 0x06000000;
    private int 실행시작주소;
    private String[] 실행인자 = new String[0];
    private String[] 환경값 = new String[0];

    പ്രോസസ്_മൂല്യം(int ఐడెంటిఫయర్_മൂല്യം, int 부모식별자, പേജ്_മാനേജര്.ഇമെയിൽ_സ്ഥലം ഇമെയിൽ_സ്ഥലം, 파일서술자표 파일서술자) {
        this.ఐడెంటిఫయర్_മൂല്യം = ఐడెంటిఫయర్_മൂല്യം;
        this.부모식별자 = 부모식별자;
        this.ഇമെയിൽ_സ്ഥലം = ഇമെയിൽ_സ്ഥലം;
        this.파일서술자 = 파일서술자;
    }

    public int ఐడెంటిఫయర్_മൂല്യം() {
        return ఐడెంటిఫయర్_മൂല്യം;
    }

    public int 부모식별자() {
        return 부모식별자;
    }

    public പേജ്_മാനേജര്.ഇമെയിൽ_സ്ഥലം ഇമെയിൽ_സ്ഥലം() {
        return ഇമെയിൽ_സ്ഥലം;
    }

    public 파일서술자표 파일서술자() {
        return 파일서술자;
    }

    public പ്രോസസ്_അവസ്ഥ അവസ്ഥ_മൂല്യം() {
        return അവസ്ഥ_മൂല്യം;
    }

    public void ഗണം_അവസ്ഥ(പ്രോസസ്_അവസ്ഥ 새상태) {
        അവസ്ഥ_മൂല്യം = 새상태;
    }

    public int പുറത്തുകടക്കൽ_കോഡ്() {
        return പുറത്തുകടക്കൽ_കോഡ്;
    }

    public void പുറത്തുകടക്കൽ_പ്രോഗ്രാം(int മൂല്യം) {
        പുറത്തുകടക്കൽ_കോഡ് = മൂല്യം & 0xff;
        അവസ്ഥ_മൂല്യം = പ്രോസസ്_അവസ്ഥ.പുറത്തുകടക്കൽ_പ്രോഗ്രാം;
    }

    public int പ്രോഗ്രാം_ഇടവേള() {
        return പ്രോഗ്രാം_ഇടവേള;
    }

    public void ഗണം_പ്രോഗ്രാം_ഇടവേള(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("പ്രോഗ്രാം_f5044b9b 끝 범위를 벗어났습니다.");
        }
        പ്രോഗ്രാം_ഇടവേള = 새끝;
    }

    public void 실행문맥설정(int ആരംഭം_ഇമെയിൽ, String[] പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്, String[] 환경) {
        실행시작주소 = ആരംഭം_ഇമെയിൽ;
        실행인자 = പാരാമീറ്റര്_ആര്_ഗ്യുമെന്_റ്.clone();
        환경값 = 환경.clone();
    }

    public int 실행시작주소() { return 실행시작주소; }
    public String[] 실행인자() { return 실행인자.clone(); }
    public String[] 환경값() { return 환경값.clone(); }
}
