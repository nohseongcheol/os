// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package যুক্তরাজ্য.JGbrOS.হোস্ট;

import যুক্তরাজ্য.JGbrOS.কারনেল.কারনেল;

public final class হোস্ট_বুট {
    private হোস্ট_বুট() {
    }

    public static void main(String[] প্যারামিটার_যুক্তি) {
        কারনেল কারনেল_মান = new কারনেল(new হোস্ট_হার্ডওয়্যার());
        কারনেল_মান.চালনা();
        কারনেল_মান.한단계실행();
    }
}

