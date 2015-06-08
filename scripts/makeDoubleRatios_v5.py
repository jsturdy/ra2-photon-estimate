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
    inputFile = r.TFile("%s/dataMCplots_%s_v4.root"%(options.outDir,sfSuffix),"READ")
    outputFile = r.TFile("%s/dataMCplots_%s_v5.root"%(options.outDir,sfSuffix),"RECREATE")
    
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
        denName = "photonsDataMC_%s"%(mbin[2])
        numName = "dimuonsDataMC_%s"%(mbin[2])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        makeDoubleRatioPlot(num,den,"doubleDataMC_%s"%(mbin[2]),
                            mbin[3],"Z#rightarrow#mu#mu+Jets Data/MC","#gamma+Jets Data/MC",1.5,0.5,"",
                            options.outDir)
        
        numName = "zmumuGammaData_ratio_%s"%(mbin[2])
        denName = "zmumuGammaMCwBKGD_ratio_%s"%(mbin[2])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        makeDoubleRatioPlot(num,den,"doubleDataMC_total_bkgd_%s"%(mbin[2]),
                            mbin[3],"Z/#gamma Data","Z/#gamma MC (bkgd. add.)",1.5,0.5,"",
                            options.outDir)
        
        numName = "zmumuGammaDataBkgdSub_ratio_%s"%(mbin[2])
        denName = "zmumuGammaMC_ratio_%s"%(mbin[2])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        makeDoubleRatioPlot(num,den,"doubleDataMC_bkgd_sub_%s"%(mbin[2]),
                            mbin[3],"Z/#gamma Data (bkgd. sub.)","Z/#gamma MC (signal)",1.5,0.5,"",
                            options.outDir)
        
        
    for j,njetbin in enumerate(histoNames):
        denName = "photonsDataMC_HT_%s"%(njetbin[0])
        numName = "dimuonsDataMC_HT_%s"%(njetbin[0])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        print num,den
        sys.stdout.flush()
        makeDoubleRatioPlot(num,den,"doubleDataMC_HT_%s"%(njetbin[0]),
                            njetbin[1],"Z#rightarrow#mu#mu+Jets Data/MC","#gamma+Jets Data/MC",1.5,0.5,"",
                            options.outDir)
        
        numName = "zmumuGammaData_ratio_HT_%s"%(njetbin[0])
        denName = "zmumuGammaMCwBKGD_ratio_HT_%s"%(njetbin[0])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        print num,den
        sys.stdout.flush()
        makeDoubleRatioPlot(num,den,"doubleDataMC_total_bkgd_HT_%s"%(njetbin[0]),
                            njetbin[1],"Z/#gamma Data","Z/#gamma MC (bkgd. add.)",1.5,0.5,"",
                            options.outDir)
        
        numName = "zmumuGammaDataBkgdSub_ratio_HT_%s"%(njetbin[0])
        denName = "zmumuGammaMC_ratio_HT_%s"%(njetbin[0])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        print num,den
        sys.stdout.flush()
        makeDoubleRatioPlot(num,den,"doubleDataMC_bkgd_sub_HT_%s"%(njetbin[0]),
                            njetbin[1],"Z/#gamma Data (bkgd. sub.)","Z/#gamma MC (signal)",1.5,0.5,"",
                            options.outDir)
        
    for j,njetbin in enumerate(histoNames):
        denName = "photonsDataMC_MHT_%s"%(njetbin[0])
        numName = "dimuonsDataMC_MHT_%s"%(njetbin[0])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        print num,den
        sys.stdout.flush()
        makeDoubleRatioPlot(num,den,"doubleDataMC_MHT_%s"%(njetbin[0]),
                            njetbin[1],"Z#rightarrow#mu#mu+Jets Data/MC","#gamma+Jets Data/MC",1.5,0.5,"",
                            options.outDir)
        
        numName = "zmumuGammaData_ratio_MHT_%s"%(njetbin[0])
        denName = "zmumuGammaMCwBKGD_ratio_MHT_%s"%(njetbin[0])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        print num,den
        sys.stdout.flush()
        makeDoubleRatioPlot(num,den,"doubleDataMC_total_bkgd_MHT_%s"%(njetbin[0]),
                            njetbin[1],"Z/#gamma Data","Z/#gamma MC (bkgd. add.)",1.5,0.5,"",
                            options.outDir)
        
        numName = "zmumuGammaDataBkgdSub_ratio_MHT_%s"%(njetbin[0])
        denName = "zmumuGammaMC_ratio_MHT_%s"%(njetbin[0])
        num = inputFile.Get(numName)
        den = inputFile.Get(denName)
        print num,den
        sys.stdout.flush()
        makeDoubleRatioPlot(num,den,"doubleDataMC_bkgd_sub_MHT_%s"%(njetbin[0]),
                            njetbin[1],"Z/#gamma Data (bkgd. sub.)","Z/#gamma MC (signal)",1.5,0.5,"",
                            options.outDir)
        
        
    inputFile.Close()
    outputFile.Close()
    
def makeDoubleRatioPlot(num,den,histoname,title,numName,denName,ratioMax,ratioMin,opts,outDir):
    #print [num,den,histoname,title,numName,denName,ratioMax,ratioMin]
    outputCanvas = r.TCanvas("output%s"%(histoname),"output",600,600)
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
    num.GetYaxis().SetLabelSize(0.035)
    num.SetNdivisions(10)
    num.GetYaxis().SetNdivisions(210)
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
    leg.Draw("same")
    outputCanvas.cd()
    ratioPad.Draw()
    ratioPad.cd()
    ratioHisto = num.Clone("%s"%(histoname))
    ratioHisto.Divide(num,den,1.0,1.0,opts)
    ratioHisto.SetLineColor(r.kBlack)
    ratioHisto.GetYaxis().SetNdivisions(205)
    ratioHisto.SetMaximum(ratioMax)
    ratioHisto.SetMinimum(ratioMin)
    ratioHisto.Write()
    ratioHisto.GetYaxis().SetLabelSize(0.15)
    ratioHisto.GetXaxis().SetLabelSize(0.)
    ratioHisto.Draw("e1p0")
    ratioPad.SetGrid()
    
    outputCanvas.cd()
    ratioPad.Draw()
    ratioPad.cd()
    ratioHisto.Draw("e1p0")
    outputCanvas.SaveAs("%s/%s.pdf"%(outDir,histoname))
    outputCanvas.SaveAs("%s/%s.png"%(outDir,histoname))
    outputCanvas.SaveAs("%s/%s.eps"%(outDir,histoname))

####very end####
if __name__ == '__main__':
    main()
