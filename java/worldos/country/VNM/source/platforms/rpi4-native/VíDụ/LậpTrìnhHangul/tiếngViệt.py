"""tựThân giáTrịNhân MicroPython에서 사용하는 한글 Hàm tên."""
import jkoros as HệĐiềuHành
ĐầuRa = print
đọcTệp = HệĐiềuHành.read
ghiTệp = HệĐiềuHành.write
gỡTệp = HệĐiềuHành.remove
đọcĐầuVào = HệĐiềuHành.stdin
vẽHìnhChữNhật = HệĐiềuHành.rect
chờBảnVẽCho = HệĐiềuHành.wait_key
miliGiây = HệĐiềuHành.ticks_ms
mởĐiệnDữLiệu = HệĐiềuHành.udp_open
gửiĐiệnDữLiệu = HệĐiềuHành.udp_send
gửiĐiệnDữLiệuBênNgoài = HệĐiềuHành.udp_sendto
nhậnĐiệnDữLiệu = HệĐiềuHành.udp_recv
đóngMạng = HệĐiềuHành.udp_close

def giảiMãVănBản(DữLiệu):
    return DữLiệu.decode("utf-8")
