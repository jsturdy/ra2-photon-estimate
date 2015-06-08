import sys,os
import ROOT as r
from array import array
import math
import optparse
import histoInformation as histoInfo
from specialFunctions import mkdir_p
import rootGarbageCollection
########Main
def main() :
    parser = optparse.OptionParser(description="Driver parameters for makeGenRatioPlots.py")
    parser.add_option('-d', '--debug',   action="store_true", default=False, dest="debug")
    parser.add_option('-n', '--nnlo',    action="store_true", default=False, dest="useNNLO")
    parser.add_option('-o', '--outDir',  type='string', action="store", default="/tmp", dest="outDir")
    parser.add_option('-i', '--inDir',   type='string', action="store", default="/tmp", dest="inDir")

    options, args = parser.parse_args()
    if options.debug:
    #    raw_input("Press Enter to begin...")
        r.gROOT.SetBatch(True)
    else:
        r.gROOT.SetBatch(True)
        
    sfSource = "scaleflo"
    sfSuffix = "LO"
    if options.useNNLO:
        sfSource = "scalef"
        sfSuffix = "NNLO"
        
    mkdir_p("%s"%(options.outDir))
    #outputFile = r.TFile("dataMCplots.root","RECREATE")
    outputFile = r.TFile("%s/dataMCplots_%s_v1.root"%(options.outDir,sfSuffix),"RECREATE")

    dataChain   = r.TChain("reco")
    signalChain = r.TChain("reco")
    qcdChain    = r.TChain("reco")
    ttjetsChain = r.TChain("reco")
    wjetsChain  = r.TChain("reco")
    zinvChain   = r.TChain("reco")
    #bkgdChains = r.TChain("reco")

    dataChain.Add(  "%s/recoTreeDR0.0_photon2012abcd.root"%(options.inDir))
    signalChain.Add("%s/recoTreeDR0.0_gjets.root"%(         options.inDir))
    qcdChain.Add(   "%s/recoTreeDR0.0_qcd.root"%(           options.inDir))
    ttjetsChain.Add("%s/recoTreeDR0.0_photon_ttbar.root"%(  options.inDir))
    wjetsChain.Add( "%s/recoTreeDR0.0_wjets.root"%(         options.inDir))
    zinvChain.Add(  "%s/recoTreeDR0.0_zinv.root"%(          options.inDir))
    #bkgdChains.Add("%s/recoTreeDR0.0_qcd.root"%(options.inDir))
    #bkgdChains.Add("%s/recoTreeDR0.0_photon_ttbar.root"%(options.inDir))
    #bkgdChains.Add("%s/recoTreeDR0.0_wjets.root"%(options.inDir))

    htHistBins = [0,100,200,300,400,500,600,700,800,900,
                  1000,1200,1500,2000
                  ]
    mhtHistBins = [0,50,100,150,
                   200,250,300,350,
                   400,450,550,650,
                   800,1000
                   ]
    
    print dataChain.GetEntries()
    print signalChain.GetEntries()
    print qcdChain.GetEntries()
    print ttjetsChain.GetEntries()
    print wjetsChain.GetEntries()
    print zinvChain.GetEntries()

    gjetsDataInputs    = []
    gjets200Inputs     = []
    gjets400Inputs     = []
    gjetsQCD250Inputs  = []
    gjetsQCD500Inputs  = []
    gjetsQCD1000Inputs = []
    gjetsTTBarInputs   = []
    gjetsWJetsInputs   = []

    gjetsDataNJets    = []
    gjets200NJets     = []
    gjets400NJets     = []
    gjetsMCNJets      = []
    gjetsQCD250NJets  = []
    gjetsQCD500NJets  = []
    gjetsQCD1000NJets = []
    gjetsQCDNJets     = []
    gjetsTTBarNJets   = []
    gjetsWJetsNJets   = []
    gjetsTotNJets     = []

    zmumuDATAInputFile  = r.TFile("histos_sel0_dimuData_per3-9_muWgt.root","READ")
    zmumu200MCInputFile = r.TFile("histos_sel0_DYmuHT200_muWgt.root","READ")
    zmumu400MCInputFile = r.TFile("histos_sel0_DYmuHT400_muWgt.root","READ")
    zmumuBkgdInputFile  = r.TFile("histos_sel0_ttbar_muWgt.root","READ")

    zinv200Inputs     = []
    zinv400Inputs     = []

    zinv200NJets     = []
    zinv400NJets     = []
    zinvMCNJets      = []

    cuts = "htVal>500&&mhtVal>100&&dphi1>0.5&&dphi2>0.5&&dphi3>0.3&&passRA2ElVeto&&passRA2MuVeto&&%s"%(
    #cuts = "htVal>500&&mhtVal>100&&dphi1>0.5&&dphi2>0.5&&dphi3>0.3&&passElVeto&&passMuVeto&&%s"%(
    #cuts = "htVal>500&&mhtVal>100&&dphi1>0.5&&dphi2>0.5&&dphi3>0.3&&%s"%(
        histoInfo.analysisCuts["photon"]["tightisopixel"])
    jetCuts = [
        #["nJetsHT>=2",0],
        ["nJetsHT==2",1],
        ["nJetsHT==3",2],
        ["nJetsHT==4",3],
        ["nJetsHT==5",4],
        ["nJetsHT==6",5],
        ["nJetsHT==7",6],
        ["nJetsHT>=8",7],
        #["nJetsHT>=3&&nJetsHT<=5",8],
        #["nJetsHT>=6&&nJetsHT<=7",9],
        ]

    outputFile.cd()
    for j,cut in enumerate(jetCuts):
        print "%s&&%s"%(cuts,cut[0])
        gjetsDataInputs   .append(r.TH2D("photon_%s_hhtmht2D_nj%d"%("data"    ,cut[1]),
                                         "photon_%s_hhtmht2D_nj%d"%("data"    ,cut[1]),
                                         25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        gjets200Inputs    .append(r.TH2D("photon_%s_hhtmht2D_nj%d"%("gjets200",cut[1]),
                                         "photon_%s_hhtmht2D_nj%d"%("gjets200",cut[1]),
                                         25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        gjets400Inputs    .append(r.TH2D("photon_%s_hhtmht2D_nj%d"%("gjets400",cut[1]),
                                         "photon_%s_hhtmht2D_nj%d"%("gjets400",cut[1]),
                                         25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        gjetsQCD250Inputs .append(r.TH2D("photon_%s_hhtmht2D_nj%d"%("qcd250"  ,cut[1]),
                                         "photon_%s_hhtmht2D_nj%d"%("qcd250"  ,cut[1]),
                                         25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        gjetsQCD500Inputs .append(r.TH2D("photon_%s_hhtmht2D_nj%d"%("qcd500"  ,cut[1]),
                                         "photon_%s_hhtmht2D_nj%d"%("qcd500"  ,cut[1]),
                                         25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        gjetsQCD1000Inputs.append(r.TH2D("photon_%s_hhtmht2D_nj%d"%("qcd1000" ,cut[1]),
                                         "photon_%s_hhtmht2D_nj%d"%("qcd1000" ,cut[1]),
                                         25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        gjetsTTBarInputs  .append(r.TH2D("photon_%s_hhtmht2D_nj%d"%("ttjets" ,cut[1]),
                                         "photon_%s_hhtmht2D_nj%d"%("ttjets" ,cut[1]),
                                         25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        gjetsWJetsInputs  .append(r.TH2D("photon_%s_hhtmht2D_nj%d"%("wjets"  ,cut[1]),
                                         "photon_%s_hhtmht2D_nj%d"%("wjets"  ,cut[1]),
                                         25,0,2500,20,0,1000))##50,0,5000,40,0,2000))

        gjetsDataInputs   [j].Sumw2()
        gjets200Inputs    [j].Sumw2()
        gjets400Inputs    [j].Sumw2()
        gjetsQCD250Inputs [j].Sumw2()
        gjetsQCD500Inputs [j].Sumw2()
        gjetsQCD1000Inputs[j].Sumw2()
        gjetsTTBarInputs  [j].Sumw2()
        gjetsWJetsInputs  [j].Sumw2()

        zinv200Inputs.append(r.TH2D("zinv_%s_hhtmht2D_nj%d"%("zinv200",cut[1]),
                                    "zinv_%s_hhtmht2D_nj%d"%("zinv200",cut[1]),
                                    25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        zinv400Inputs.append(r.TH2D("zinv_%s_hhtmht2D_nj%d"%("zinv400",cut[1]),
                                    "zinv_%s_hhtmht2D_nj%d"%("zinv400",cut[1]),
                                    25,0,2500,20,0,1000))##50,0,5000,40,0,2000))
        zinv200Inputs[    j].Sumw2()
        zinv400Inputs[    j].Sumw2()

    #if options.debug:
    #    raw_input("Press Enter to begin...")
    for j,cut in enumerate(jetCuts):

        if options.debug:
            print gjetsDataInputs[j]
            print "mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("data",cut[1])
            print "%s&&%s"%(cuts,cut[0])
        dataChain  .Draw("mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("data"    ,cut[1]),
                         "%s&&%s"%(cuts,cut[0]),"colz")
        if options.debug:
            print "data histogram has %d entries"%(gjetsDataInputs[j].GetEntries())
            print gjets200Inputs[j]
            print histoInfo.mcSamples["gjets200"]["scalef"]
            print "mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("gjets200",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["gjets200"]["scalef"],
                                                      1.1*histoInfo.mcSamples["gjets200"]["scalef"])
        signalChain.Draw("mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("gjets200",cut[1]),
                         "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                             0.9*histoInfo.mcSamples["gjets200"]["scalef"],
                                                             1.1*histoInfo.mcSamples["gjets200"]["scalef"]),"colz")
        if options.debug:
            print "gjets200 histogram has %d entries"%(gjets200Inputs[j].GetEntries())
            print gjets400Inputs[j]
            print histoInfo.mcSamples["gjets400"]["scalef"]
            print "mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("gjets400",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["gjets400"]["scalef"],
                                                      1.1*histoInfo.mcSamples["gjets400"]["scalef"])
        signalChain.Draw("mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("gjets400",cut[1]),
                         "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                             0.9*histoInfo.mcSamples["gjets400"]["scalef"],
                                                             1.1*histoInfo.mcSamples["gjets400"]["scalef"]),"colz")
        if options.debug:
            print "gjets400 histogram has %d entries"%(gjets400Inputs[j].GetEntries())
            print gjetsQCD250Inputs[j]
            print histoInfo.mcSamples["qcd250"]["scalef"]
            print "mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("qcd250",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["qcd250"]["scalef"],
                                                      1.1*histoInfo.mcSamples["qcd250"]["scalef"])
        qcdChain   .Draw("mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("qcd250"  ,cut[1]),
                         "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                             0.9*histoInfo.mcSamples["qcd250"]["scalef"],
                                                             1.1*histoInfo.mcSamples["qcd250"]["scalef"]),"colz")
        if options.debug:
            print "qcd250 histogram has %d entries"%(gjetsQCD250Inputs[j].GetEntries())
            print gjetsQCD500Inputs[j]
            print histoInfo.mcSamples["qcd500"]["scalef"]
            print "mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("qcd500",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["qcd500"]["scalef"],
                                                      1.1*histoInfo.mcSamples["qcd500"]["scalef"])
        qcdChain   .Draw("mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("qcd500"  ,cut[1]),
                         "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                             0.9*histoInfo.mcSamples["qcd500"]["scalef"],
                                                             1.1*histoInfo.mcSamples["qcd500"]["scalef"]),"colz")
        if options.debug:
            print "qcd500 histogram has %d entries"%(gjetsQCD500Inputs[j].GetEntries())
            print gjetsQCD1000Inputs[j]
            print histoInfo.mcSamples["qcd1000"]["scalef"]
            print "mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("qcd1000",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["qcd1000"]["scalef"],
                                                      1.1*histoInfo.mcSamples["qcd1000"]["scalef"])
        qcdChain   .Draw("mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("qcd1000" ,cut[1]),
                         "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                             0.9*histoInfo.mcSamples["qcd1000"]["scalef"],
                                                             1.1*histoInfo.mcSamples["qcd1000"]["scalef"]),"colz")
        if options.debug:
            print "qcd1000 histogram has %d entries"%(gjetsQCD1000Inputs[j].GetEntries())
            print gjetsTTBarInputs[j]
            print histoInfo.mcSamples["ttjets"]["scalef"]
            print "mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("ttjets",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["ttjets"]["scalef"],
                                                      1.1*histoInfo.mcSamples["ttjets"]["scalef"])
        ttjetsChain.Draw("mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("ttjets"     ,cut[1]),
                         "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                             0.9*histoInfo.mcSamples["ttjets"]["scalef"],
                                                             1.1*histoInfo.mcSamples["ttjets"]["scalef"]),"colz")
        if options.debug:
            print "ttjets histogram has %d entries"%(gjetsTTBarInputs[j].GetEntries())
            print gjetsWJetsInputs[j]
            print histoInfo.mcSamples["wjets"]["scalef"]
            print "mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("wjets",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["wjets"]["scalef"],
                                                      1.1*histoInfo.mcSamples["wjets"]["scalef"])
        wjetsChain .Draw("mhtVal:htVal>>photon_%s_hhtmht2D_nj%d"%("wjets"      ,cut[1]),
                         "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                             0.9*histoInfo.mcSamples["wjets"]["scalef"],
                                                             1.1*histoInfo.mcSamples["wjets"]["scalef"]),"colz")
        
        if options.debug:
            print "wjets histogram has %d entries"%(gjetsWJetsInputs[j].GetEntries())
        gjetsDataInputs[j]   .Write()
        gjets200Inputs[j]    .Write()
        gjets400Inputs[j]    .Write()
        gjetsQCD250Inputs[j] .Write()
        gjetsQCD500Inputs[j] .Write()
        gjetsQCD1000Inputs[j].Write()
        gjetsTTBarInputs[j]  .Write()
        gjetsWJetsInputs[j]  .Write()

        ###ZInvisible plots
        cuts = "htVal>500&&mhtVal>100&&dphi1>0.5&&dphi2>0.5&&dphi3>0.3"
        if options.debug:
            print zinv200Inputs[j]
            print histoInfo.mcSamples["zinv200"]["scalef"]
            print "mhtVal:htVal>>zinv_%s_hhtmht2D_nj%d"%("zinv200",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["zinv200"]["scalef"],
                                                      1.1*histoInfo.mcSamples["zinv200"]["scalef"])
        zinvChain.Draw("mhtVal:htVal>>zinv_%s_hhtmht2D_nj%d"%("zinv200",cut[1]),
                       "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                           0.9*histoInfo.mcSamples["zinv200"]["scalef"],
                                                           1.1*histoInfo.mcSamples["zinv200"]["scalef"]),"colz")
        if options.debug:
            print "zinv200 histogram has %d entries"%(zinv200Inputs[j].GetEntries())
            print zinv400Inputs[j]
            print histoInfo.mcSamples["zinv400"]["scalef"]
            print "mhtVal:htVal>>zinv_%s_hhtmht2D_nj%d"%("zinv400",cut[1])
            print "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                      0.9*histoInfo.mcSamples["zinv400"]["scalef"],
                                                      1.1*histoInfo.mcSamples["zinv400"]["scalef"])
        zinvChain.Draw("mhtVal:htVal>>zinv_%s_hhtmht2D_nj%d"%("zinv400",cut[1]),
                       "%s&&%s&&(eventWt>%f&&eventWt<%f)"%(cuts,cut[0],
                                                           0.9*histoInfo.mcSamples["zinv400"]["scalef"],
                                                           1.1*histoInfo.mcSamples["zinv400"]["scalef"]),"colz")
        if options.debug:
            print "zinv400 histogram has %d entries"%(zinv400Inputs[j].GetEntries())
        zinv200Inputs[    j].GetEntries()
        zinv400Inputs[    j].GetEntries()
        zinv200Inputs[    j].Write()
        zinv400Inputs[    j].Write()
    ###
    if options.debug:
        print zmumuDATAInputFile
        print zmumu200MCInputFile
        print zmumu400MCInputFile
        print zmumuBkgdInputFile


    histoNames = [
        #["hhtmht2D_nj0","N_{Jets}#geq 2"],#[2,)
        ["hhtmht2D_nj1","N_{Jets} = 2"],#2
        ["hhtmht2D_nj2","N_{Jets} = 3"],#3
        ["hhtmht2D_nj3","N_{Jets} = 4"],#4
        ["hhtmht2D_nj4","N_{Jets} = 5"],#5
        ["hhtmht2D_nj5","N_{Jets} = 6"],#6
        ["hhtmht2D_nj6","N_{Jets} = 7"],#7
        ["hhtmht2D_nj7","N_{Jets}#geq 8"],#[8,)
        #["hhtmht2D_nj8","3#leq N_{Jets}#leq 5"],#[3,5]
        #["hhtmht2D_nj9","6#leq N_{Jets}#leq 7"],#[6,7]
        ]
    ##MHT bins
    #(The HT bins are nbins= 25, low=0, high=2500; the MHT bins are nbins=20, low=0, high=1000)

    mhtBins = [[100,199,"100to200"],
               [200,299,"200to300"],
               [300,449,"300to450"],
               [100,10000,"100toInf"],
               [200,10000,"200toInf"],
               [450,10000,"450toInf"]]

    photonDataSF    = 1
    photonSFht200   = 19.4/10*histoInfo.mcSamples["gjets200"]["scaleflo"]
    photonSFht400   = 19.4/10*histoInfo.mcSamples["gjets400"]["scaleflo"]
    ## values used here are for bkgd subtraction, question is whether to use
    ## same order as gjets or to use best known value
    ## conclusion was to use best known value
    photonSFqcd250  = 19.4/10*histoInfo.mcSamples["qcd250"  ]["scalef"]
    photonSFqcd500  = 19.4/10*histoInfo.mcSamples["qcd500"  ]["scalef"]
    photonSFqcd1000 = 19.4/10*histoInfo.mcSamples["qcd1000" ]["scalef"]
    photonSFttbar   = 19.4/10*histoInfo.mcSamples["ttjets"  ]["scalef"]
    photonSFwjets   = 19.4/10*histoInfo.mcSamples["wjets"   ]["scalef"]

    zmumuDataSF  = 19.4/18.2
    zmumuSFht200 = 19.73*19.4*1000/6368770.
    zmumuSFht400 = 2.826*19.4*1000/2347781.
    ## values used here are for bkgd subtraction, question is whether to use
    ## same order as gjets or to use best known value
    ## conclusion was to use best known value
    #zmumuSFttbar =  53.2*19.4*1000/5000000.
    zmumuSFttbar =   234*19.4*1000/5000000.
    
    if options.useNNLO:
        zmumuSFht200 = 25.54*19.4*1000/6368770.
        zmumuSFht400 =  3.36*19.4*1000/2347781.
        #zmumuSFttbar =   234*19.4*1000/5000000.

    ## values used here are for performing the ratio, question is whether to use
    ## same order as gjets or to use best known value, same question for the zmumu
    zinvSFht200   = 19.4/10*histoInfo.mcSamples["zinv200"][sfSource]
    zinvSFht400   = 19.4/10*histoInfo.mcSamples["zinv400"][sfSource]

    zmumuDataNJets  = []
    zmumu200NJets   = []
    zmumu400NJets   = []
    zmumuMCNJets    = []
    zmumuTotNJets   = []
    zmumuTTBarNJets = []

    zmumuDataInputs  = []
    zmumu200Inputs   = []
    zmumu400Inputs   = []
    zmumuTTBarInputs = []
    for h,hist in enumerate(histoNames): 
        zmumuDataInputs .append(zmumuDATAInputFile .Get(hist[0]).Clone("zmumu_data_%s"%(  hist[0])))
        zmumu200Inputs  .append(zmumu200MCInputFile.Get(hist[0]).Clone("zmumu_ht200_%s"%( hist[0])))
        zmumu400Inputs  .append(zmumu400MCInputFile.Get(hist[0]).Clone("zmumu_ht400_%s"%( hist[0])))
        zmumuTTBarInputs.append(zmumuBkgdInputFile .Get(hist[0]).Clone("zmumu_ttjets_%s"%(hist[0])))

        zmumuDataInputs[h] .Sumw2()
        zmumu200Inputs[h]  .Sumw2()
        zmumu400Inputs[h]  .Sumw2()
        zmumuTTBarInputs[h].Sumw2()

        outputFile.cd()
        zmumuDataInputs[h] .Write()
        zmumu200Inputs[h]  .Write()
        zmumu400Inputs[h]  .Write()
        zmumuTTBarInputs[h].Write()


    ####HT
    gjetsDataHT    = []
    gjets200HT     = []
    gjets400HT     = []
    gjetsQCD250HT  = []
    gjetsQCD500HT  = []
    gjetsQCD1000HT = []
    gjetsTTBarHT   = []
    gjetsWJetsHT   = []
    gjetsMCHT      = []
    gjetsQCDHT      = []
    gjetsTotHT      = []
    
    zmumuDataHT  = []
    zmumu200HT   = []
    zmumu400HT   = []
    zmumuTTBarHT = []
    zmumuMCHT      = []
    zmumuTotHT      = []
    
    zinv200HT = []
    zinv400HT = []
    zinvMCHT      = []

    ####MHT
    gjetsDataMHT    = []
    gjets200MHT     = []
    gjets400MHT     = []
    gjetsQCD250MHT  = []
    gjetsQCD500MHT  = []
    gjetsQCD1000MHT = []
    gjetsTTBarMHT   = []
    gjetsWJetsMHT   = []
    gjetsMCMHT      = []
    gjetsQCDMHT      = []
    gjetsTotMHT      = []
    
    zmumuDataMHT  = []
    zmumu200MHT   = []
    zmumu400MHT   = []
    zmumuTTBarMHT = []
    zmumuMCMHT      = []
    zmumuTotMHT      = []
    
    zinv200MHT = []
    zinv400MHT = []
    zinvMCMHT      = []


    for j,cut in enumerate(jetCuts):
        gjetsDataHT   .append( gjetsDataInputs[j]   .ProjectionX("gjetsDataHT_nj%d"%(cut[1])   ))
        gjets200HT    .append( gjets200Inputs[j]    .ProjectionX("gjets200HT_nj%d"%(cut[1])    ))
        gjets400HT    .append( gjets400Inputs[j]    .ProjectionX("gjets400HT_nj%d"%(cut[1])    ))
        gjetsQCD250HT .append( gjetsQCD250Inputs[j] .ProjectionX("gjetsQCD250HT_nj%d"%(cut[1]) ))
        gjetsQCD500HT .append( gjetsQCD500Inputs[j] .ProjectionX("gjetsQCD500HT_nj%d"%(cut[1]) ))
        gjetsQCD1000HT.append( gjetsQCD1000Inputs[j].ProjectionX("gjetsQCD1000HT_nj%d"%(cut[1])))
        gjetsTTBarHT  .append( gjetsTTBarInputs[j]  .ProjectionX("gjetsTTBarHT_nj%d"%(cut[1])  ))
        gjetsWJetsHT  .append( gjetsWJetsInputs[j]  .ProjectionX("gjetsWJetsHT_nj%d"%(cut[1])  ))
        
        zmumuDataHT .append( zmumuDataInputs[j] .ProjectionX("zmumuDataHT_nj%d"%(cut[1]) ))
        zmumu200HT  .append( zmumu200Inputs[j]  .ProjectionX("zmumu200HT_nj%d"%(cut[1])  ))
        zmumu400HT  .append( zmumu400Inputs[j]  .ProjectionX("zmumu400HT_nj%d"%(cut[1])  ))
        zmumuTTBarHT.append( zmumuTTBarInputs[j].ProjectionX("zmumuTTBarHT_nj%d"%(cut[1])))
        
        zinv200HT.append(     zinv200Inputs[j].ProjectionX("zinv200HT_nj%d"%(cut[1])))
        zinv400HT.append(     zinv400Inputs[j].ProjectionX("zinv400HT_nj%d"%(cut[1])))

        gjetsDataHT[j]   .Scale(photonDataSF)
        gjets200HT[j]    .Scale(photonSFht200)
        gjets400HT[j]    .Scale(photonSFht400)
        gjetsQCD250HT[j] .Scale(photonSFqcd250)
        gjetsQCD500HT[j] .Scale(photonSFqcd500)
        gjetsQCD1000HT[j].Scale(photonSFqcd1000)
        gjetsTTBarHT[j]  .Scale(photonSFttbar)
        gjetsWJetsHT[j]  .Scale(photonSFwjets)

        gjetsMCHT   .append(gjets400HT[j].Clone("photons_signalTotal_HT_%s"%(cut[1])))
        gjetsMCHT[j].Add(gjets200HT[j])

        gjetsQCDHT   .append(gjetsQCD250HT[j].Clone("photons_qcdTotal_HT_%s"%(cut[1])))
        gjetsQCDHT[j].Add(gjetsQCD500HT[j])
        gjetsQCDHT[j].Add(gjetsQCD1000HT[j])

        gjetsTotHT   .append(gjetsMCHT[j].Clone("photons_mcTotal_HT_%s"%(cut[1])))
        gjetsTotHT[j].Add(gjetsQCDHT[j])
        gjetsTotHT[j].Add(gjetsTTBarHT[j])
        gjetsTotHT[j].Add(gjetsWJetsHT[j])

        gjetsDataHT[j]   .SetMarkerColor(r.kBlack)
        gjets200HT[j]    .SetMarkerColor(r.kOrange+10)
        gjets400HT[j]    .SetMarkerColor(r.kOrange+2)
        gjetsMCHT[j]     .SetMarkerColor(r.kOrange)
        gjetsQCD250HT[j] .SetMarkerColor(r.kRed+1)
        gjetsQCD500HT[j] .SetMarkerColor(r.kRed+2)
        gjetsQCD1000HT[j].SetMarkerColor(r.kRed+3)
        gjetsQCDHT[j]    .SetMarkerColor(r.kRed)
        gjetsTTBarHT[j]  .SetMarkerColor(r.kCyan+2)
        gjetsWJetsHT[j]  .SetMarkerColor(r.kGreen+3)
        gjetsTotHT[j]    .SetMarkerColor(r.kViolet)

        gjetsDataHT[j]   .SetLineColor(r.kBlack)
        gjets200HT[j]    .SetLineColor(r.kOrange+10)
        gjets400HT[j]    .SetLineColor(r.kOrange+2)
        gjetsMCHT[j]     .SetLineColor(r.kOrange)
        gjetsQCD250HT[j] .SetLineColor(r.kRed+1)
        gjetsQCD500HT[j] .SetLineColor(r.kRed+2)
        gjetsQCD1000HT[j].SetLineColor(r.kRed+3)
        gjetsQCDHT[j]    .SetLineColor(r.kRed)
        gjetsTTBarHT[j]  .SetLineColor(r.kCyan+2)
        gjetsWJetsHT[j]  .SetLineColor(r.kGreen+3)
        gjetsTotHT[j]    .SetLineColor(r.kViolet)

        gjetsDataHT[j]   .SetLineWidth(2)
        gjets200HT[j]    .SetLineWidth(2)
        gjets400HT[j]    .SetLineWidth(2)
        gjetsMCHT[j]     .SetLineWidth(2)
        gjetsQCD250HT[j] .SetLineWidth(2)
        gjetsQCD500HT[j] .SetLineWidth(2)
        gjetsQCD1000HT[j].SetLineWidth(2)
        gjetsQCDHT[j]    .SetLineWidth(2)
        gjetsTTBarHT[j]  .SetLineWidth(2)
        gjetsWJetsHT[j]  .SetLineWidth(2)
        gjetsTotHT[j]    .SetLineWidth(2)

        gjetsDataHTtmp    = gjetsDataHT[j]   .Rebin(len(htHistBins)-1,gjetsDataHT[j]   .GetName()+"_rebinned",array('d',htHistBins))
        gjets200HTtmp     = gjets200HT[j]    .Rebin(len(htHistBins)-1,gjets200HT[j]    .GetName()+"_rebinned",array('d',htHistBins))
        gjets400HTtmp     = gjets400HT[j]    .Rebin(len(htHistBins)-1,gjets400HT[j]    .GetName()+"_rebinned",array('d',htHistBins))
        gjetsQCD250HTtmp  = gjetsQCD250HT[j] .Rebin(len(htHistBins)-1,gjetsQCD250HT[j] .GetName()+"_rebinned",array('d',htHistBins))
        gjetsQCD500HTtmp  = gjetsQCD500HT[j] .Rebin(len(htHistBins)-1,gjetsQCD500HT[j] .GetName()+"_rebinned",array('d',htHistBins))
        gjetsQCD1000HTtmp = gjetsQCD1000HT[j].Rebin(len(htHistBins)-1,gjetsQCD1000HT[j].GetName()+"_rebinned",array('d',htHistBins))
        gjetsTTBarHTtmp   = gjetsTTBarHT[j]  .Rebin(len(htHistBins)-1,gjetsTTBarHT[j]  .GetName()+"_rebinned",array('d',htHistBins))
        gjetsWJetsHTtmp   = gjetsWJetsHT[j]  .Rebin(len(htHistBins)-1,gjetsWJetsHT[j]  .GetName()+"_rebinned",array('d',htHistBins))
        gjetsMCHTtmp      = gjetsMCHT[j]     .Rebin(len(htHistBins)-1,gjetsMCHT[j]     .GetName()+"_rebinned",array('d',htHistBins))
        gjetsQCDHTtmp     = gjetsQCDHT[j]    .Rebin(len(htHistBins)-1,gjetsQCDHT[j]    .GetName()+"_rebinned",array('d',htHistBins))
        gjetsTotHTtmp     = gjetsTotHT[j]    .Rebin(len(htHistBins)-1,gjetsTotHT[j]    .GetName()+"_rebinned",array('d',htHistBins))

        gjetsDataHTtmp   .Write()
        gjets200HTtmp    .Write()
        gjets400HTtmp    .Write()
        gjetsQCD250HTtmp .Write()
        gjetsQCD500HTtmp .Write()
        gjetsQCD1000HTtmp.Write()
        gjetsTTBarHTtmp  .Write()
        gjetsWJetsHTtmp  .Write()
        gjetsMCHTtmp     .Write()
        gjetsQCDHTtmp    .Write()
        gjetsTotHTtmp    .Write()
        #gjetsDataHT[j]   .Write()
        #gjets200HT[j]    .Write()
        #gjets400HT[j]    .Write()
        #gjetsQCD250HT[j] .Write()
        #gjetsQCD500HT[j] .Write()
        #gjetsQCD1000HT[j].Write()
        #gjetsTTBarHT[j]  .Write()
        #gjetsWJetsHT[j]  .Write()
        #gjetsMCHT[j]     .Write()
        #gjetsQCDHT[j]    .Write()
        #gjetsTotHT[j]    .Write()
        ####
        zmumuDataHT[j] .Scale(zmumuDataSF)
        zmumu200HT[j]  .Scale(zmumuSFht200)
        zmumu400HT[j]  .Scale(zmumuSFht400)
        zmumuTTBarHT[j].Scale(zmumuSFttbar)

        zmumuMCHT   .append(zmumu400HT[j].Clone("zmumu_signalTotal_HT_%s"%(cut[1])))
        zmumuMCHT[j].Add(zmumu200HT[j])

        zmumuTotHT   .append(zmumu400HT[j].Clone("zmumu_mcTotal_HT_%s"%(cut[1])))
        zmumuTotHT[j].Add(zmumu200HT[j])
        zmumuTotHT[j].Add(zmumuTTBarHT[j])

        zmumuDataHT[j] .SetMarkerColor(r.kBlack)
        zmumu200HT[j]  .SetMarkerColor(r.kMagenta+1)
        zmumu400HT[j]  .SetMarkerColor(r.kMagenta+2)
        zmumuMCHT[j]   .SetMarkerColor(r.kMagenta+3)
        zmumuTTBarHT[j].SetMarkerColor(r.kCyan+2)
        zmumuTotHT[j]  .SetMarkerColor(r.kViolet)

        zmumuDataHT[j] .SetLineColor(r.kBlack)
        zmumu200HT[j]  .SetLineColor(r.kMagenta+1)
        zmumu400HT[j]  .SetLineColor(r.kMagenta+2)
        zmumuMCHT[j]   .SetLineColor(r.kMagenta+3)
        zmumuTTBarHT[j].SetLineColor(r.kCyan+2)
        zmumuTotHT[j]  .SetLineColor(r.kViolet)

        zmumuDataHT[j] .SetLineWidth(2)
        zmumu200HT[j]  .SetLineWidth(2)
        zmumu400HT[j]  .SetLineWidth(2)
        zmumuTTBarHT[j].SetLineWidth(2)
        zmumuMCHT[j]   .SetLineWidth(2)
        zmumuTotHT[j]  .SetLineWidth(2)

        zmumuDataHTtmp  = zmumuDataHT[j] .Rebin(len(htHistBins)-1,zmumuDataHT[j] .GetName()+"_rebinned",array('d',htHistBins))
        zmumu200HTtmp   = zmumu200HT[j]  .Rebin(len(htHistBins)-1,zmumu200HT[j]  .GetName()+"_rebinned",array('d',htHistBins))
        zmumu400HTtmp   = zmumu400HT[j]  .Rebin(len(htHistBins)-1,zmumu400HT[j]  .GetName()+"_rebinned",array('d',htHistBins))
        zmumuTTBarHTtmp = zmumuTTBarHT[j].Rebin(len(htHistBins)-1,zmumuTTBarHT[j].GetName()+"_rebinned",array('d',htHistBins))
        zmumuMCHTtmp    = zmumuMCHT[j]   .Rebin(len(htHistBins)-1,zmumuMCHT[j]   .GetName()+"_rebinned",array('d',htHistBins))
        zmumuTotHTtmp   = zmumuTotHT[j]  .Rebin(len(htHistBins)-1,zmumuTotHT[j]  .GetName()+"_rebinned",array('d',htHistBins))

        zmumuDataHTtmp .Write()
        zmumu200HTtmp  .Write()
        zmumu400HTtmp  .Write()
        zmumuTTBarHTtmp.Write()
        zmumuMCHTtmp   .Write()
        zmumuTotHTtmp  .Write()
        #zmumuDataHT[j] .Write()
        #zmumu200HT[j]  .Write()
        #zmumu400HT[j]  .Write()
        #zmumuTTBarHT[j].Write()
        #zmumuMCHT[j]   .Write()
        #zmumuTotHT[j]  .Write()

        ###Z Invisible###
        zinv200HT[    j].Scale(zinvSFht200)
        zinv400HT[    j].Scale(zinvSFht400)
        #
        zinvMCHT.append(zinv400HT[j].Clone("zinv_signalTotal_HT_%s"%(cut[1])))
        zinvMCHT[j].Add(zinv200HT[j])
        zinv200HT[    j].SetMarkerColor(r.kAzure+1)
        zinv400HT[    j].SetMarkerColor(r.kAzure+2)
        zinvMCHT[     j].SetMarkerColor(r.kAzure+3)
        zinv200HT[  j].SetLineColor(r.kAzure+1)
        zinv400HT[  j].SetLineColor(r.kAzure+2)
        zinvMCHT[   j].SetLineColor(r.kAzure+3)
        zinv200HT[    j].SetLineWidth(2)
        zinv400HT[    j].SetLineWidth(2)
        zinvMCHT[     j].SetLineWidth(2)

        zinv200HTtmp = zinv200HT[j].Rebin(len(htHistBins)-1,zinv200HT[j].GetName()+"_rebinned",array('d',htHistBins))
        zinv400HTtmp = zinv400HT[j].Rebin(len(htHistBins)-1,zinv400HT[j].GetName()+"_rebinned",array('d',htHistBins))
        zinvMCHTtmp  = zinvMCHT[j] .Rebin(len(htHistBins)-1,zinvMCHT[j] .GetName()+"_rebinned",array('d',htHistBins))

        zinv200HTtmp.Write()
        zinv400HTtmp.Write()
        zinvMCHTtmp .Write()
        #zinv200HT[j].Write()
        #zinv400HT[j].Write()
        #zinvMCHT[j] .Write()
        
        ### MHT
        gjetsDataMHT   .append( gjetsDataInputs[j]   .ProjectionY("gjetsDataMHT_nj%d"%(cut[1])   ))
        gjets200MHT    .append( gjets200Inputs[j]    .ProjectionY("gjets200MHT_nj%d"%(cut[1])    ))
        gjets400MHT    .append( gjets400Inputs[j]    .ProjectionY("gjets400MHT_nj%d"%(cut[1])    ))
        gjetsQCD250MHT .append( gjetsQCD250Inputs[j] .ProjectionY("gjetsQCD250MHT_nj%d"%(cut[1]) ))
        gjetsQCD500MHT .append( gjetsQCD500Inputs[j] .ProjectionY("gjetsQCD500MHT_nj%d"%(cut[1]) ))
        gjetsQCD1000MHT.append( gjetsQCD1000Inputs[j].ProjectionY("gjetsQCD1000MHT_nj%d"%(cut[1])))
        gjetsTTBarMHT  .append( gjetsTTBarInputs[j]  .ProjectionY("gjetsTTBarMHT_nj%d"%(cut[1])  ))
        gjetsWJetsMHT  .append( gjetsWJetsInputs[j]  .ProjectionY("gjetsWJetsMHT_nj%d"%(cut[1])  ))

        zmumuDataMHT .append( zmumuDataInputs[j] .ProjectionY("zmumuDataMHT_nj%d"%(cut[1]) ))
        zmumu200MHT  .append( zmumu200Inputs[j]  .ProjectionY("zmumu200MHT_nj%d"%(cut[1])  ))
        zmumu400MHT  .append( zmumu400Inputs[j]  .ProjectionY("zmumu400MHT_nj%d"%(cut[1])  ))
        zmumuTTBarMHT.append( zmumuTTBarInputs[j].ProjectionY("zmumuTTBarMHT_nj%d"%(cut[1])))
        
        zinv200MHT.append(     zinv400Inputs[j].ProjectionY("zinv200MHT_nj%d"%(cut[1])))
        zinv400MHT.append(     zinv400Inputs[j].ProjectionY("zinv400MHT_nj%d"%(cut[1])))
        
        gjetsDataMHT[j]   .Scale(photonDataSF)
        gjets200MHT[j]    .Scale(photonSFht200)
        gjets400MHT[j]    .Scale(photonSFht400)
        gjetsQCD250MHT[j] .Scale(photonSFqcd250)
        gjetsQCD500MHT[j] .Scale(photonSFqcd500)
        gjetsQCD1000MHT[j].Scale(photonSFqcd1000)
        gjetsTTBarMHT[j]  .Scale(photonSFttbar)
        gjetsWJetsMHT[j]  .Scale(photonSFwjets)

        gjetsMCMHT   .append(gjets400MHT[j].Clone("photons_signalTotal_MHT_%s"%(cut[1])))
        gjetsMCMHT[j].Add(gjets200MHT[j])

        gjetsQCDMHT   .append(gjetsQCD250MHT[j].Clone("photons_qcdTotal_MHT_%s"%(cut[1])))
        gjetsQCDMHT[j].Add(gjetsQCD500MHT[j])
        gjetsQCDMHT[j].Add(gjetsQCD1000MHT[j])

        gjetsTotMHT   .append(gjetsMCMHT[j].Clone("photons_mcTotal_MHT_%s"%(cut[1])))
        gjetsTotMHT[j].Add(gjetsQCDMHT[j])
        gjetsTotMHT[j].Add(gjetsTTBarMHT[j])
        gjetsTotMHT[j].Add(gjetsWJetsMHT[j])

        gjetsDataMHT[j]   .SetMarkerColor(r.kBlack)
        gjets200MHT[j]    .SetMarkerColor(r.kOrange+10)
        gjets400MHT[j]    .SetMarkerColor(r.kOrange+2)
        gjetsMCMHT[j]     .SetMarkerColor(r.kOrange)
        gjetsQCD250MHT[j] .SetMarkerColor(r.kRed+1)
        gjetsQCD500MHT[j] .SetMarkerColor(r.kRed+2)
        gjetsQCD1000MHT[j].SetMarkerColor(r.kRed+3)
        gjetsQCDMHT[j]    .SetMarkerColor(r.kRed)
        gjetsTTBarMHT[j]  .SetMarkerColor(r.kCyan+2)
        gjetsWJetsMHT[j]  .SetMarkerColor(r.kGreen+3)
        gjetsTotMHT[j]    .SetMarkerColor(r.kViolet)

        gjetsDataMHT[j]   .SetLineColor(r.kBlack)
        gjets200MHT[j]    .SetLineColor(r.kOrange+10)
        gjets400MHT[j]    .SetLineColor(r.kOrange+2)
        gjetsMCMHT[j]     .SetLineColor(r.kOrange)
        gjetsQCD250MHT[j] .SetLineColor(r.kRed+1)
        gjetsQCD500MHT[j] .SetLineColor(r.kRed+2)
        gjetsQCD1000MHT[j].SetLineColor(r.kRed+3)
        gjetsQCDMHT[j]    .SetLineColor(r.kRed)
        gjetsTTBarMHT[j]  .SetLineColor(r.kCyan+2)
        gjetsWJetsMHT[j]  .SetLineColor(r.kGreen+3)
        gjetsTotMHT[j]    .SetLineColor(r.kViolet)

        gjetsDataMHT[j]   .SetLineWidth(2)
        gjets200MHT[j]    .SetLineWidth(2)
        gjets400MHT[j]    .SetLineWidth(2)
        gjetsMCMHT[j]     .SetLineWidth(2)
        gjetsQCD250MHT[j] .SetLineWidth(2)
        gjetsQCD500MHT[j] .SetLineWidth(2)
        gjetsQCD1000MHT[j].SetLineWidth(2)
        gjetsQCDMHT[j]    .SetLineWidth(2)
        gjetsTTBarMHT[j]  .SetLineWidth(2)
        gjetsWJetsMHT[j]  .SetLineWidth(2)
        gjetsTotMHT[j]    .SetLineWidth(2)

        gjetsDataMHTtmp    = gjetsDataMHT[j]   .Rebin(len(mhtHistBins)-1,gjetsDataMHT[j]   .GetName()+"_rebinned",array('d',mhtHistBins))
        gjets200MHTtmp     = gjets200MHT[j]    .Rebin(len(mhtHistBins)-1,gjets200MHT[j]    .GetName()+"_rebinned",array('d',mhtHistBins))
        gjets400MHTtmp     = gjets400MHT[j]    .Rebin(len(mhtHistBins)-1,gjets400MHT[j]    .GetName()+"_rebinned",array('d',mhtHistBins))
        gjetsQCD250MHTtmp  = gjetsQCD250MHT[j] .Rebin(len(mhtHistBins)-1,gjetsQCD250MHT[j] .GetName()+"_rebinned",array('d',mhtHistBins))
        gjetsQCD500MHTtmp  = gjetsQCD500MHT[j] .Rebin(len(mhtHistBins)-1,gjetsQCD500MHT[j] .GetName()+"_rebinned",array('d',mhtHistBins))
        gjetsQCD1000MHTtmp = gjetsQCD1000MHT[j].Rebin(len(mhtHistBins)-1,gjetsQCD1000MHT[j].GetName()+"_rebinned",array('d',mhtHistBins))
        gjetsTTBarMHTtmp   = gjetsTTBarMHT[j]  .Rebin(len(mhtHistBins)-1,gjetsTTBarMHT[j]  .GetName()+"_rebinned",array('d',mhtHistBins))
        gjetsWJetsMHTtmp   = gjetsWJetsMHT[j]  .Rebin(len(mhtHistBins)-1,gjetsWJetsMHT[j]  .GetName()+"_rebinned",array('d',mhtHistBins))
        gjetsMCMHTtmp      = gjetsMCMHT[j]     .Rebin(len(mhtHistBins)-1,gjetsMCMHT[j]     .GetName()+"_rebinned",array('d',mhtHistBins))
        gjetsQCDMHTtmp     = gjetsQCDMHT[j]    .Rebin(len(mhtHistBins)-1,gjetsQCDMHT[j]    .GetName()+"_rebinned",array('d',mhtHistBins))
        gjetsTotMHTtmp     = gjetsTotMHT[j]    .Rebin(len(mhtHistBins)-1,gjetsTotMHT[j]    .GetName()+"_rebinned",array('d',mhtHistBins))

        gjetsDataMHTtmp   .Write()
        gjets200MHTtmp    .Write()
        gjets400MHTtmp    .Write()
        gjetsQCD250MHTtmp .Write()
        gjetsQCD500MHTtmp .Write()
        gjetsQCD1000MHTtmp.Write()
        gjetsTTBarMHTtmp  .Write()
        gjetsWJetsMHTtmp  .Write()
        gjetsMCMHTtmp     .Write()
        gjetsQCDMHTtmp    .Write()
        gjetsTotMHTtmp    .Write()
        ##gjetsDataMHT[j]   .Write()
        ##gjets200MHT[j]    .Write()
        ##gjets400MHT[j]    .Write()
        ##gjetsQCD250MHT[j] .Write()
        ##gjetsQCD500MHT[j] .Write()
        ##gjetsQCD1000MHT[j].Write()
        ##gjetsTTBarMHT[j]  .Write()
        ##gjetsWJetsMHT[j]  .Write()
        ##gjetsMCMHT[j]     .Write()
        ##gjetsQCDMHT[j]    .Write()
        ##gjetsTotMHT[j]    .Write()
        ####
        zmumuDataMHT[j] .Scale(zmumuDataSF)
        zmumu200MHT[j]  .Scale(zmumuSFht200)
        zmumu400MHT[j]  .Scale(zmumuSFht400)
        zmumuTTBarMHT[j].Scale(zmumuSFttbar)

        zmumuMCMHT   .append(zmumu400MHT[j].Clone("zmumu_signalTotal_MHT_%s"%(cut[1])))
        zmumuMCMHT[j].Add(zmumu200MHT[j])

        zmumuTotMHT   .append(zmumu400MHT[j].Clone("zmumu_mcTotal_MHT_%s"%(cut[1])))
        zmumuTotMHT[j].Add(zmumu200MHT[j])
        zmumuTotMHT[j].Add(zmumuTTBarMHT[j])

        zmumuDataMHT[j] .SetMarkerColor(r.kBlack)
        zmumu200MHT[j]  .SetMarkerColor(r.kMagenta+1)
        zmumu400MHT[j]  .SetMarkerColor(r.kMagenta+2)
        zmumuMCMHT[j]   .SetMarkerColor(r.kMagenta+3)
        zmumuTTBarMHT[j].SetMarkerColor(r.kCyan+2)
        zmumuTotMHT[j]  .SetMarkerColor(r.kViolet)

        zmumuDataMHT[j] .SetLineColor(r.kBlack)
        zmumu200MHT[j]  .SetLineColor(r.kMagenta+1)
        zmumu400MHT[j]  .SetLineColor(r.kMagenta+2)
        zmumuMCMHT[j]   .SetLineColor(r.kMagenta+3)
        zmumuTTBarMHT[j].SetLineColor(r.kCyan+2)
        zmumuTotMHT[j]  .SetLineColor(r.kViolet)

        zmumuDataMHT[j] .SetLineWidth(2)
        zmumu200MHT[j]  .SetLineWidth(2)
        zmumu400MHT[j]  .SetLineWidth(2)
        zmumuTTBarMHT[j].SetLineWidth(2)
        zmumuMCMHT[j]   .SetLineWidth(2)
        zmumuTotMHT[j]  .SetLineWidth(2)

        zmumuDataMHTtmp  = zmumuDataMHT[j] .Rebin(len(mhtHistBins)-1,zmumuDataMHT[j] .GetName()+"_rebinned",array('d',mhtHistBins))
        zmumu200MHTtmp   = zmumu200MHT[j]  .Rebin(len(mhtHistBins)-1,zmumu200MHT[j]  .GetName()+"_rebinned",array('d',mhtHistBins))
        zmumu400MHTtmp   = zmumu400MHT[j]  .Rebin(len(mhtHistBins)-1,zmumu400MHT[j]  .GetName()+"_rebinned",array('d',mhtHistBins))
        zmumuTTBarMHTtmp = zmumuTTBarMHT[j].Rebin(len(mhtHistBins)-1,zmumuTTBarMHT[j].GetName()+"_rebinned",array('d',mhtHistBins))
        zmumuMCMHTtmp    = zmumuMCMHT[j]   .Rebin(len(mhtHistBins)-1,zmumuMCMHT[j]   .GetName()+"_rebinned",array('d',mhtHistBins))
        zmumuTotMHTtmp   = zmumuTotMHT[j]  .Rebin(len(mhtHistBins)-1,zmumuTotMHT[j]  .GetName()+"_rebinned",array('d',mhtHistBins))

        zmumuDataMHTtmp .Write()
        zmumu200MHTtmp  .Write()
        zmumu400MHTtmp  .Write()
        zmumuTTBarMHTtmp.Write()
        zmumuMCMHTtmp   .Write()
        zmumuTotMHTtmp  .Write()
        #zmumuDataMHT[j] .Write()
        #zmumu200MHT[j]  .Write()
        #zmumu400MHT[j]  .Write()
        #zmumuTTBarMHT[j].Write()
        #zmumuMCMHT[j]   .Write()
        #zmumuTotMHT[j]  .Write()

        ###Z Invisible###
        zinv200MHT[    j].Scale(zinvSFht200)
        zinv400MHT[    j].Scale(zinvSFht400)
        #
        zinvMCMHT.append(zinv400MHT[j].Clone("zinv_signalTotal_MHT_%s"%(cut[1])))
        zinvMCMHT[j].Add(zinv200MHT[j])
        zinv200MHT[j].SetMarkerColor(r.kAzure+1)
        zinv400MHT[j].SetMarkerColor(r.kAzure+2)
        zinvMCMHT[ j].SetMarkerColor(r.kAzure+3)
        zinv200MHT[j].SetLineColor(r.kAzure+1)
        zinv400MHT[j].SetLineColor(r.kAzure+2)
        zinvMCMHT[ j].SetLineColor(r.kAzure+3)
        zinv200MHT[j].SetLineWidth(2)
        zinv400MHT[j].SetLineWidth(2)
        zinvMCMHT[ j].SetLineWidth(2)

        zinv200MHTtmp = zinv200MHT[j].Rebin(len(mhtHistBins)-1,zinv200MHT[j].GetName()+"_rebinned",array('d',mhtHistBins))
        zinv400MHTtmp = zinv400MHT[j].Rebin(len(mhtHistBins)-1,zinv400MHT[j].GetName()+"_rebinned",array('d',mhtHistBins))
        zinvMCMHTtmp  = zinvMCMHT[ j].Rebin(len(mhtHistBins)-1,zinvMCMHT[ j].GetName()+"_rebinned",array('d',mhtHistBins))
        
        zinv200MHTtmp.Write()
        zinv400MHTtmp.Write()
        zinvMCMHTtmp .Write()
        #zinv200MHT[j].Write()
        #zinv400MHT[j].Write()
        #zinvMCMHT[ j].Write()
    

    for m,mbin in enumerate(mhtBins):
        gjetsDataNJets   .append(r.TH1D("gjetsDataNJets_%s"%(mbin[2])   ,"gjetsDataNJets_%s"%(mbin[2])   ,9,-0.5,8.5))
        gjets200NJets    .append(r.TH1D("gjets200NJets_%s"%(mbin[2])    ,"gjets200NJets_%s"%(mbin[2])    ,9,-0.5,8.5))
        gjets400NJets    .append(r.TH1D("gjets400NJets_%s"%(mbin[2])    ,"gjets400NJets_%s"%(mbin[2])    ,9,-0.5,8.5))
        gjetsQCD250NJets .append(r.TH1D("gjetsQCD250NJets_%s"%(mbin[2]) ,"gjetsQCD250NJets_%s"%(mbin[2]) ,9,-0.5,8.5))
        gjetsQCD500NJets .append(r.TH1D("gjetsQCD500NJets_%s"%(mbin[2]) ,"gjetsQCD500NJets_%s"%(mbin[2]) ,9,-0.5,8.5))
        gjetsQCD1000NJets.append(r.TH1D("gjetsQCD1000NJets_%s"%(mbin[2]),"gjetsQCD1000NJets_%s"%(mbin[2]),9,-0.5,8.5))
        gjetsTTBarNJets  .append(r.TH1D("gjetsTTBarNJets_%s"%(mbin[2])  ,"gjetsTTBarNJets_%s"%(mbin[2])  ,9,-0.5,8.5))
        gjetsWJetsNJets  .append(r.TH1D("gjetsWJetsNJets_%s"%(mbin[2])  ,"gjetsWJetsNJets_%s"%(mbin[2])  ,9,-0.5,8.5))
        gjetsDataNJets[m]   .Sumw2()
        gjets200NJets[m]    .Sumw2()
        gjets400NJets[m]    .Sumw2()
        gjetsQCD250NJets[m] .Sumw2()
        gjetsQCD500NJets[m] .Sumw2()
        gjetsQCD1000NJets[m].Sumw2()
        gjetsTTBarNJets[m]  .Sumw2()
        gjetsWJetsNJets[m]  .Sumw2()


        zmumuDataNJets .append(r.TH1D("zmumuDataNJets_%s"%(mbin[2]) ,"zmumuDataNJets_%s"%(mbin[2]) ,9,-0.5,8.5))
        zmumu200NJets  .append(r.TH1D("zmumu200NJets_%s"%(mbin[2])  ,"zmumu200NJets_%s"%(mbin[2])  ,9,-0.5,8.5))
        zmumu400NJets  .append(r.TH1D("zmumu400NJets_%s"%(mbin[2])  ,"zmumu400NJets_%s"%(mbin[2])  ,9,-0.5,8.5))
        zmumuTTBarNJets.append(r.TH1D("zmumuTTBarNJets_%s"%(mbin[2]),"zmumuTTBarNJets_%s"%(mbin[2]),9,-0.5,8.5))
        zmumuDataNJets[m] .Sumw2()
        zmumu200NJets[m]  .Sumw2()
        zmumu400NJets[m]  .Sumw2()
        zmumuTTBarNJets[m].Sumw2()


        zinv200NJets.append(    r.TH1D("zinv200NJets_%s"%(mbin[2])    ,"zinv200NJets_%s"%(mbin[2])    ,9,-0.5,8.5))
        zinv400NJets.append(    r.TH1D("zinv400NJets_%s"%(mbin[2])    ,"zinv400NJets_%s"%(mbin[2])    ,9,-0.5,8.5))
        zinv200NJets[    m].Sumw2()
        zinv400NJets[    m].Sumw2()

        for h,hist in enumerate(histoNames):
            ##gjets plots
            lowMHTBin  = gjetsDataInputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = gjetsDataInputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = gjetsDataInputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            gjetsDataNJets[m].SetBinContent(h+3,binValue)
            gjetsDataNJets[m].SetBinError(h+3,binError)
            
            if options.debug:
                print gjetsDataInputs[h]
                print "gjets data::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                  highMHTBin,mbin[1],
                                                                                  binValue,binError)
            
            lowMHTBin  = gjets200Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = gjets200Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = gjets200Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            gjets200NJets[m].SetBinContent(h+3,binValue)
            gjets200NJets[m].SetBinError(h+3,binError)

            if options.debug:
                print gjets200Inputs[h]
                print "gjets200::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                highMHTBin,mbin[1],
                                                                                binValue,binError)

            lowMHTBin  = gjets400Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = gjets400Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = gjets400Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            gjets400NJets[m].SetBinContent(h+3,binValue)
            gjets400NJets[m].SetBinError(h+3,binError)

            if options.debug:
                print gjets400Inputs[h]
                print "gjets400::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                highMHTBin,mbin[1],
                                                                                binValue,binError)

            lowMHTBin  = gjetsQCD250Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = gjetsQCD250Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = gjetsQCD250Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            gjetsQCD250NJets[m].SetBinContent(h+3,binValue)
            gjetsQCD250NJets[m].SetBinError(h+3,binError)

            if options.debug:
                print gjetsQCD250Inputs[h]
                print "gjetsQCD250::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                   highMHTBin,mbin[1],
                                                                                   binValue,binError)

            lowMHTBin  = gjetsQCD500Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = gjetsQCD500Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = gjetsQCD500Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            gjetsQCD500NJets[m].SetBinContent(h+3,binValue)
            gjetsQCD500NJets[m].SetBinError(h+3,binError)

            if options.debug:
                print gjetsQCD500Inputs[h]
                print "gjetsQCD500::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                   highMHTBin,mbin[1],
                                                                                   binValue,binError)

            lowMHTBin  = gjetsQCD1000Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = gjetsQCD1000Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = gjetsQCD1000Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            gjetsQCD1000NJets[m].SetBinContent(h+3,binValue)
            gjetsQCD1000NJets[m].SetBinError(h+3,binError)

            if options.debug:
                print gjetsQCD1000Inputs[h]
                print "gjetsQCD1000::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                    highMHTBin,mbin[1],
                                                                                    binValue,binError)

            lowMHTBin  = gjetsTTBarInputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = gjetsTTBarInputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = gjetsTTBarInputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            gjetsTTBarNJets[m].SetBinContent(h+3,binValue)
            gjetsTTBarNJets[m].SetBinError(h+3,binError)

            if options.debug:
                print gjetsTTBarInputs[h]
                print "tt+jets::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                               highMHTBin,mbin[1],
                                                                               binValue,binError)

            lowMHTBin  = gjetsWJetsInputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = gjetsWJetsInputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = gjetsWJetsInputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            gjetsWJetsNJets[m].SetBinContent(h+3,binValue)
            gjetsWJetsNJets[m].SetBinError(h+3,binError)

            if options.debug:
                print gjetsWJetsInputs[h]
                print "w+jets::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                              highMHTBin,mbin[1],
                                                                              binValue,binError)

            ##zmumu plots
            lowMHTBin  = zmumuDataInputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = zmumuDataInputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = zmumuDataInputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            zmumuDataNJets[m].SetBinContent(h+3,binValue)
            zmumuDataNJets[m].SetBinError(h+3,binError)
            
            if options.debug:
                print zmumuDataInputs[h]
                print "zmumu data::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                  highMHTBin,mbin[1],
                                                                                  binValue,binError)
            
            lowMHTBin  = zmumu200Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = zmumu200Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = zmumu200Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            zmumu200NJets[m].SetBinContent(h+3,binValue)
            zmumu200NJets[m].SetBinError(h+3,binError)

            if options.debug:
                print zmumu200Inputs[h]
                print "zmumu200::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                highMHTBin,mbin[1],
                                                                                binValue,binError)

            lowMHTBin  = zmumu400Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = zmumu400Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = zmumu400Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            zmumu400NJets[m].SetBinContent(h+3,binValue)
            zmumu400NJets[m].SetBinError(h+3,binError)
            if options.debug:
                print zmumu400Inputs[h]
                print "zmumu400::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                                highMHTBin,mbin[1],
                                                                                binValue,binError)

            lowMHTBin  = zmumuTTBarInputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = zmumuTTBarInputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = zmumuTTBarInputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            zmumuTTBarNJets[m].SetBinContent(h+3,zmumuTTBarInputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,""))
            zmumuTTBarNJets[m].SetBinError(h+3,binError)

            if options.debug:
                print zmumuTTBarInputs[h]
                print "tt+jets::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                               highMHTBin,mbin[1],
                                                                               binValue,binError)

            #########
            lowMHTBin  = zinv200Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = zinv200Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = zinv200Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            zinv200NJets[m].SetBinContent(h+3,binValue)
            zinv200NJets[m].SetBinError(h+3,binError)
            if options.debug:
                print zinv200Inputs[h]
                print "zinv200::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                               highMHTBin,mbin[1],
                                                                               binValue,binError)
            #
            lowMHTBin  = zinv400Inputs[h].GetYaxis().FindBin(mbin[0])
            highMHTBin = zinv400Inputs[h].GetYaxis().FindBin(mbin[1])
            binError = r.Double(0.)
            binValue = zinv400Inputs[h].IntegralAndError(0,-1,lowMHTBin,highMHTBin,binError,"")
            zinv400NJets[m].SetBinContent(h+3,binValue)
            zinv400NJets[m].SetBinError(h+3,binError)
            if options.debug:
                print zinv400Inputs[h]
                print "zinv400::low:%d(%d), high:%d(%d), integral:%d+/-%2.2f"%(lowMHTBin,mbin[0],
                                                                               highMHTBin,mbin[1],
                                                                               binValue,binError)
        #########
        gjetsDataNJets[m]   .Scale(photonDataSF)
        gjets200NJets[m]    .Scale(photonSFht200)
        gjets400NJets[m]    .Scale(photonSFht400)
        gjetsQCD250NJets[m] .Scale(photonSFqcd250)
        gjetsQCD500NJets[m] .Scale(photonSFqcd500)
        gjetsQCD1000NJets[m].Scale(photonSFqcd1000)
        gjetsTTBarNJets[m]  .Scale(photonSFttbar)
        gjetsWJetsNJets[m]  .Scale(photonSFwjets)

        gjetsMCNJets   .append(gjets400NJets[m].Clone("photons_signalTotal_%s"%(mbin[2])))
        gjetsMCNJets[m].Add(gjets200NJets[m])

        gjetsQCDNJets   .append(gjetsQCD250NJets[m].Clone("photons_qcdTotal_%s"%(mbin[2])))
        gjetsQCDNJets[m].Add(gjetsQCD500NJets[m])
        gjetsQCDNJets[m].Add(gjetsQCD1000NJets[m])

        gjetsTotNJets   .append(gjetsMCNJets[m].Clone("photons_mcTotal_%s"%(mbin[2])))
        gjetsTotNJets[m].Add(gjetsQCDNJets[m])
        gjetsTotNJets[m].Add(gjetsTTBarNJets[m])
        gjetsTotNJets[m].Add(gjetsWJetsNJets[m])

        gjetsDataNJets[m]   .SetMarkerColor(r.kBlack)
        gjets200NJets[m]    .SetMarkerColor(r.kOrange+10)
        gjets400NJets[m]    .SetMarkerColor(r.kOrange+2)
        gjetsMCNJets[m]     .SetMarkerColor(r.kOrange)
        gjetsQCD250NJets[m] .SetMarkerColor(r.kRed+1)
        gjetsQCD500NJets[m] .SetMarkerColor(r.kRed+2)
        gjetsQCD1000NJets[m].SetMarkerColor(r.kRed+3)
        gjetsQCDNJets[m]    .SetMarkerColor(r.kRed)
        gjetsTTBarNJets[m]  .SetMarkerColor(r.kCyan+2)
        gjetsWJetsNJets[m]  .SetMarkerColor(r.kGreen+3)
        gjetsTotNJets[m]    .SetMarkerColor(r.kViolet)

        gjetsDataNJets[m]   .SetLineColor(r.kBlack)
        gjets200NJets[m]    .SetLineColor(r.kOrange+10)
        gjets400NJets[m]    .SetLineColor(r.kOrange+2)
        gjetsMCNJets[m]     .SetLineColor(r.kOrange)
        gjetsQCD250NJets[m] .SetLineColor(r.kRed+1)
        gjetsQCD500NJets[m] .SetLineColor(r.kRed+2)
        gjetsQCD1000NJets[m].SetLineColor(r.kRed+3)
        gjetsQCDNJets[m]    .SetLineColor(r.kRed)
        gjetsTTBarNJets[m]  .SetLineColor(r.kCyan+2)
        gjetsWJetsNJets[m]  .SetLineColor(r.kGreen+3)
        gjetsTotNJets[m]    .SetLineColor(r.kViolet)

        gjetsDataNJets[m]   .SetLineWidth(2)
        gjets200NJets[m]    .SetLineWidth(2)
        gjets400NJets[m]    .SetLineWidth(2)
        gjetsMCNJets[m]     .SetLineWidth(2)
        gjetsQCD250NJets[m] .SetLineWidth(2)
        gjetsQCD500NJets[m] .SetLineWidth(2)
        gjetsQCD1000NJets[m].SetLineWidth(2)
        gjetsQCDNJets[m]    .SetLineWidth(2)
        gjetsTTBarNJets[m]  .SetLineWidth(2)
        gjetsWJetsNJets[m]  .SetLineWidth(2)
        gjetsTotNJets[m]    .SetLineWidth(2)

        gjetsDataNJets[m]   .Write()
        gjets200NJets[m]    .Write()
        gjets400NJets[m]    .Write()
        gjetsQCD250NJets[m] .Write()
        gjetsQCD500NJets[m] .Write()
        gjetsQCD1000NJets[m].Write()
        gjetsTTBarNJets[m]  .Write()
        gjetsWJetsNJets[m]  .Write()
        gjetsMCNJets[m]     .Write()
        gjetsQCDNJets[m]    .Write()
        gjetsTotNJets[m]    .Write()
        ####
        zmumuDataNJets[m].Scale(zmumuDataSF)
        zmumu200NJets[m].Scale(zmumuSFht200)
        zmumu400NJets[m].Scale(zmumuSFht400)
        zmumuTTBarNJets[m].Scale(zmumuSFttbar)

        zmumuMCNJets   .append(zmumu400NJets[m].Clone("zmumu_signalTotal_%s"%(mbin[2])))
        zmumuMCNJets[m].Add(zmumu200NJets[m])

        zmumuTotNJets   .append(zmumu400NJets[m].Clone("zmumu_mcTotal_%s"%(mbin[2])))
        zmumuTotNJets[m].Add(zmumu200NJets[m])
        zmumuTotNJets[m].Add(zmumuTTBarNJets[m])

        zmumuDataNJets[m] .SetMarkerColor(r.kBlack)
        zmumu200NJets[m]  .SetMarkerColor(r.kMagenta+1)
        zmumu400NJets[m]  .SetMarkerColor(r.kMagenta+2)
        zmumuMCNJets[m]   .SetMarkerColor(r.kMagenta+3)
        zmumuTTBarNJets[m].SetMarkerColor(r.kCyan+2)
        zmumuTotNJets[m]  .SetMarkerColor(r.kViolet)

        zmumuDataNJets[m] .SetLineColor(r.kBlack)
        zmumu200NJets[m]  .SetLineColor(r.kMagenta+1)
        zmumu400NJets[m]  .SetLineColor(r.kMagenta+2)
        zmumuMCNJets[m]   .SetLineColor(r.kMagenta+3)
        zmumuTTBarNJets[m].SetLineColor(r.kCyan+2)
        zmumuTotNJets[m]  .SetLineColor(r.kViolet)

        zmumuDataNJets[m] .SetLineWidth(2)
        zmumu200NJets[m]  .SetLineWidth(2)
        zmumu400NJets[m]  .SetLineWidth(2)
        zmumuTTBarNJets[m].SetLineWidth(2)
        zmumuMCNJets[m]   .SetLineWidth(2)
        zmumuTotNJets[m]  .SetLineWidth(2)

        zmumuDataNJets[m] .Write()
        zmumu200NJets[m]  .Write()
        zmumu400NJets[m]  .Write()
        zmumuTTBarNJets[m].Write()
        zmumuMCNJets[m]   .Write()
        zmumuTotNJets[m]  .Write()

        ###Z Invisible###
        zinv200NJets[    m].Scale(zinvSFht200)
        zinv400NJets[    m].Scale(zinvSFht400)
        #
        zinvMCNJets.append(zinv400NJets[m].Clone("zinv_signalTotal_%s"%(mbin[2])))
        zinvMCNJets[m].Add(zinv200NJets[m])
        zinv200NJets[    m].SetMarkerColor(r.kAzure+1)
        zinv400NJets[    m].SetMarkerColor(r.kAzure+2)
        zinvMCNJets[     m].SetMarkerColor(r.kAzure+3)
        zinv200NJets[  m].SetLineColor(r.kAzure+1)
        zinv400NJets[  m].SetLineColor(r.kAzure+2)
        zinvMCNJets[   m].SetLineColor(r.kAzure+3)
        zinv200NJets[    m].SetLineWidth(2)
        zinv400NJets[    m].SetLineWidth(2)
        zinvMCNJets[     m].SetLineWidth(2)
        zinv200NJets[    m].Write()
        zinv400NJets[    m].Write()
        zinvMCNJets[     m].Write()
        #outputCanvas = r.TCanvas("output","output",600,600)
        #outputCanvas.cd()
        #plotPad  = r.TPad("plotPad", "plotPad",0.0,0.2,1.0,1.0)
        #plotPad.SetTopMargin(0.025)
        #plotPad.SetBottomMargin(0.05)
        #plotPad.SetLeftMargin(0.05)
        #plotPad.SetRightMargin(0.025)
        #plotPad.Draw()
        #plotPad.cd()
        #
        #zmumuDataNJets[m] .SetNdivisions(210)
        #zmumuDataNJets[m] .SetMinimum(0.01)
        #zmumuDataNJets[m] .SetStats(0)
        #zmumuDataNJets[m] .SetTitle("")
        #zmumu200NJets[m]  .SetStats(0)
        #zmumu400NJets[m]  .SetStats(0)
        #zmumuTTBarNJets[m].SetStats(0)
        #zmumuMCNJets[m]   .SetStats(0)
        #zmumuTotNJets[m]  .SetStats(0)
        #zmumuDataNJets[m] .Draw("ep0")
        #zmumu200NJets[m]  .Draw("ep0sames")
        #zmumu400NJets[m]  .Draw("ep0sames")
        #zmumuTTBarNJets[m].Draw("ep0sames")
        #zmumuMCNJets[m]   .Draw("ep0sames")
        #zmumuTotNJets[m]  .Draw("ep0sames")
        #plotPad.SetLogy(1)
        #plotPad.SetGrid()
        #outputCanvas.cd()
        #ratioPad = r.TPad("ratioPad","ratioPad",0.0,0.0,1.0,0.2)
        #ratioPad.SetTopMargin(0.05)
        #ratioPad.SetBottomMargin(0.075)
        #ratioPad.SetLeftMargin(0.05)
        #ratioPad.SetRightMargin(0.025)
        #ratioPad.Draw()
        #ratioPad.cd()
        #ratioHisto = zmumuDataNJets[m].Clone("ratio")
        #ratioHisto.Divide(zmumuDataNJets[m],zmumuTotNJets[m],1.0,1.0,"")
        #ratioHisto.GetYaxis().SetNdivisions(205)
        #ratioHisto.SetMaximum(2)
        #ratioHisto.SetMinimum(0)
        #ratioHisto.GetYaxis().SetLabelSize(0.15)
        #ratioHisto.GetXaxis().SetLabelSize(0.15)
        #ratioHisto.Draw("ep0")
        #ratioPad.SetGrid()
        #
        #if options.debug:
        #    raw_input("Press any key to continue...")

    #outputFile.Write()
    outputFile.Close()
    #if options.debug:
    #    raw_input("Press Enter to exit main...")
################
####very end####
if __name__ == '__main__':
    main()
