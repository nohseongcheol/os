// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;

/** मराठी API मधून घोषित करता येणारा, फेकता येणारा आणि पकडता येणारा पत्ता_लुकअप_अपवाद अपवाद. */
public class पत्ता_लुकअप_अपवाद extends इनपुट_आउटपुट_अपवाद {
    public पत्ता_लुकअप_अपवाद() { super(); }
    public पत्ता_लुकअप_अपवाद(String वर्णन) { super(वर्णन); }
    public String वर्णन() { return getMessage(); }
}
