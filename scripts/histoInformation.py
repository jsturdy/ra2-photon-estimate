import sys,os
import ROOT as r
from array import array
import math

    #"wjets"  :wjets400SFLO   = 25.22*10*1000/6619651.},
    #"zinv200":zinv200SFLO   = 41.49*5.1*1000/5055885.},#published 5055873.
    #"zinv400":zinv400SFLO   = 5.274*5.1*1000/5105710.},
##xs from jim (where did he get them):
    #ttbar:234 (NLO) somewhere mentioned the NLO*BR = 103.0
    #zmumu200:25.54 (NLO?NNLO?)
    #zmumu400:3.36 (NLO?NNLO?)
    
mcSamples = {
    "qcd250"  :{"scalef":276000.0*10.*1000./27002490.,"scaleflo":276000.0*10.*1000./27002490.,"scalefb":276000.0*10.*1000./27002490.,"color":r.kRed+1},
    "qcd500"  :{"scalef":8426.0*10.*1000./30599239.  ,"scaleflo":8426.0*10.*1000./30599239.  ,"scalefb":8426.0*10.*1000./30599239.  ,"color":r.kRed+2},
    "qcd1000" :{"scalef":204.0*10.*1000./13829995.   ,"scaleflo":204.0*10.*1000./13829995.   ,"scalefb":8426.0*10.*1000./13829995.  ,"color":r.kRed+3},
    "ttjets"  :{"scalef":103.0*10*1000/11081685.     ,"scaleflo":53.2*10*1000/11081685.      ,"scalefb":103.0*10*1000/11081685.     ,"color":r.kBlue},
    "wjets"   :{"scalef":30.08*10*1000/6619651.      ,"scaleflo":25.22*10*1000/6619651.      ,"scalefb":30.08*10*1000/6619651.      ,"color":r.kViolet},
    "gjets200":{"scalef":960.5*10*1000/10494617.     ,"scaleflo":960.5*10*1000/10494617.     ,"scalefb":960.5*10*1000/10494617.     ,"color":r.kOrange+1},
    "gjets400":{"scalef":107.5*10*1000/11146707.     ,"scaleflo":107.5*10*1000/11146707.     ,"scalefb":107.5*10*1000/11146707.     ,"color":r.kOrange+2},
    "zinv200" :{"scalef":49.28*10*1000/5055885.      ,"scaleflo":41.49*10*1000/5055885.      ,"scalefb":49.28*10*1000/5055885.      ,"color":r.kGreen+2},
    "zinv400" :{"scalef":6.26*10*1000/5105710.       ,"scaleflo":5.274*10*1000/5105710.      ,"scalefb":6.26*10*1000/5105710.       ,"color":r.kGreen+3},
    "zmumu200":{"scalef":25.54*10*1000/2694645.      ,"scaleflo":19.73*10*1000/2694645.      ,"scalefb":19.73*10*1000/2694645.      ,"color":r.kCyan+2},
    "zmumu400":{"scalef":3.36*10*1000/2727789.       ,"scaleflo":2.826*10*1000/2727789.      ,"scalefb":2.826*10*1000/2727789.      ,"color":r.kCyan+3},
}

