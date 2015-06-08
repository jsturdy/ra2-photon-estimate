import sys,os
import ROOT as r
from array import array
import math
import optparse
import histoInformation as histoInfo
import rootGarbageCollection

def main():
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
    inputFile = r.TFile("%s/dataMCplots_%s_v3.root"%(options.outDir,sfSuffix),"READ")
    outputFile = r.TFile("%s/dataMCplots_%s_v4.root"%(options.outDir,sfSuffix),"RECREATE")
    
##    gjetsDataNJets    = []
##    gjets200NJets     = []
##    gjets400NJets     = []
##    gjetsMCNJets      = []
##    gjetsQCD500NJets  = []
##    gjetsQCD1000NJets = []
##    gjetsQCDNJets     = []
##    gjetsTTBarNJets   = []
##    gjetsWJetsNJets   = []
##    gjetsTotNJets     = []
##    
##    zmumuDataNJets  = []
##    zmumu200NJets   = []
##    zmumu400NJets   = []
##    zmumuMCNJets    = []
##    zmumuTotNJets   = []
##    zmumuTTBarNJets = []
    
    histoNames = [
        ["nj1","N_{Jets} = 2"],#2
        ["nj2","N_{Jets} = 3"],#3
        ["nj3","N_{Jets} = 4"],#4
        ["nj4","N_{Jets} = 5"],#5
        ["nj5","N_{Jets} = 6"],#6
        ["nj6","N_{Jets} = 7"],#7
        ["nj7","N_{Jets}#geq 8"],#[8,)
        ["nj3to5","3 #leq N_{Jets}#leq 5"],#[8,)
        ["nj6to7","6 #leq N_{Jets}#leq 7"],#[8,)
        ["nj3plus","N_{Jets}#geq 3"],#[8,)
        ["nj2plus","N_{Jets}#geq 2"],#[8,)
        ]
    ##MHT bins
    #(The HT bins are nbins= 25, low=0, high=2500; the MHT bins are nbins=20, low=0, high=1000)
    
    mhtBins = [[100,199,"100to200","100#leq#slashH_{T}#leq 200"],
               [200,299,"200to300","200#leq#slashH_{T}#leq 300"],
               [300,449,"300to450","300#leq#slashH_{T}#leq 450"],
               [100,10000,"100toInf","100#leq#slashH_{T}"],
               [200,10000,"200toInf","200#leq#slashH_{T}"],
               [450,10000,"450toInf","450#leq#slashH_{T}"]
               ]
    
    for m,mbin in enumerate(mhtBins):
        gjetsDataNJets =    inputFile.Get("gjetsDataNJets_%s"%(mbin[2]))
        gjets200NJets =     inputFile.Get("gjets200NJets_%s"%(mbin[2]))
        gjets400NJets =     inputFile.Get("gjets400NJets_%s"%(mbin[2]))
        gjetsQCD500NJets =  inputFile.Get("gjetsQCD500NJets_%s"%(mbin[2]))
        gjetsQCD1000NJets = inputFile.Get("gjetsQCD1000NJets_%s"%(mbin[2]))
        gjetsTTBarNJets =   inputFile.Get("gjetsTTBarNJets_%s"%(mbin[2]))
        gjetsWJetsNJets =   inputFile.Get("gjetsWJetsNJets_%s"%(mbin[2]))
        gjetsMCNJets =      inputFile.Get("photons_signalTotal_%s"%(mbin[2]))
        gjetsQCDNJets =     inputFile.Get("photons_qcdTotal_%s"%(mbin[2]))
        gjetsTotNJets =     inputFile.Get("photons_mcTotal_%s"%(mbin[2]))
    #
        gjetsDataBkgdSubNJets = inputFile.Get("gjetsDataNJets_%s"%(mbin[2])).Clone("gjetsDataBkgdSubNJets_%s"%(mbin[2]))
        print gjetsDataBkgdSubNJets
        sys.stdout.flush()
        gjetsDataBkgdSubNJets.Add(gjetsQCDNJets,-1.0)
        gjetsDataBkgdSubNJets.Add(gjetsTTBarNJets,-1.0)
        gjetsDataBkgdSubNJets.Add(gjetsWJetsNJets,-1.0)
        
        zmumuDataNJets =  inputFile.Get("zmumuDataNJets_%s"%(mbin[2]))
        zmumu200NJets =   inputFile.Get("zmumu200NJets_%s"%(mbin[2]))
        zmumu400NJets =   inputFile.Get("zmumu400NJets_%s"%(mbin[2]))
        zmumuTTBarNJets = inputFile.Get("zmumuTTBarNJets_%s"%(mbin[2]))
        zmumuMCNJets =    inputFile.Get("zmumu_signalTotal_%s"%(mbin[2]))
        zmumuTotNJets =   inputFile.Get("zmumu_mcTotal_%s"%(mbin[2]))
        zmumuDataBkgdSubNJets = inputFile.Get("zmumuDataNJets_%s"%(mbin[2])).Clone("zmumuDataBkgdSubNJets_%s"%(mbin[2]))
        zmumuDataBkgdSubNJets.Add(zmumuTTBarNJets,-1.0)
        
        # ##ratios to do
        # photon: data/mc
        makeRatioPlot(gjetsDataNJets,gjetsTotNJets,"photonsDataMC_%s"%(mbin[2]),
                      mbin[3],"#gamma+Jets Data","#gamma+Jets Total MC",2,0,"",options.outDir)
        makeRatioPlot(gjetsMCNJets,gjetsTotNJets,"photonsSignalMC_%s"%(mbin[2]),
                      mbin[3],"#gamma+Jets Signal MC","#gamma+Jets Total MC",1.05,0.9,"B",options.outDir)
        # di-muon: data/mc
        makeRatioPlot(zmumuDataNJets,zmumuTotNJets,"dimuonsDataMC_%s"%(mbin[2]),
                      mbin[3],"Z#rightarrow#mu#mu+Jets Data","Z#rightarrow#mu#mu+Jets Total MC",2,0,"",options.outDir)
        makeRatioPlot(zmumuMCNJets,zmumuTotNJets,"dimuonsSignalMC_%s"%(mbin[2]),
                      mbin[3],"Z#rightarrow#mu#mu+Jets Signal MC","Z#rightarrow#mu#mu+Jets Total MC",1.05,0.9,"B",options.outDir)
        # data: z/gamma, with bkgd sub. on data, all data
        makeRatioPlot(zmumuDataNJets,gjetsDataNJets,"zmumuGammaData_ratio_%s"%(mbin[2]),
                      mbin[3],"Z#rightarrow#mu#mu+Jets Data","#gamma+Jets Data",0.05,0,"",options.outDir)
        makeRatioPlot(zmumuDataBkgdSubNJets,gjetsDataBkgdSubNJets,"zmumuGammaDataBkgdSub_ratio_%s"%(mbin[2]),
                      mbin[3],"Z#rightarrow#mu#mu+Jets Data (bkgd. sub.)","#gamma+Jets Data (bkgd. sub.)",0.05,0,"",options.outDir)
        # mc: z/gamma with bkgds in mc, just mc signal samples
        makeRatioPlot(zmumuMCNJets,gjetsMCNJets,"zmumuGammaMC_ratio_%s"%(mbin[2]),
                      mbin[3],"Z#rightarrow#mu#mu+Jets MC","#gamma+Jets MC",0.05,0,"",options.outDir)
        makeRatioPlot(zmumuTotNJets,gjetsTotNJets,"zmumuGammaMCwBKGD_ratio_%s"%(mbin[2]),
                      mbin[3],"Z#rightarrow#mu#mu+Jets MC (w/ bkgd.)","#gamma+Jets MC (w/ bkgd.)",0.05,0,"",options.outDir)

    for j,hbin in enumerate(histoNames):
        gjetsDataHT =    inputFile.Get("gjetsDataHT_%s_rebinned"%(hbin[0]))
        gjets200HT =     inputFile.Get("gjets200HT_%s_rebinned"%(hbin[0]))
        gjets400HT =     inputFile.Get("gjets400HT_%s_rebinned"%(hbin[0]))
        gjetsQCD500HT =  inputFile.Get("gjetsQCD500HT_%s_rebinned"%(hbin[0]))
        gjetsQCD1000HT = inputFile.Get("gjetsQCD1000HT_%s_rebinned"%(hbin[0]))
        gjetsTTBarHT =   inputFile.Get("gjetsTTBarHT_%s_rebinned"%(hbin[0]))
        gjetsWJetsHT =   inputFile.Get("gjetsWJetsHT_%s_rebinned"%(hbin[0]))
        gjetsMCHT =      inputFile.Get("photons_signalTotal_HT_%s"%(hbin[0]))
        gjetsQCDHT =     inputFile.Get("photons_qcdTotal_HT_%s"%(hbin[0]))
        gjetsTotHT =     inputFile.Get("photons_mcTotal_HT_%s"%(hbin[0]))
    #
        gjetsDataBkgdSubHT = inputFile.Get("gjetsDataHT_%s_rebinned"%(hbin[0])).Clone("gjetsDataBkgdSubHT_%s"%(hbin[0]))
        print gjetsDataHT
        print gjets200HT
        print gjets400HT
        print gjetsQCD500HT
        print gjetsQCD1000HT
        print gjetsTTBarHT
        print gjetsWJetsHT
        print gjetsMCHT
        print gjetsQCDHT
        print gjetsTotHT
        print gjetsDataBkgdSubHT
        sys.stdout.flush()
        gjetsDataBkgdSubHT.Add(gjetsQCDHT,-1.0)
        gjetsDataBkgdSubHT.Add(gjetsTTBarHT,-1.0)
        gjetsDataBkgdSubHT.Add(gjetsWJetsHT,-1.0)
        
        zmumuDataHT =  inputFile.Get("zmumuDataHT_%s_rebinned"%( hbin[0]))
        zmumu200HT =   inputFile.Get("zmumu200HT_%s_rebinned"%(  hbin[0]))
        zmumu400HT =   inputFile.Get("zmumu400HT_%s_rebinned"%(  hbin[0]))
        zmumuTTBarHT = inputFile.Get("zmumuTTBarHT_%s_rebinned"%(hbin[0]))
        zmumuMCHT =    inputFile.Get("zmumu_signalTotal_HT_%s"%( hbin[0]))
        zmumuTotHT =   inputFile.Get("zmumu_mcTotal_HT_%s"%(     hbin[0]))
        zmumuDataBkgdSubHT = inputFile.Get("zmumuDataHT_%s_rebinned"%(hbin[0])).Clone("zmumuDataBkgdSubHT_%s"%(hbin[0]))
        zmumuDataBkgdSubHT.Add(zmumuTTBarHT,-1.0)
        
        # ##ratios to do
        # photon: data/mc
        makeRatioPlot(gjetsDataHT,gjetsTotHT,"photonsDataMC_HT_%s"%(hbin[0]),
                      hbin[1],"#gamma+Jets Data","#gamma+Jets Total MC",2,0,"",options.outDir)
        makeRatioPlot(gjetsMCHT,gjetsTotHT,"photonsSignalMC_HT_%s"%(hbin[0]),
                      hbin[1],"#gamma+Jets Signal MC","#gamma+Jets Total MC",1.05,0.9,"B",options.outDir)
        # di-muon: data/mc
        makeRatioPlot(zmumuDataHT,zmumuTotHT,"dimuonsDataMC_HT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets Data","Z#rightarrow#mu#mu+Jets Total MC",2,0,"",options.outDir)
        makeRatioPlot(zmumuMCHT,zmumuTotHT,"dimuonsSignalMC_HT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets Signal MC","Z#rightarrow#mu#mu+Jets Total MC",1.05,0.9,"B",options.outDir)
        # data: z/gamma, with bkgd sub. on data, all data
        makeRatioPlot(zmumuDataHT,gjetsDataHT,"zmumuGammaData_ratio_HT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets Data","#gamma+Jets Data",0.05,0,"",options.outDir)
        makeRatioPlot(zmumuDataBkgdSubHT,gjetsDataBkgdSubHT,"zmumuGammaDataBkgdSub_ratio_HT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets Data (bkgd. sub.)","#gamma+Jets Data (bkgd. sub.)",0.05,0,"",options.outDir)
        # mc: z/gamma with bkgds in mc, just mc signal samples
        makeRatioPlot(zmumuMCHT,gjetsMCHT,"zmumuGammaMC_ratio_HT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets MC","#gamma+Jets MC",0.05,0,"",options.outDir)
        makeRatioPlot(zmumuTotHT,gjetsTotHT,"zmumuGammaMCwBKGD_ratio_HT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets MC (w/ bkgd.)","#gamma+Jets MC (w/ bkgd.)",0.05,0,"",options.outDir)


    for j,hbin in enumerate(histoNames):
        gjetsDataMHT =    inputFile.Get("gjetsDataMHT_%s_rebinned"%(hbin[0]))
        gjets200MHT =     inputFile.Get("gjets200MHT_%s_rebinned"%(hbin[0]))
        gjets400MHT =     inputFile.Get("gjets400MHT_%s_rebinned"%(hbin[0]))
        gjetsQCD500MHT =  inputFile.Get("gjetsQCD500MHT_%s_rebinned"%(hbin[0]))
        gjetsQCD1000MHT = inputFile.Get("gjetsQCD1000MHT_%s_rebinned"%(hbin[0]))
        gjetsTTBarMHT =   inputFile.Get("gjetsTTBarMHT_%s_rebinned"%(hbin[0]))
        gjetsWJetsMHT =   inputFile.Get("gjetsWJetsMHT_%s_rebinned"%(hbin[0]))
        gjetsMCMHT =      inputFile.Get("photons_signalTotal_MHT_%s"%(hbin[0]))
        gjetsQCDMHT =     inputFile.Get("photons_qcdTotal_MHT_%s"%(hbin[0]))
        gjetsTotMHT =     inputFile.Get("photons_mcTotal_MHT_%s"%(hbin[0]))
    #
        gjetsDataBkgdSubMHT = inputFile.Get("gjetsDataMHT_%s_rebinned"%(hbin[0])).Clone("gjetsDataBkgdSubMHT_%s"%(hbin[0]))
        gjetsDataBkgdSubMHT.Add(gjetsQCDMHT,-1.0)
        gjetsDataBkgdSubMHT.Add(gjetsTTBarMHT,-1.0)
        gjetsDataBkgdSubMHT.Add(gjetsWJetsMHT,-1.0)
        
        zmumuDataMHT =  inputFile.Get("zmumuDataMHT_%s_rebinned"%(hbin[0]))
        zmumu200MHT =   inputFile.Get("zmumu200MHT_%s_rebinned"%(hbin[0]))
        zmumu400MHT =   inputFile.Get("zmumu400MHT_%s_rebinned"%(hbin[0]))
        zmumuTTBarMHT = inputFile.Get("zmumuTTBarMHT_%s_rebinned"%(hbin[0]))
        zmumuMCMHT =    inputFile.Get("zmumu_signalTotal_MHT_%s"%(hbin[0]))
        zmumuTotMHT =   inputFile.Get("zmumu_mcTotal_MHT_%s"%(hbin[0]))
        zmumuDataBkgdSubMHT = inputFile.Get("zmumuDataMHT_%s_rebinned"%(hbin[0])).Clone("zmumuDataBkgdSubMHT_%s"%(hbin[0]))
        zmumuDataBkgdSubMHT.Add(zmumuTTBarMHT,-1.0)
        
        # ##ratios to do
        # photon: data/mc
        makeRatioPlot(gjetsDataMHT,gjetsTotMHT,"photonsDataMC_MHT_%s"%(hbin[0]),
                      hbin[1],"#gamma+Jets Data","#gamma+Jets Total MC",2,0,"",options.outDir)
        makeRatioPlot(gjetsMCMHT,gjetsTotMHT,"photonsSignalMC_MHT_%s"%(hbin[0]),
                      hbin[1],"#gamma+Jets Signal MC","#gamma+Jets Total MC",1.05,0.9,"B",options.outDir)
        # di-muon: data/mc
        makeRatioPlot(zmumuDataMHT,zmumuTotMHT,"dimuonsDataMC_MHT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets Data","Z#rightarrow#mu#mu+Jets Total MC",2,0,"",options.outDir)
        makeRatioPlot(zmumuMCMHT,zmumuTotMHT,"dimuonsSignalMC_MHT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets Signal MC","Z#rightarrow#mu#mu+Jets Total MC",1.05,0.9,"B",options.outDir)
        # data: z/gamma, with bkgd sub. on data, all data
        makeRatioPlot(zmumuDataMHT,gjetsDataMHT,"zmumuGammaData_ratio_MHT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets Data","#gamma+Jets Data",0.05,0,"",options.outDir)
        makeRatioPlot(zmumuDataBkgdSubMHT,gjetsDataBkgdSubMHT,"zmumuGammaDataBkgdSub_ratio_MHT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets Data (bkgd. sub.)","#gamma+Jets Data (bkgd. sub.)",0.05,0,"",options.outDir)
        # mc: z/gamma with bkgds in mc, just mc signal samples
        makeRatioPlot(zmumuMCMHT,gjetsMCMHT,"zmumuGammaMC_ratio_MHT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets MC","#gamma+Jets MC",0.05,0,"",options.outDir)
        makeRatioPlot(zmumuTotMHT,gjetsTotMHT,"zmumuGammaMCwBKGD_ratio_MHT_%s"%(hbin[0]),
                      hbin[1],"Z#rightarrow#mu#mu+Jets MC (w/ bkgd.)","#gamma+Jets MC (w/ bkgd.)",0.05,0,"",options.outDir)

    inputFile.Close()
    outputFile.Close()
    
