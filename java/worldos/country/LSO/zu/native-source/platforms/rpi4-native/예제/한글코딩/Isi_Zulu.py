"""자체 ikhenela_inani MicroPython에서 사용하는 한글 umsebenzi_inani Igama."""
import jkoros as isistimu_yokusebenza
출력 = print
파일읽기 = isistimu_yokusebenza.read
bhala_ifayela = isistimu_yokusebenza.write
khipha_ifayela = isistimu_yokusebenza.remove
입력읽기 = isistimu_yokusebenza.stdin
네모그리기 = isistimu_yokusebenza.rect
그림기다리기 = isistimu_yokusebenza.wait_key
밀리초 = isistimu_yokusebenza.ticks_ms
전문통신열기 = isistimu_yokusebenza.udp_open
전문보내기 = isistimu_yokusebenza.udp_send
바깥전문보내기 = isistimu_yokusebenza.udp_sendto
전문받기 = isistimu_yokusebenza.udp_recv
vala_iNethiwekhi = isistimu_yokusebenza.udp_close

def 글해독(imininingwane):
    return imininingwane.decode("utf-8")
