// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा अनुपस्थित_संचिका_अपवाद अपवाद. */
public class अनुपस्थित_संचिका_अपवाद extends इनपुट_आउटपुट_अपवाद {
    public अनुपस्थित_संचिका_अपवाद() { super(); }
    public अनुपस्थित_संचिका_अपवाद(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
