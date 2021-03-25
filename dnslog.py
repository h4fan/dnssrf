# -*- coding: utf-8 -*-

"""
    FixedResolver - example resolver which responds with fixed response
                    to all requests
"""

from __future__ import print_function

import copy,binascii

from dnslib import RR,QTYPE,A,TXT
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger
from dbop import log2db

from config import ACME_challenge_DOMAIN,ACME_challenge_TXT_Record,SERVER_IP,REBIND_DOMAIN,REBIND_DOMAIN_VALUE

rebindflag = 0

class FixedResolver(BaseResolver):
    """
        Respond with fixed response to all requests
    """
    def __init__(self,zone):
        # Parse RRs
        self.rrs = RR.fromZone(zone)

    def resolve(self,request,handler):
        reply = request.reply()
        qname = request.q.qname
        if(qname == ACME_challenge_DOMAIN):
            reply.add_answer(RR(qname,QTYPE.TXT,ttl=0,rdata=TXT(ACME_challenge_TXT_Record)))
        elif(qname == REBIND_DOMAIN):
            global rebindflag
            reply.add_answer(RR(qname,QTYPE.A,ttl=0,rdata=A(REBIND_DOMAIN_VALUE[rebindflag])))
            rebindflag = (rebindflag + 1) % 2
        else:
        # Replace labels with request label
            reply.add_answer(RR(qname,QTYPE.A,ttl=0,rdata=A(SERVER_IP)))

            #reply.add_answer(a)
        return reply


class CustomLogger(DNSLogger):
    def __init__(self,log="",prefix=True):
        super(CustomLogger,self).__init__(log,prefix)

    def log_request(self,handler,request):
        
        # print("%sRequest: [%s:%d] (%s) / '%s' (%s)" % (
        #             self.log_prefix(handler),
        #             handler.client_address[0],
        #             handler.client_address[1],
        #             handler.protocol,
        #             request.q.qname,
        #             QTYPE[request.q.qtype]))
        #self.log_data(request)
        log2db(handler.client_address[0],"DNS",request.q.qname,str(QTYPE[request.q.qtype])+'|'+str(request.q.qname))

    def log_data(self,dnsobj):
        print("\n",dnsobj.toZone("    "),"\n",sep="")

if __name__ == '__main__':

    import argparse,sys,time

    p = argparse.ArgumentParser(description="Fixed DNS Resolver")
    p.add_argument("--response","-r",default=". 60 IN A 127.0.0.1",
                    metavar="<response>",
                    help="DNS response (zone format) (default: 127.0.0.1)")
    p.add_argument("--zonefile","-f",
                    metavar="<zonefile>",
                    help="DNS response (zone file, '-' for stdin)")
    p.add_argument("--port","-p",type=int,default=53,
                    metavar="<port>",
                    help="Server port (default:53)")
    p.add_argument("--address","-a",default="",
                    metavar="<address>",
                    help="Listen address (default:all)")
    p.add_argument("--udplen","-u",type=int,default=0,
                    metavar="<udplen>",
                    help="Max UDP packet length (default:0)")
    p.add_argument("--tcp",action='store_true',default=False,
                    help="TCP server (default: UDP only)")
    p.add_argument("--log",default="request,reply,truncated,error",
                    help="Log hooks to enable (default: +request,+reply,+truncated,+error,-recv,-send,-data)")
    p.add_argument("--log-prefix",action='store_true',default=False,
                    help="Log prefix (timestamp/handler/resolver) (default: False)")
    args = p.parse_args()

    if args.zonefile:
        if args.zonefile == '-':
            args.response = sys.stdin
        else:
            args.response = open(args.zonefile)

    resolver = FixedResolver(args.response)
    logger = CustomLogger(args.log,args.log_prefix)

    print("Starting Fixed Resolver (%s:%d) [%s]" % (
                        args.address or "*",
                        args.port,
                        "UDP/TCP" if args.tcp else "UDP"))

    for rr in resolver.rrs:
        print("    | ",rr.toZone().strip(),sep="")

    if args.udplen:
        DNSHandler.udplen = args.udplen

    udp_server = DNSServer(resolver,
                           port=args.port,
                           address=args.address,
                           logger=logger)
    udp_server.start_thread()

    if args.tcp:
        tcp_server = DNSServer(resolver,
                               port=args.port,
                               address=args.address,
                               tcp=True,
                               logger=logger)
        tcp_server.start_thread()

    while udp_server.isAlive():
        time.sleep(1)