efficiencies = {
#    "base"              :{"cut":"","label":""},
    "acc"               :{"cut":"passAcceptance","label":"pass acceptance"},
    "reco"              :{"cut":"passAcceptance&&passRecoID","label":"pass ID"},
    "recoPixV"          :{"cut":"passAcceptance&&passRecoIDPixV","label":"pass ID (pixel veto"},
    #"recoCSEV"          :{"cut":"passAcceptance&&passRecoIDCSEV","label":"pass ID (CSEV)"},
    "recoPFIso"         :{"cut":"passAcceptance&&passRecoIDPFIso","label":"pass ID and PF Isolation"},
    "recoPixVPFIso"     :{"cut":"passAcceptance&&passRecoIDPFIso&&passRecoIDPixV","label":"pass ID (pixel veto) and PF Isolation"},
    #"recoCSEVPFIso"     :{"cut":"passAcceptance&&passRecoIDPFIso&&passRecoIDCSEV","label":"pass ID (CSEV) and PF Isolation"},
    "recoTight"         :{"cut":"passAcceptance&&passRecoTightID","label":"pass tight ID and PF Isolation"},
    "recoTightPixV"     :{"cut":"passAcceptance&&passRecoTightID&&passRecoIDPixV","label":"pass tight ID (pixel veto) and PF Isolation"},
    #"recoTightCSEV"     :{"cut":"passAcceptance&&passRecoTightID&&passRecoIDCSEV","label":"pass tight ID (CSEV) and PF Isolation"},
    "recoTightPFIso"    :{"cut":"passAcceptance&&passRecoTightID&&passRecoIDPFIso","label":"pass tight ID and PF Isolation"},
    "recoTightPixVPFIso":{"cut":"passAcceptance&&passRecoTightID&&passRecoIDPFIso&&passRecoIDPixV","label":"pass tight ID (pixel veto) and PF Isolation"},
    #"recoTightCSEVPFIso":{"cut":"passAcceptance&&passRecoTightID&&passRecoIDPFIso&&passRecoIDCSEV","label":"pass tight ID (CSEV) and PF Isolation"},
    }

