// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.system_ffeiliau;

public final class ffeil_gwybodaeth {
    private final int Maint;
    private final int 형태;

    public ffeil_gwybodaeth(int Maint, int 형태) {
        this.Maint = Maint;
        this.형태 = 형태;
    }

    public int Maint() {
        return Maint;
    }

    public int 형태() {
        return 형태;
    }
}

