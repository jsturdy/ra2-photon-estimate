import sys,os
import ROOT as r
from array import array
import math
import optparse
import histoInformation as histoInfo
import rootGarbageCollection


def main() :
    parser = optparse.OptionParser(description="Driver parameters for makeGenRatioPlots.py")
    parser.add_option('-d', '--debug',   action="store_true", default=False, dest="debug")
    parser.add_option('-n', '--nnlo',    action="store_true", default=False, dest="useNNLO")
    parser.add_option('-o', '--outDir',  type='string', action="store", default="/tmp", dest="outDir")
    parser.add_option('-i', '--inDir',   type='string', action="store", default="/tmp", dest="inDir")

    options, args = parser.parse_args()
    if options.debug:
        raw_input("Press Enter to begin...")
        r.gROOT.SetBatch(False)
    else:
        r.gROOT.SetBatch(True)

    sfSuffix = "LO"
    if options.useNNLO:
        sfSuffix = "NNLO"

    ### %s used to be "new"
    inputFile = r.TFile("%s/dataMCplots_%s_v1.root"%(options.outDir,sfSuffix),"READ")
    outputFile = r.TFile("%s/dataMCplots_%s_v3.root"%(options.outDir,sfSuffix),"RECREATE")
    
    histoNames = [
        ["nj1","N_{Jets} = 2"],#2
        ["nj2","N_{Jets} = 3"],#3
        ["nj3","N_{Jets} = 4"],#4
        ["nj4","N_{Jets} = 5"],#5
        ["nj5","N_{Jets} = 6"],#6
        ["nj6","N_{Jets} = 7"],#7
        ["nj7","N_{Jets}#geq 8"],#[8,)
        ["nj3to5","3 #leq N_{Jets}#leq 5",["nj2","nj3","nj4"]],#[8,)
        ["nj6to7","6 #leq N_{Jets}#leq 7",["nj5","nj6"]],#[8,)
        ["nj3plus","N_{Jets}#geq 3",["nj2","nj3","nj4","nj5","nj6","nj7"]],#[8,)
        ["nj2plus","N_{Jets}#geq 2",["nj1","nj2","nj3","nj4","nj5","nj6","nj7"]],#[8,)
        ]
    ##MHT bins
    #(The HT bins are nbins= 25, low=0, high=2500; the MHT bins are nbins=20, low=0, high=1000)
    
    mhtBins = [[100,199,"100to200"],
               [200,299,"200to300"],
               [300,449,"300to450"],
               [100,10000,"100toInf"],
               [200,10000,"200toInf"],
               [450,10000,"450toInf"]]
    
    gjetsDataNJets    = []
    gjets200NJets     = []
    gjets400NJets     = []
    gjetsMCNJets      = []
    gjetsQCD500NJets  = []
    gjetsQCD1000NJets = []
    gjetsQCDNJets     = []
    gjetsTTBarNJets   = []
    gjetsWJetsNJets   = []
    gjetsTotNJets     = []
    
    zmumuDataNJets  = []
    zmumu200NJets   = []
    zmumu400NJets   = []
    zmumuMCNJets    = []
    zmumuTotNJets   = []
    zmumuTTBarNJets = []
    
    zinv200NJets   = []
    zinv400NJets   = []
    zinvMCNJets    = []
    zinvTotNJets   = []
    
    for m,mbin in enumerate(mhtBins):
        gjetsDataNJets.append(   inputFile.Get("gjetsDataNJets_%s"%(mbin[2])   ))
        gjets200NJets.append(    inputFile.Get("gjets200NJets_%s"%(mbin[2])    ))
        gjets400NJets.append(    inputFile.Get("gjets400NJets_%s"%(mbin[2])    ))
        gjetsQCD500NJets.append( inputFile.Get("gjetsQCD500NJets_%s"%(mbin[2]) ))
        gjetsQCD1000NJets.append(inputFile.Get("gjetsQCD1000NJets_%s"%(mbin[2])))
        gjetsTTBarNJets.append(  inputFile.Get("gjetsTTBarNJets_%s"%(mbin[2])  ))
        gjetsWJetsNJets.append(  inputFile.Get("gjetsWJetsNJets_%s"%(mbin[2])  ))
        gjetsDataNJets[   m].SetStats(0)
        gjets200NJets[    m].SetStats(0)
        gjets400NJets[    m].SetStats(0)
        gjetsQCD500NJets[ m].SetStats(0)
        gjetsQCD1000NJets[m].SetStats(0)
        gjetsTTBarNJets[  m].SetStats(0)
        gjetsWJetsNJets[  m].SetStats(0)
        #
        zmumuDataNJets.append( inputFile.Get("zmumuDataNJets_%s"%(mbin[2]) ))
        zmumu200NJets.append(  inputFile.Get("zmumu200NJets_%s"%(mbin[2])  ))
        zmumu400NJets.append(  inputFile.Get("zmumu400NJets_%s"%(mbin[2])  ))
        zmumuTTBarNJets.append(inputFile.Get("zmumuTTBarNJets_%s"%(mbin[2])))
        zmumuDataNJets[ m].SetStats(0)
        zmumu200NJets[  m].SetStats(0)
        zmumu400NJets[  m].SetStats(0)
        zmumuTTBarNJets[m].SetStats(0)

        zinv200NJets.append(  inputFile.Get("zinv200NJets_%s"%(mbin[2])  ))
        zinv400NJets.append(  inputFile.Get("zinv400NJets_%s"%(mbin[2])  ))
        zinv200NJets[  m].SetStats(0)
        zinv400NJets[  m].SetStats(0)

        gjetsMCNJets.append(gjets400NJets[m].Clone("photons_signalTotal_%s"%(mbin[2])))
        gjetsMCNJets[m].Add(gjets200NJets[m])

        gjetsQCDNJets.append(gjetsQCD500NJets[m].Clone("photons_qcdTotal_%s"%(mbin[2])))
        gjetsQCDNJets[m].Add(gjetsQCD1000NJets[m])

        gjetsTotNJets.append(gjetsMCNJets[m].Clone("photons_mcTotal_%s"%(mbin[2])))
        gjetsTotNJets[m].Add(gjetsQCDNJets[m])
        gjetsTotNJets[m].Add(gjetsTTBarNJets[m])
        gjetsTotNJets[m].Add(gjetsWJetsNJets[m])

        gjetsDataNJets[   m].SetMarkerColor(r.kBlack)
        gjets200NJets[    m].SetMarkerColor(r.kOrange+10)
        gjets400NJets[    m].SetMarkerColor(r.kOrange+2)
        gjetsMCNJets[     m].SetMarkerColor(r.kOrange)
        gjetsQCD500NJets[ m].SetMarkerColor(r.kRed+2)
        gjetsQCD1000NJets[m].SetMarkerColor(r.kRed+3)
        gjetsQCDNJets[    m].SetMarkerColor(r.kRed)
        gjetsTTBarNJets[  m].SetMarkerColor(r.kCyan+2)
        gjetsWJetsNJets[  m].SetMarkerColor(r.kGreen+3)
        gjetsTotNJets[    m].SetMarkerColor(r.kViolet)
    
        gjetsDataNJets[   m].SetLineColor(r.kBlack)
        gjets200NJets[    m].SetLineColor(r.kOrange+10)
        gjets400NJets[    m].SetLineColor(r.kOrange+2)
        gjetsMCNJets[     m].SetLineColor(r.kOrange)
        gjetsQCD500NJets[ m].SetLineColor(r.kRed+2)
        gjetsQCD1000NJets[m].SetLineColor(r.kRed+3)
        gjetsQCDNJets[    m].SetLineColor(r.kRed)
        gjetsTTBarNJets[  m].SetLineColor(r.kCyan+2)
        gjetsWJetsNJets[  m].SetLineColor(r.kGreen+3)
        gjetsTotNJets[    m].SetLineColor(r.kViolet)
    
        gjetsDataNJets[   m].SetLineWidth(2)
        gjets200NJets[    m].SetLineWidth(2)
        gjets400NJets[    m].SetLineWidth(2)
        gjetsMCNJets[     m].SetLineWidth(2)
        gjetsQCD500NJets[ m].SetLineWidth(2)
        gjetsQCD1000NJets[m].SetLineWidth(2)
        gjetsQCDNJets[    m].SetLineWidth(2)
        gjetsTTBarNJets[  m].SetLineWidth(2)
        gjetsWJetsNJets[  m].SetLineWidth(2)
        gjetsTotNJets[    m].SetLineWidth(2)
    
        gjetsDataNJets[   m].Write()
        gjets200NJets[    m].Write()
        gjets400NJets[    m].Write()
        gjetsMCNJets[     m].Write()
        gjetsQCD500NJets[ m].Write()
        gjetsQCD1000NJets[m].Write()
        gjetsQCDNJets[    m].Write()
        gjetsTTBarNJets[  m].Write()
        gjetsWJetsNJets[  m].Write()
        gjetsTotNJets[    m].Write()
    
    
        zmumuMCNJets.append(zmumu400NJets[m].Clone("zmumu_signalTotal_%s"%(mbin[2])))
        zmumuMCNJets[m].Add(zmumu200NJets[m])
    
        zmumuTotNJets.append(zmumu400NJets[m].Clone("zmumu_mcTotal_%s"%(mbin[2])))
        zmumuTotNJets[m].Add(zmumu200NJets[m])
        zmumuTotNJets[m].Add(zmumuTTBarNJets[m])
    
        zmumuDataNJets[ m].SetMarkerColor(r.kBlack)
        zmumu200NJets[  m].SetMarkerColor(r.kMagenta+1)
        zmumu400NJets[  m].SetMarkerColor(r.kMagenta+2)
        zmumuMCNJets[   m].SetMarkerColor(r.kMagenta+3)
        zmumuTTBarNJets[m].SetMarkerColor(r.kCyan+2)
        zmumuTotNJets[  m].SetMarkerColor(r.kViolet)
    
        zmumuDataNJets[ m].SetLineColor(r.kBlack)
        zmumu200NJets[  m].SetLineColor(r.kMagenta+1)
        zmumu400NJets[  m].SetLineColor(r.kMagenta+2)
        zmumuMCNJets[   m].SetLineColor(r.kMagenta+3)
        zmumuTTBarNJets[m].SetLineColor(r.kCyan+2)
        zmumuTotNJets[  m].SetLineColor(r.kViolet)
    
        zmumuDataNJets[ m].SetLineWidth(2)
        zmumu200NJets[  m].SetLineWidth(2)
        zmumu400NJets[  m].SetLineWidth(2)
        zmumuTTBarNJets[m].SetLineWidth(2)
        zmumuMCNJets[   m].SetLineWidth(2)
        zmumuTotNJets[  m].SetLineWidth(2)
    
        zmumuDataNJets[ m].Write()
        zmumu200NJets[  m].Write()
        zmumu400NJets[  m].Write()
        zmumuTTBarNJets[m].Write()
        zmumuMCNJets[   m].Write()
        zmumuTotNJets[  m].Write()
    
        zinvMCNJets.append(zinv400NJets[m].Clone("zinv_signalTotal_%s"%(mbin[2])))
        zinvMCNJets[m].Add(zinv200NJets[m])
    
        zinv200NJets[  m].SetMarkerColor(r.kAzure+1)
        zinv400NJets[  m].SetMarkerColor(r.kAzure+2)
        zinvMCNJets[   m].SetMarkerColor(r.kAzure+3)
    
        zinv200NJets[  m].SetLineColor(r.kAzure+1)
        zinv400NJets[  m].SetLineColor(r.kAzure+2)
        zinvMCNJets[   m].SetLineColor(r.kAzure+3)
    
        zinv200NJets[  m].SetLineWidth(2)
        zinv400NJets[  m].SetLineWidth(2)
        zinvMCNJets[   m].SetLineWidth(2)
    
        zinv200NJets[  m].Write()
        zinv400NJets[  m].Write()
        zinvMCNJets[   m].Write()
    
    for j,hname in enumerate(histoNames):
        if j < 7:
            gjetsDataHT =   inputFile.Get("gjetsDataHT_%s_rebinned"%(hname[0])   )
            gjets200HT =    inputFile.Get("gjets200HT_%s_rebinned"%(hname[0])    )
            gjets400HT =    inputFile.Get("gjets400HT_%s_rebinned"%(hname[0])    )
            gjetsQCD500HT = inputFile.Get("gjetsQCD500HT_%s_rebinned"%(hname[0]) )
            gjetsQCD1000HT =inputFile.Get("gjetsQCD1000HT_%s_rebinned"%(hname[0]))
            gjetsTTBarHT =  inputFile.Get("gjetsTTBarHT_%s_rebinned"%(hname[0])  )
            gjetsWJetsHT =  inputFile.Get("gjetsWJetsHT_%s_rebinned"%(hname[0])  )

            zmumuDataHT = inputFile.Get("zmumuDataHT_%s_rebinned"%(hname[0]) )
            zmumu200HT =  inputFile.Get("zmumu200HT_%s_rebinned"%(hname[0])  )
            zmumu400HT =  inputFile.Get("zmumu400HT_%s_rebinned"%(hname[0])  )
            zmumuTTBarHT =inputFile.Get("zmumuTTBarHT_%s_rebinned"%(hname[0]))

            zinv200HT =  inputFile.Get("zinv200HT_%s_rebinned"%(hname[0])  )
            zinv400HT =  inputFile.Get("zinv400HT_%s_rebinned"%(hname[0])  )
        else:
            gjetsDataHT =   inputFile.Get("gjetsDataHT_%s_rebinned"%(   hname[2][0])).Clone("gjetsDataHT_%s_rebinned"%(   hname[0]))
            gjets200HT =    inputFile.Get("gjets200HT_%s_rebinned"%(    hname[2][0])).Clone("gjets200HT_%s_rebinned"%(    hname[0]))
            gjets400HT =    inputFile.Get("gjets400HT_%s_rebinned"%(    hname[2][0])).Clone("gjets400HT_%s_rebinned"%(    hname[0]))
            gjetsQCD500HT = inputFile.Get("gjetsQCD500HT_%s_rebinned"%( hname[2][0])).Clone("gjetsQCD500HT_%s_rebinned"%( hname[0]))
            gjetsQCD1000HT =inputFile.Get("gjetsQCD1000HT_%s_rebinned"%(hname[2][0])).Clone("gjetsQCD1000HT_%s_rebinned"%(hname[0]))
            gjetsTTBarHT =  inputFile.Get("gjetsTTBarHT_%s_rebinned"%(  hname[2][0])).Clone("gjetsTTBarHT_%s_rebinned"%(  hname[0]))
            gjetsWJetsHT =  inputFile.Get("gjetsWJetsHT_%s_rebinned"%(  hname[2][0])).Clone("gjetsWJetsHT_%s_rebinned"%(  hname[0]))

            zmumuDataHT = inputFile.Get("zmumuDataHT_%s_rebinned"%( hname[2][0])).Clone("zmumuDataHT_%s_rebinned"%( hname[0]))
            zmumu200HT =  inputFile.Get("zmumu200HT_%s_rebinned"%(  hname[2][0])).Clone("zmumu200HT_%s_rebinned"%(  hname[0]))
            zmumu400HT =  inputFile.Get("zmumu400HT_%s_rebinned"%(  hname[2][0])).Clone("zmumu400HT_%s_rebinned"%(  hname[0]))
            zmumuTTBarHT =inputFile.Get("zmumuTTBarHT_%s_rebinned"%(hname[2][0])).Clone("zmumuTTBarHT_%s_rebinned"%(hname[0]))

            zinv200HT = inputFile.Get("zinv200HT_%s_rebinned"%(hname[2][0]) ).Clone("zinv200HT_%s_rebinned"%(hname[0]))
            zinv400HT = inputFile.Get("zinv400HT_%s_rebinned"%(hname[2][0]) ).Clone("zinv400HT_%s_rebinned"%(hname[0]))
            
            for addbin in range(len(hname[2])-1):
                gjetsDataHT.Add(   inputFile.Get("gjetsDataHT_%s_rebinned"%(   hname[2][addbin+1])))
                gjets200HT.Add(    inputFile.Get("gjets200HT_%s_rebinned"%(    hname[2][addbin+1])))
                gjets400HT.Add(    inputFile.Get("gjets400HT_%s_rebinned"%(    hname[2][addbin+1])))
                gjetsQCD500HT.Add( inputFile.Get("gjetsQCD500HT_%s_rebinned"%( hname[2][addbin+1])))
                gjetsQCD1000HT.Add(inputFile.Get("gjetsQCD1000HT_%s_rebinned"%(hname[2][addbin+1])))
                gjetsTTBarHT.Add(  inputFile.Get("gjetsTTBarHT_%s_rebinned"%(  hname[2][addbin+1])))
                gjetsWJetsHT.Add(  inputFile.Get("gjetsWJetsHT_%s_rebinned"%(  hname[2][addbin+1])))
                
                zmumuDataHT.Add( inputFile.Get("zmumuDataHT_%s_rebinned"%( hname[2][addbin+1])))
                zmumu200HT.Add(  inputFile.Get("zmumu200HT_%s_rebinned"%(  hname[2][addbin+1])))
                zmumu400HT.Add(  inputFile.Get("zmumu400HT_%s_rebinned"%(  hname[2][addbin+1])))
                zmumuTTBarHT.Add(inputFile.Get("zmumuTTBarHT_%s_rebinned"%(hname[2][addbin+1])))
                
                zinv200HT.Add(inputFile.Get("zinv200HT_%s_rebinned"%(hname[2][addbin+1])))
                zinv400HT.Add(inputFile.Get("zinv400HT_%s_rebinned"%(hname[2][addbin+1])))
                
        gjetsDataHT.SetStats(0)
        gjets200HT.SetStats(0)
        gjets400HT.SetStats(0)
        gjetsQCD500HT.SetStats(0)
        gjetsQCD1000HT.SetStats(0)
        gjetsTTBarHT.SetStats(0)
        gjetsWJetsHT.SetStats(0)
        #
        zmumuDataHT.SetStats(0)
        zmumu200HT.SetStats(0)
        zmumu400HT.SetStats(0)
        zmumuTTBarHT.SetStats(0)
        
        zinv200HT.SetStats(0)
        zinv400HT.SetStats(0)
        
        gjetsMCHT = gjets400HT.Clone("photons_signalTotal_HT_%s"%(hname[0]))
        gjetsMCHT.Add(gjets200HT)
        
        gjetsQCDHT =gjetsQCD500HT.Clone("photons_qcdTotal_HT_%s"%(hname[0]))
        gjetsQCDHT.Add(gjetsQCD1000HT)
        
        gjetsTotHT =gjetsMCHT.Clone("photons_mcTotal_HT_%s"%(hname[0]))
        gjetsTotHT.Add(gjetsQCDHT)
        gjetsTotHT.Add(gjetsTTBarHT)
        gjetsTotHT.Add(gjetsWJetsHT)
        
        gjetsDataHT.SetMarkerColor(r.kBlack)
        gjets200HT.SetMarkerColor(r.kOrange+10)
        gjets400HT.SetMarkerColor(r.kOrange+2)
        gjetsMCHT.SetMarkerColor(r.kOrange)
        gjetsQCD500HT.SetMarkerColor(r.kRed+2)
        gjetsQCD1000HT.SetMarkerColor(r.kRed+3)
        gjetsQCDHT.SetMarkerColor(r.kRed)
        gjetsTTBarHT.SetMarkerColor(r.kCyan+2)
        gjetsWJetsHT.SetMarkerColor(r.kGreen+3)
        gjetsTotHT.SetMarkerColor(r.kViolet)
        
        gjetsDataHT.SetLineColor(r.kBlack)
        gjets200HT.SetLineColor(r.kOrange+10)
        gjets400HT.SetLineColor(r.kOrange+2)
        gjetsMCHT.SetLineColor(r.kOrange)
        gjetsQCD500HT.SetLineColor(r.kRed+2)
        gjetsQCD1000HT.SetLineColor(r.kRed+3)
        gjetsQCDHT.SetLineColor(r.kRed)
        gjetsTTBarHT.SetLineColor(r.kCyan+2)
        gjetsWJetsHT.SetLineColor(r.kGreen+3)
        gjetsTotHT.SetLineColor(r.kViolet)
        
        gjetsDataHT.SetLineWidth(2)
        gjets200HT.SetLineWidth(2)
        gjets400HT.SetLineWidth(2)
        gjetsMCHT.SetLineWidth(2)
        gjetsQCD500HT.SetLineWidth(2)
        gjetsQCD1000HT.SetLineWidth(2)
        gjetsQCDHT.SetLineWidth(2)
        gjetsTTBarHT.SetLineWidth(2)
        gjetsWJetsHT.SetLineWidth(2)
        gjetsTotHT.SetLineWidth(2)
        
        gjetsDataHT.Write()
        gjets200HT.Write()
        gjets400HT.Write()
        gjetsMCHT.Write()
        gjetsQCD500HT.Write()
        gjetsQCD1000HT.Write()
        gjetsQCDHT.Write()
        gjetsTTBarHT.Write()
        gjetsWJetsHT.Write()
        gjetsTotHT.Write()
        
        
        zmumuMCHT =zmumu400HT.Clone("zmumu_signalTotal_HT_%s"%(hname[0]))
        zmumuMCHT.Add(zmumu200HT)
        
        zmumuTotHT =zmumu400HT.Clone("zmumu_mcTotal_HT_%s"%(hname[0]))
        zmumuTotHT.Add(zmumu200HT)
        zmumuTotHT.Add(zmumuTTBarHT)
        
        zmumuDataHT.SetMarkerColor(r.kBlack)
        zmumu200HT.SetMarkerColor(r.kMagenta+1)
        zmumu400HT.SetMarkerColor(r.kMagenta+2)
        zmumuMCHT.SetMarkerColor(r.kMagenta+3)
        zmumuTTBarHT.SetMarkerColor(r.kCyan+2)
        zmumuTotHT.SetMarkerColor(r.kViolet)
        
        zmumuDataHT.SetLineColor(r.kBlack)
        zmumu200HT.SetLineColor(r.kMagenta+1)
        zmumu400HT.SetLineColor(r.kMagenta+2)
        zmumuMCHT.SetLineColor(r.kMagenta+3)
        zmumuTTBarHT.SetLineColor(r.kCyan+2)
        zmumuTotHT.SetLineColor(r.kViolet)
        
        zmumuDataHT.SetLineWidth(2)
        zmumu200HT.SetLineWidth(2)
        zmumu400HT.SetLineWidth(2)
        zmumuTTBarHT.SetLineWidth(2)
        zmumuMCHT.SetLineWidth(2)
        zmumuTotHT.SetLineWidth(2)
        
        zmumuDataHT.Write()
        zmumu200HT.Write()
        zmumu400HT.Write()
        zmumuTTBarHT.Write()
        zmumuMCHT.Write()
        zmumuTotHT.Write()
        
        zinvMCHT =zinv400HT.Clone("zinv_signalTotal_HT_%s"%(hname[0]))
        zinvMCHT.Add(zinv200HT)
        
        zinv200HT.SetMarkerColor(r.kAzure+1)
        zinv400HT.SetMarkerColor(r.kAzure+2)
        zinvMCHT.SetMarkerColor(r.kAzure+3)
        
        zinv200HT.SetLineColor(r.kAzure+1)
        zinv400HT.SetLineColor(r.kAzure+2)
        zinvMCHT.SetLineColor(r.kAzure+3)
        
        zinv200HT.SetLineWidth(2)
        zinv400HT.SetLineWidth(2)
        zinvMCHT.SetLineWidth(2)
        
        zinv200HT.Write()
        zinv400HT.Write()
        zinvMCHT.Write()
        
    
    
    for j,hname in enumerate(histoNames):
        if j < 7:
            gjetsDataMHT =   inputFile.Get("gjetsDataMHT_%s_rebinned"%(hname[0])   )
            gjets200MHT =    inputFile.Get("gjets200MHT_%s_rebinned"%(hname[0])    )
            gjets400MHT =    inputFile.Get("gjets400MHT_%s_rebinned"%(hname[0])    )
            gjetsQCD500MHT = inputFile.Get("gjetsQCD500MHT_%s_rebinned"%(hname[0]) )
            gjetsQCD1000MHT =inputFile.Get("gjetsQCD1000MHT_%s_rebinned"%(hname[0]))
            gjetsTTBarMHT =  inputFile.Get("gjetsTTBarMHT_%s_rebinned"%(hname[0])  )
            gjetsWJetsMHT =  inputFile.Get("gjetsWJetsMHT_%s_rebinned"%(hname[0])  )

            zmumuDataMHT = inputFile.Get("zmumuDataMHT_%s_rebinned"%(hname[0]) )
            zmumu200MHT =  inputFile.Get("zmumu200MHT_%s_rebinned"%(hname[0])  )
            zmumu400MHT =  inputFile.Get("zmumu400MHT_%s_rebinned"%(hname[0])  )
            zmumuTTBarMHT =inputFile.Get("zmumuTTBarMHT_%s_rebinned"%(hname[0]))

            zinv200MHT =  inputFile.Get("zinv200MHT_%s_rebinned"%(hname[0])  )
            zinv400MHT =  inputFile.Get("zinv400MHT_%s_rebinned"%(hname[0])  )
        else:
            gjetsDataMHT =   inputFile.Get("gjetsDataMHT_%s_rebinned"%(   hname[2][0])).Clone("gjetsDataMHT_%s_rebinned"%(   hname[0]))
            gjets200MHT =    inputFile.Get("gjets200MHT_%s_rebinned"%(    hname[2][0])).Clone("gjets200MHT_%s_rebinned"%(    hname[0]))
            gjets400MHT =    inputFile.Get("gjets400MHT_%s_rebinned"%(    hname[2][0])).Clone("gjets400MHT_%s_rebinned"%(    hname[0]))
            gjetsQCD500MHT = inputFile.Get("gjetsQCD500MHT_%s_rebinned"%( hname[2][0])).Clone("gjetsQCD500MHT_%s_rebinned"%( hname[0]))
            gjetsQCD1000MHT =inputFile.Get("gjetsQCD1000MHT_%s_rebinned"%(hname[2][0])).Clone("gjetsQCD1000MHT_%s_rebinned"%(hname[0]))
            gjetsTTBarMHT =  inputFile.Get("gjetsTTBarMHT_%s_rebinned"%(  hname[2][0])).Clone("gjetsTTBarMHT_%s_rebinned"%(  hname[0]))
            gjetsWJetsMHT =  inputFile.Get("gjetsWJetsMHT_%s_rebinned"%(  hname[2][0])).Clone("gjetsWJetsMHT_%s_rebinned"%(  hname[0]))

            zmumuDataMHT = inputFile.Get("zmumuDataMHT_%s_rebinned"%( hname[2][0])).Clone("zmumuDataMHT_%s_rebinned"%( hname[0]))
            zmumu200MHT =  inputFile.Get("zmumu200MHT_%s_rebinned"%(  hname[2][0])).Clone("zmumu200MHT_%s_rebinned"%(  hname[0]))
            zmumu400MHT =  inputFile.Get("zmumu400MHT_%s_rebinned"%(  hname[2][0])).Clone("zmumu400MHT_%s_rebinned"%(  hname[0]))
            zmumuTTBarMHT =inputFile.Get("zmumuTTBarMHT_%s_rebinned"%(hname[2][0])).Clone("zmumuTTBarMHT_%s_rebinned"%(hname[0]))

            zinv200MHT = inputFile.Get("zinv200MHT_%s_rebinned"%(hname[2][0]) ).Clone("zinv200MHT_%s_rebinned"%(hname[0]))
            zinv400MHT = inputFile.Get("zinv400MHT_%s_rebinned"%(hname[2][0]) ).Clone("zinv400MHT_%s_rebinned"%(hname[0]))
            
            for addbin in range(len(hname[2])-1):
                gjetsDataMHT.Add(   inputFile.Get("gjetsDataMHT_%s_rebinned"%(   hname[2][addbin+1])))
                gjets200MHT.Add(    inputFile.Get("gjets200MHT_%s_rebinned"%(    hname[2][addbin+1])))
                gjets400MHT.Add(    inputFile.Get("gjets400MHT_%s_rebinned"%(    hname[2][addbin+1])))
                gjetsQCD500MHT.Add( inputFile.Get("gjetsQCD500MHT_%s_rebinned"%( hname[2][addbin+1])))
                gjetsQCD1000MHT.Add(inputFile.Get("gjetsQCD1000MHT_%s_rebinned"%(hname[2][addbin+1])))
                gjetsTTBarMHT.Add(  inputFile.Get("gjetsTTBarMHT_%s_rebinned"%(  hname[2][addbin+1])))
                gjetsWJetsMHT.Add(  inputFile.Get("gjetsWJetsMHT_%s_rebinned"%(  hname[2][addbin+1])))
                
                zmumuDataMHT.Add( inputFile.Get("zmumuDataMHT_%s_rebinned"%( hname[2][addbin+1])))
                zmumu200MHT.Add(  inputFile.Get("zmumu200MHT_%s_rebinned"%(  hname[2][addbin+1])))
                zmumu400MHT.Add(  inputFile.Get("zmumu400MHT_%s_rebinned"%(  hname[2][addbin+1])))
                zmumuTTBarMHT.Add(inputFile.Get("zmumuTTBarMHT_%s_rebinned"%(hname[2][addbin+1])))
                
                zinv200MHT.Add(inputFile.Get("zinv200MHT_%s_rebinned"%(hname[2][addbin+1])))
                zinv400MHT.Add(inputFile.Get("zinv400MHT_%s_rebinned"%(hname[2][addbin+1])))
                
        gjetsDataMHT.SetStats(0)
        gjets200MHT.SetStats(0)
        gjets400MHT.SetStats(0)
        gjetsQCD500MHT.SetStats(0)
        gjetsQCD1000MHT.SetStats(0)
        gjetsTTBarMHT.SetStats(0)
        gjetsWJetsMHT.SetStats(0)
        #
        zmumuDataMHT.SetStats(0)
        zmumu200MHT.SetStats(0)
        zmumu400MHT.SetStats(0)
        zmumuTTBarMHT.SetStats(0)
        
        zinv200MHT.SetStats(0)
        zinv400MHT.SetStats(0)
        
        gjetsMCMHT = gjets400MHT.Clone("photons_signalTotal_MHT_%s"%(hname[0]))
        gjetsMCMHT.Add(gjets200MHT)
        
        gjetsQCDMHT =gjetsQCD500MHT.Clone("photons_qcdTotal_MHT_%s"%(hname[0]))
        gjetsQCDMHT.Add(gjetsQCD1000MHT)
        
        gjetsTotMHT =gjetsMCMHT.Clone("photons_mcTotal_MHT_%s"%(hname[0]))
        gjetsTotMHT.Add(gjetsQCDMHT)
        gjetsTotMHT.Add(gjetsTTBarMHT)
        gjetsTotMHT.Add(gjetsWJetsMHT)
        
        gjetsDataMHT.SetMarkerColor(r.kBlack)
        gjets200MHT.SetMarkerColor(r.kOrange+10)
        gjets400MHT.SetMarkerColor(r.kOrange+2)
        gjetsMCMHT.SetMarkerColor(r.kOrange)
        gjetsQCD500MHT.SetMarkerColor(r.kRed+2)
        gjetsQCD1000MHT.SetMarkerColor(r.kRed+3)
        gjetsQCDMHT.SetMarkerColor(r.kRed)
        gjetsTTBarMHT.SetMarkerColor(r.kCyan+2)
        gjetsWJetsMHT.SetMarkerColor(r.kGreen+3)
        gjetsTotMHT.SetMarkerColor(r.kViolet)
        
        gjetsDataMHT.SetLineColor(r.kBlack)
        gjets200MHT.SetLineColor(r.kOrange+10)
        gjets400MHT.SetLineColor(r.kOrange+2)
        gjetsMCMHT.SetLineColor(r.kOrange)
        gjetsQCD500MHT.SetLineColor(r.kRed+2)
        gjetsQCD1000MHT.SetLineColor(r.kRed+3)
        gjetsQCDMHT.SetLineColor(r.kRed)
        gjetsTTBarMHT.SetLineColor(r.kCyan+2)
        gjetsWJetsMHT.SetLineColor(r.kGreen+3)
        gjetsTotMHT.SetLineColor(r.kViolet)
        
        gjetsDataMHT.SetLineWidth(2)
        gjets200MHT.SetLineWidth(2)
        gjets400MHT.SetLineWidth(2)
        gjetsMCMHT.SetLineWidth(2)
        gjetsQCD500MHT.SetLineWidth(2)
        gjetsQCD1000MHT.SetLineWidth(2)
        gjetsQCDMHT.SetLineWidth(2)
        gjetsTTBarMHT.SetLineWidth(2)
        gjetsWJetsMHT.SetLineWidth(2)
        gjetsTotMHT.SetLineWidth(2)
        
        gjetsDataMHT.Write()
        gjets200MHT.Write()
        gjets400MHT.Write()
        gjetsMCMHT.Write()
        gjetsQCD500MHT.Write()
        gjetsQCD1000MHT.Write()
        gjetsQCDMHT.Write()
        gjetsTTBarMHT.Write()
        gjetsWJetsMHT.Write()
        gjetsTotMHT.Write()
        
        
        zmumuMCMHT =zmumu400MHT.Clone("zmumu_signalTotal_MHT_%s"%(hname[0]))
        zmumuMCMHT.Add(zmumu200MHT)
        
        zmumuTotMHT =zmumu400MHT.Clone("zmumu_mcTotal_MHT_%s"%(hname[0]))
        zmumuTotMHT.Add(zmumu200MHT)
        zmumuTotMHT.Add(zmumuTTBarMHT)
        
        zmumuDataMHT.SetMarkerColor(r.kBlack)
        zmumu200MHT.SetMarkerColor(r.kMagenta+1)
        zmumu400MHT.SetMarkerColor(r.kMagenta+2)
        zmumuMCMHT.SetMarkerColor(r.kMagenta+3)
        zmumuTTBarMHT.SetMarkerColor(r.kCyan+2)
        zmumuTotMHT.SetMarkerColor(r.kViolet)
        
        zmumuDataMHT.SetLineColor(r.kBlack)
        zmumu200MHT.SetLineColor(r.kMagenta+1)
        zmumu400MHT.SetLineColor(r.kMagenta+2)
        zmumuMCMHT.SetLineColor(r.kMagenta+3)
        zmumuTTBarMHT.SetLineColor(r.kCyan+2)
        zmumuTotMHT.SetLineColor(r.kViolet)
        
        zmumuDataMHT.SetLineWidth(2)
        zmumu200MHT.SetLineWidth(2)
        zmumu400MHT.SetLineWidth(2)
        zmumuTTBarMHT.SetLineWidth(2)
        zmumuMCMHT.SetLineWidth(2)
        zmumuTotMHT.SetLineWidth(2)
        
        zmumuDataMHT.Write()
        zmumu200MHT.Write()
        zmumu400MHT.Write()
        zmumuTTBarMHT.Write()
        zmumuMCMHT.Write()
        zmumuTotMHT.Write()
        
        zinvMCMHT =zinv400MHT.Clone("zinv_signalTotal_MHT_%s"%(hname[0]))
        zinvMCMHT.Add(zinv200MHT)
        
        zinv200MHT.SetMarkerColor(r.kAzure+1)
        zinv400MHT.SetMarkerColor(r.kAzure+2)
        zinvMCMHT.SetMarkerColor(r.kAzure+3)
        
        zinv200MHT.SetLineColor(r.kAzure+1)
        zinv400MHT.SetLineColor(r.kAzure+2)
        zinvMCMHT.SetLineColor(r.kAzure+3)
        
        zinv200MHT.SetLineWidth(2)
        zinv400MHT.SetLineWidth(2)
        zinvMCMHT.SetLineWidth(2)
        
        zinv200MHT.Write()
        zinv400MHT.Write()
        zinvMCMHT.Write()
        
    
    inputFile.Close()
    outputFile.Close()
####very end####
if __name__ == '__main__':
    main()