histograms = {"nJetsHT"    :{"title":"N_{Jets}:(p_{T}>50 GeV, |#eta| < 2.5)","bins":15 ,"binrange":[-0.5,14.5],"labels":{"x":"N_{Jets}"         ,"y":"Events/bin"    ,"z":""},"fitrange":[2,7],
                             "varbins":[-0.5+nj for nj in range(16)]},
              "nJetsMHT"   :{"title":"N_{Jets}:(p_{T}>30 GeV, |#eta| < 5.0)","bins":15 ,"binrange":[-0.5,14.5],"labels":{"x":"N_{Jets}"         ,"y":"Events/bin"    ,"z":""},"fitrange":[2,7],
                             "varbins":[-0.5+nj for nj in range(16)]},
              "nGenJetsHT" :{"title":"N_{Jets}:(p_{T}>50 GeV, |#eta| < 2.5)","bins":15 ,"binrange":[-0.5,14.5],"labels":{"x":"N_{Jets}"         ,"y":"Events/bin"    ,"z":""},"fitrange":[2,7],
                             "varbins":[-0.5+nj for nj in range(16)]},
              "nGenJetsMHT":{"title":"N_{Jets}:(p_{T}>30 GeV, |#eta| < 5.0)","bins":15 ,"binrange":[-0.5,14.5],"labels":{"x":"N_{Jets}"         ,"y":"Events/bin"    ,"z":""},"fitrange":[2,7],
                             "varbins":[-0.5+nj for nj in range(16)]},
              "nVtx"       :{"title":"N_{vertices}"                         ,"bins":75 ,"binrange":[-0.5,74.5],"labels":{"x":"N_{vertices}"     ,"y":"Events/bin"    ,"z":""},"fitrange":[8,40],
                             "varbins":[-0.5+nvtx for nvtx in range(76)]},
              #"mhtVal"     :{"title":"#slashH_{T}"                          ,"bins":200,"binrange":[0,1000]   ,"labels":{"x":"#slashH_{T} [GeV]","y":"Events/5 GeV"  ,"z":""},"fitrange":[100,600],
              #"varbins":[]},
              "mhtVal"     :{"title":"#slashH_{T}"                          ,"bins":50,"binrange":[0,1000]   ,"labels":{"x":"#slashH_{T} [GeV]","y":"Events/20 GeV"  ,"z":""},"fitrange":[100,600],
                             "varbins":[mht*20 if mht<15 else 300+(25*(mht-15)) if mht<21 else 450+(50*(mht-21)) if mht<26 else 700+(100*(mht-26)) if mht<30 else 1010 for mht in range(31)]},
              "mhtGenVal"  :{"title":"#slashH_{T}"                          ,"bins":50,"binrange":[0,1000]   ,"labels":{"x":"#slashH_{T} [GeV]","y":"Events/20 GeV"  ,"z":""},"fitrange":[100,600],
                             "varbins":[mht*20 if mht<15 else 300+(25*(mht-15)) if mht<21 else 450+(50*(mht-21)) if mht<26 else 700+(100*(mht-26)) if mht<30 else 1010 for mht in range(31)]},
              "htVal"      :{"title":"H_{T}"                                ,"bins":30,"binrange":[0,3000]   ,"labels":{"x":"H_{T} [GeV]"      ,"y":"Events/100 GeV","z":""},"fitrange":[350,1000],
                             #"varbins":[ht*50 if ht<16 else 800+(100*(ht-16)) if ht<19 else 1100+(200*(ht-19)) if ht<21 else 1500+(250*(ht-21)) if ht < 26 else 3000+(500*(ht-26)) if ht < 27 else 3010 for ht in range(28)]},
                             "varbins":[ht*50 if ht<16 else 800+(100*(ht-16)) if ht<19 else 1100+(200*(ht-19)) if ht<21 else 1500+(250*(ht-21)) if ht < 24 else 2050 for ht in range(25)]},
              "htGenVal"   :{"title":"H_{T}"                                ,"bins":30,"binrange":[0,3000]   ,"labels":{"x":"H_{T} [GeV]"      ,"y":"Events/100 GeV","z":""},"fitrange":[350,1000],
                             "varbins":[ht*50 if ht<16 else 800+(100*(ht-16)) if ht<19 else 1100+(200*(ht-19)) if ht<21 else 1500+(250*(ht-21)) if ht < 24 else 2050 for ht in range(25)]},
                             #"varbins":[ht*50 if ht<16 else 800+(100*(ht-16)) if ht<19 else 1100+(200*(ht-19)) if ht<21 else 1500+(250*(ht-21)) if ht < 26 else 3000+(500*(ht-26)) if ht < 27 else 3010 for ht in range(28)]},
              #"genBosonPt" :{"title":"Boson p_{T}"                          ,"bins":200,"binrange":[0,1000]   ,"labels":{"x":"p_{T} [GeV]"      ,"y":"Events/5 GeV"  ,"z":""},"fitrange":[100,600],
              #"varbins":[]}
              "genBosonPt" :{"title":"Boson p_{T}"                          ,"bins":50,"binrange":[0,1000]   ,"labels":{"x":"p_{T} [GeV]"      ,"y":"Events/20 GeV"  ,"z":""},"fitrange":[100,600],
                             "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "genBosonEta":{"title":"Boson #eta"                           ,"bins":50,"binrange":[-5,5]     ,"labels":{"x":"#eta"             ,"y":"Events/bin"    ,"z":""},"fitrange":[-5,5],
                             "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "genBosonMinDR":{"title":"#Delta R_{min}(boson,jet)"          ,"bins":40,"binrange":[0,1]      ,"labels":{"x":"#Delta R"         ,"y":"Events/bin"    ,"z":""},"fitrange":[0,1],
                               "varbins":[0+(dr/40) for dr in range(41)]},
              ###jet histograms
              "jet1Pt" :{"title":"Jet_{1} p_{T}",                          "bins":30,"binrange":[0,1500],  "labels":{"x":"p_{T} [GeV]","y":"Events/50 GeV","z":""},"fitrange":[],
                         "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "jet2Pt" :{"title":"Jet_{2} p_{T}",                          "bins":40,"binrange":[0,1000],  "labels":{"x":"p_{T} [GeV]","y":"Events/25 GeV","z":""},"fitrange":[],
                         "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "jet3Pt" :{"title":"Jet_{3} p_{T}",                          "bins":32,"binrange":[0,800],   "labels":{"x":"p_{T} [GeV]","y":"Events/25 GeV","z":""},"fitrange":[],
                         "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "jet4Pt" :{"title":"Jet_{4} p_{T}",                          "bins":32,"binrange":[0,800],   "labels":{"x":"p_{T} [GeV]","y":"Events/25 GeV","z":""},"fitrange":[],
                         "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "jet1Eta":{"title":"Jet_{1} #eta",                           "bins":50,"binrange":[-5.0,5.0],"labels":{"x":"#eta"       ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                         "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "jet2Eta":{"title":"Jet_{2} #eta",                           "bins":50,"binrange":[-5.0,5.0],"labels":{"x":"#eta"       ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                         "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "jet3Eta":{"title":"Jet_{3} #eta",                           "bins":50,"binrange":[-5.0,5.0],"labels":{"x":"#eta"       ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                         "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "jet4Eta":{"title":"Jet_{4} #eta",                           "bins":50,"binrange":[-5.0,5.0],"labels":{"x":"#eta"       ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                         "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "dphi1"  :{"title":"#Delta#phi(Jet_{1},#slashH_{T})",        "bins":20,"binrange":[0,3.2],   "labels":{"x":"#Delta#phi" ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                         "varbins":[0+(phi*(3.2/20)) for phi in range(21)]},
              "dphi2"  :{"title":"#Delta#phi(Jet_{2},#slashH_{T})",        "bins":20,"binrange":[0,3.2],   "labels":{"x":"#Delta#phi" ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                         "varbins":[0+(phi*(3.2/20)) for phi in range(21)]},
              "dphi3"  :{"title":"#Delta#phi(Jet_{3},#slashH_{T})",        "bins":20,"binrange":[0,3.2],   "labels":{"x":"#Delta#phi" ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                         "varbins":[0+(phi*(3.2/20)) for phi in range(21)]},
              "dphimin":{"title":"#Delta#phi_{min}(Jet_{all},#slashH_{T})","bins":20,"binrange":[0,3.2],   "labels":{"x":"#Delta#phi" ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                         "varbins":[0+(phi*(3.2/20)) for phi in range(21)]},
              
              ###photon histograms
              "nPhotonsID"   :{"title":"N_{#gamma}:(ID)"                           ,"bins":4 ,"binrange":[-0.5,3.5],"labels":{"x":"N_{#gamma}","y":"Events/bin"    ,"z":""},"fitrange":[],
                               "varbins":[-0.5+nph for nph in range(5)]},
              "nPhotonsLoose":{"title":"N_{#gamma}:(Iso_{PF-EA#cdot#rho} Loose WP)","bins":4 ,"binrange":[-0.5,3.5],"labels":{"x":"N_{#gamma}","y":"Events/bin"    ,"z":""},"fitrange":[],
                               "varbins":[-0.5+nph for nph in range(5)]},
              "nPhotonsTight":{"title":"N_{#gamma}:(Iso_{PF-EA#cdot#rho} Tight WP)","bins":4 ,"binrange":[-0.5,3.5],"labels":{"x":"N_{#gamma}","y":"Events/bin"    ,"z":""},"fitrange":[],
                               "varbins":[-0.5+nph for nph in range(5)]},
              #"photonPt"    :{"title":"#gamma p_{T}"               ,"bins":100,"binrange":[0,1000],"labels":{"x":"p_{T} [GeV]"         ,"y":"Events/10 GeV","z":""},"fitrange":[100,600],
              #"varbins":[]},
              "photonPt"    :{"title":"#gamma p_{T}"               ,"bins":40,"binrange":[0,1000],"labels":{"x":"p_{T} [GeV]"         ,"y":"Events/25 GeV","z":""},"fitrange":[100,600],
                              "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "photonEta"   :{"title":"#gamma #eta"                ,"bins":50 ,"binrange":[-5,5]  ,"labels":{"x":"#eta"                ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                              "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "photonMinDR" :{"title":"#Delta R_{min}(#gamma,jet)" ,"bins":40 ,"binrange":[0,1]   ,"labels":{"x":"#Delta R"            ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                              "varbins":[0+(dr/40) for dr in range(41)]},
              "photonPhi"   :{"title":"#gamma #phi"                ,"bins":20 ,"binrange":[0,3.2] ,"labels":{"x":"#phi"                ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                              "varbins":[0+(phi*(3.2/20)) for phi in range(21)]},
              "photonpfCH"  :{"title":"#gamma ISO_{PF}^{h^{#pm}}"  ,"bins":40 ,"binrange":[0,1]   ,"labels":{"x":"ISO_{PF}^{h^{#pm}} [GeV]" ,"y":"Events/bin","z":""},"fitrange":[],
                              "varbins":[0+(x/40) for x in range(41)]},
              "photonpfNU"  :{"title":"#gamma ISO_{PF}^{h^{0}}"    ,"bins":30 ,"binrange":[0,15]  ,"labels":{"x":"ISO_{PF}^{h^{0}} [GeV]" ,"y":"Events/bin","z":""},"fitrange":[],
                              "varbins":[0+(x*(15/30)) for x in range(31)]},
              "photonpfGA"  :{"title":"#gamma ISO_{PF}^{#gamma}"   ,"bins":25 ,"binrange":[0,5]   ,"labels":{"x":"ISO_{PF}^{#gamma} [GeV]","y":"Events/bin","z":""},"fitrange":[],
                              "varbins":[0+(x*(5/25)) for x in range(26)]},
              "photonHoverE":{"title":"#gamma H/EM"                ,"bins":25 ,"binrange":[0.1,10],"labels":{"x":"H/EM"                ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                              "varbins":[0.1+(x*(10/25)) for x in range(26)]},
              "photonSieie" :{"title":"#gamma #sigma_{i#eta i#eta}","bins":40 ,"binrange":[0,0.04],"labels":{"x":"#sigma_{i#eta i#eta}","y":"Events/bin"   ,"z":""},"fitrange":[],
                              "varbins":[0+(x*(0.04/40)) for x in range(41)]},
              
              ###muon histograms
              "muon1Pt" :{"title":"#mu_{1} p_{T}"  ,"bins":100,"binrange":[0,1000],"labels":{"x":"p_{T} [GeV]"  ,"y":"Events/10 GeV","z":""},"fitrange":[100,600],
                          "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "muon1M"  :{"title":"#mu_{1} M_{inv}","bins":40 ,"binrange":[0,200] ,"labels":{"x":"M_{#mu} [GeV]","y":"Events/5 GeV" ,"z":""},"fitrange":[],
                          "varbins":[]},
              "muon1Eta":{"title":"#mu_{1} #eta"   ,"bins":50 ,"binrange":[-5,5]  ,"labels":{"x":"#eta"         ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                          "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "muon1Phi":{"title":"#mu_{1} #phi"   ,"bins":20 ,"binrange":[0,3.2] ,"labels":{"x":"#phi"         ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                          "varbins":[0+(phi*(3.2/20)) for phi in range(21)]},
              
              "muon2Pt" :{"title":"#mu_{2} p_{T}"  ,"bins":100,"binrange":[0,1000],"labels":{"x":"p_{T} [GeV]"  ,"y":"Events/10 GeV","z":""},"fitrange":[100,600],
                          "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "muon2M"  :{"title":"#mu_{2} M_{inv}","bins":40 ,"binrange":[0,200] ,"labels":{"x":"M_{#mu} [GeV]","y":"Events/5 GeV" ,"z":""},"fitrange":[],
                          "varbins":[]},
              "muon2Eta":{"title":"#mu_{2} #eta"   ,"bins":50 ,"binrange":[-5,5]  ,"labels":{"x":"#eta"         ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                          "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "muon2Phi":{"title":"#mu_{2} #phi"   ,"bins":20 ,"binrange":[0,3.2] ,"labels":{"x":"#phi"         ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                          "varbins":[0+(phi*(3.2/20)) for phi in range(21)]},
              
              "dimuonPt" :{"title":"#mu#mu p_{T}"  ,"bins":100,"binrange":[0,1000],"labels":{"x":"p_{T} [GeV]"     ,"y":"Events/10 GeV","z":""},"fitrange":[100,600],
                           "varbins":[pt*20 if pt<15 else 300+(25*(pt-15)) if pt<21 else 450+(50*(pt-21)) if pt<26 else 700+(100*(pt-26)) if pt<30 else 1010 for pt in range(31)]},
              "dimuonM"  :{"title":"#mu#mu M_{inv}","bins":100,"binrange":[0,200] ,"labels":{"x":"M_{#mu#mu} [GeV]","y":"Events/5 GeV" ,"z":""},"fitrange":[],
                           "varbins":[]},
              "dimuonEta":{"title":"#mu#mu #eta"   ,"bins":50 ,"binrange":[-5,5]  ,"labels":{"x":"#eta"            ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                           "varbins":[-5+(eta*((5-(-5))/50)) for eta in range(51)]},
              "dimuonPhi":{"title":"#mu#mu #phi"   ,"bins":20 ,"binrange":[0,3.2] ,"labels":{"x":"#phi"            ,"y":"Events/bin"   ,"z":""},"fitrange":[],
                           "varbins":[0+(phi*(3.2/20)) for phi in range(21)]},
              "dimuonMinDR":{"title":"#Delta R_{min}(#mu#mu,jet)","bins":20 ,"binrange":[0,1],"labels":{"x":"#Delta R","y":"Events/bin"   ,"z":""},"fitrange":[],
                             "varbins":[0+(dr/20) for dr in range(21)]},
              }


cutSeries = [
    ["h_Total_",        r.kYellow ,"No Cuts"],
    ["h_HTCuts_",       r.kGreen  ,"H_{T} > 500 GeV"],
    ["h_MHTCuts_",      r.kOrange ,"#slashH_{T} > 200 GeV"],
    ["h_DPhiCuts_",     r.kGreen+4,"#Delta#phi Cuts"],
    ["h_HTDPhiCuts_",   r.kViolet ,"H_{T} > 500 and #Delta#phi Cuts"],
    ["h_MHTDPhiCuts_",  r.kRed    ,"#slashH_{T} > 200 and #Delta#phi Cuts"],
    ["h_HTMHTCuts_",    r.kBlue   ,"H_{T} > 500 and #slashH_{T} > 200"],
    ["h_HTMHTDPhiCuts_",r.kBlack  ,"H_{T} > 500, #slashH_{T} > 200, and #Delta#phi Cuts"],
    ["h_HTBin1MHTBin1_",r.kRed     ,"#splitline{500 < H_{T} < 900}{ 200 < #slashH_{T} < 350}"],
    ["h_HTBin2MHTBin1_",r.kRed+3   ,"#splitline{900 < H_{T} < 1300}{ 200 < #slashH_{T} < 350}"],
    ["h_HTBin3MHTBin1_",r.kOrange  ,"#splitline{1300 < H_{T}}{ 200 < #slashH_{T} < 350}"],
    ["h_HTBin1MHTBin2_",r.kGreen+3 ,"#splitline{500 < H_{T} < 900}{ 350 < #slashH_{T} < 500}"],
    ["h_HTBin2MHTBin2_",r.kBlue    ,"#splitline{900 < H_{T} < 1300}{ 350 < #slashH_{T} < 500}"],
    ["h_HTBin3MHTBin2_",r.kBlue+3  ,"#splitline{1300 < H_{T}}{ 350 < #slashH_{T} < 500}"],
    ["h_HTBin1MHTBin3_",r.kYellow+3,"#splitline{500 < H_{T} < 900}{ 500 < #slashH_{T}}"],
    ["h_HTBin2MHTBin3_",r.kCyan+3  ,"#splitline{900 < H_{T} < 1300}{ 500 < #slashH_{T}}"],
    ["h_HTBin3MHTBin3_",r.kViolet  ,"#splitline{1300 < H_{T}}{ 500 < #slashH_{T}}"],
    ]

ptSeries = [
    ["",      "p_{T} > 0 GeV"],
    ["Pt50_", "p_{T} > 50 GeV"],
    ["Pt100_","p_{T} > 100 GeV"],
    ["Pt150_","p_{T} > 150 GeV"],
    ["Pt200_","p_{T} > 200 GeV"]
    ##    "",
    ##    "Pt50_",
    ##    "Pt100_",
    ##    "Pt150_",
    ##    "Pt200_",
    ]

minvSeries = [
    "",
    "MInv"
    ]

analysisCuts = {
    "photon":{#"tightidpixel":"photonPixelVeto>0",
              #"tightidcsev" :"photonEConvVeto>0",
              "tightisopixel":"nPhotonsTight==1&&photonPixelVeto>0",
              "tightisocsev" :"nPhotonsTight==1&&photonEConvVeto>0",
              },
    "dimuon":{"basic":"abs(muon1Eta)<2.1&&abs(muon2Eta)<2.1&&abs(dimuonM-91.2)<20.0"}
    }