def makeRatioPlot(num,den,histoname,title,numName,denName,ratioMax,ratioMin,opts,outDir):
    print num,den
    sys.stdout.flush()
    outputCanvas = r.TCanvas("output","output",600,600)
    outputCanvas.cd()
    plotPad  = r.TPad("plotPad", "plotPad",0.0,0.2,1.0,1.0)
    plotPad.SetFillStyle(4000)
    plotPad.SetFrameFillStyle(4000)
    plotPad.SetTopMargin(0.025)
    plotPad.SetBottomMargin(0.06)
    plotPad.SetLeftMargin(0.075)
    plotPad.SetRightMargin(0.05)

    ratioPad = r.TPad("ratioPad","ratioPad",0.0,0.0,1.0,0.2)
    ratioPad.SetFillStyle(4000)
    ratioPad.SetFrameFillStyle(4000)
    ratioPad.SetTopMargin(0.03)
    ratioPad.SetBottomMargin(0.1)
    ratioPad.SetLeftMargin(0.075)
    ratioPad.SetRightMargin(0.05)

    plotPad.Draw()
    plotPad.cd()

    leg = r.TLegend(0.1,0.1,0.6,0.3)
    leg.SetFillStyle(4000)
    leg.SetFillColor(r.kWhite)
    leg.SetTextFont(42)
    leg.SetHeader(title)
    leg.SetTextSize(0.03)

    maxVal = num.GetMaximum()
    if den.GetMaximum():
        maxVal = den.GetMaximum()

    
    num.GetXaxis().SetLabelSize(0.04)
    num.GetXaxis().SetLabelOffset(0.015)
    num.SetNdivisions(10)
    num.SetMaximum(1.15*maxVal)
    num.SetMinimum(0.01)
    num.SetStats(0)
    num.SetTitle("")
    num.SetLineColor(r.kRed)
    den.SetLineColor(r.kBlue)
    num.Draw("e1p0")
    den.Draw("e1p0sames")
    numErr = r.Double(0.)
    numVal = num.IntegralAndError(0,-1,numErr,"")
    denErr = r.Double(0.)
    denVal = den.IntegralAndError(0,-1,denErr,"")
    leg.AddEntry(num,"#splitline{%s}{(num:%2.2e#pm%2.2e)}"%(numName,numVal,numErr),"pel")
    leg.AddEntry(den,"#splitline{%s}{(den:%2.2e#pm%2.2e)}"%(denName,denVal,denErr),"pel")

    plotPad.SetGrid()
    outputCanvas.cd()
    ratioPad.Draw()
    ratioPad.cd()
    ratioHisto = num.Clone("%s"%(histoname))
    ratioHisto.Divide(num,den,1.0,1.0,opts)
    ratioHisto.SetLineColor(r.kBlack)
    ratioHisto.GetYaxis().SetNdivisions(205)
    ratioHisto.SetMaximum(ratioMax)
    ratioHisto.SetMinimum(ratioMin)
    ratioHisto.GetYaxis().SetLabelSize(0.125)
    ratioHisto.GetXaxis().SetLabelSize(0.)
    ratioHisto.Draw("e1p0")
    ratioPad.SetGrid()
    ratioHisto.Write()
    
    outputCanvas.cd()
    plotPad.cd()
    leg.Draw("same")
    #outputCanvas.SaveAs("%s/%s.pdf"%(outDir,histoname))
    #outputCanvas.SaveAs("%s/%s.png"%(outDir,histoname))
    outputCanvas.SaveAs("%s/%s.eps"%(outDir,histoname))
    plotPad.SetLogy(1)
    #outputCanvas.SaveAs("%s/%s_logy.pdf"%(outDir,histoname))
    #outputCanvas.SaveAs("%s/%s_logy.png"%(outDir,histoname))
    outputCanvas.SaveAs("%s/%s_logy.eps"%(outDir,histoname))
    #
    #
    #outputFile.Write()
####very end####
if __name__ == '__main__':
    main()
