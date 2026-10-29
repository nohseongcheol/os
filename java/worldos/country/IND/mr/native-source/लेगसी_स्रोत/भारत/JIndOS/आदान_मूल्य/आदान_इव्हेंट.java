// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.आदान_मूल्य;

public final class आदान_इव्हेंट {
    public enum प्रकार_मूल्य {
        कळ_खाली,
        कळ_वर,
        माऊस_हालचाल,
        बटण_दाबलेले,
        बटण_मुक्तकेलेले
    }

    private final प्रकार_मूल्य इव्हेंट_प्रकार;
    private final int पहिले_मूल्य;
    private final int दुसरे_मूल्य;

    public आदान_इव्हेंट(प्रकार_मूल्य इव्हेंट_प्रकार, int पहिले_मूल्य, int दुसरे_मूल्य) {
        this.इव्हेंट_प्रकार = इव्हेंट_प्रकार;
        this.पहिले_मूल्य = पहिले_मूल्य;
        this.दुसरे_मूल्य = दुसरे_मूल्य;
    }

    public प्रकार_मूल्य इव्हेंट_प्रकार() {
        return इव्हेंट_प्रकार;
    }

    public int पहिले_मूल्य() {
        return पहिले_मूल्य;
    }

    public int दुसरे_मूल्य() {
        return दुसरे_मूल्य;
    }
}

