import sys,os
import ROOT as r
from array import array
import math,itertools
import optparse
from specialFunctions import mkdir_p

########Main
def main() :
    parser = optparse.OptionParser(description="Driver parameters for makeGenRatioPlots.py")
    parser.add_option('-d', '--debug',   action="store_true", default=False, dest="debug")
    parser.add_option('-z', '--zmumuMC', action="store_true", default=False, dest="zmumuMC")
    parser.add_option('-l', '--lepVeto', action="store_true", default=False, dest="lepVeto")
    parser.add_option('-n', '--name',    type='string', action="store", default="ZGammaRatio_pt100_dr0.0_reco_plots_inclusivejet_full", dest="name")
    parser.add_option('-o', '--outDir',  type='string', action="store", default="/tmp", dest="outDir")
    parser.add_option('-i', '--inDir',   type='string', action="store", default="/media/btrfs/research/BackgroundStudies/ZInvisible/Photons/15.03.2013", dest="inDir")
    parser.add_option('-g', '--genreco', action="store_true", default=False, dest="genreco")
    parser.add_option('-f', '--fitbins', type='int', action="store",      default=0,     dest="fitBins")
    parser.add_option('-r', '--fitrange',type='int', action="store",      default=2,     dest="fitRange")
    
    options, args = parser.parse_args()
    
    r.gROOT.SetBatch(True)
    mkdir_p("%s"%(options.outDir))
  
    goodFitBins = [0,1,2,3,4,5,6]
    myFitBin = options.fitBins
    if options.fitBins not in goodFitBins:
        print "invalid option for fit bins, using default 0"
        myFitBin = 0
    myWorkingDir = os.getcwd()

    inFileName = "ZGammaRatio_pt100_dr0.0_reco_plots_inclusivejet_full"

    totalLumi = 19.371
    topText = "CMS Preliminary"
    topMCText = "CMS Simulation"
    bottomText = "#bf{L} = %2.1f fb^{-1}, #sqrt{s} = 8 TeV"%(19.5)
    bottomMCText = "#sqrt{s} = 8 TeV"

    extra = "zmumuGammaData"
    if options.zmumuMC:
        extra = "zmumuGammaMC"

    lepVetoExtr = "noLepVeto"
    if options.lepVeto:
        lepVetoExtr = "withLepVeto"
        
    print "%s/dataMCplots_new_v5.root"%(options.inDir)
    doubleFitFile = r.TFile("%s/dataMCplots_new_v5.root"%(options.inDir),"READ")

    if options.genreco:
        inputFile   = r.TFile("%s/ZGammaRatio_gen_plots_full.root"%(options.inDir),"READ")
        dataFitFile = r.TFile("%s/dataMCplots_new_v4.root"%(options.inDir),"READ")
        efficiencyFile = r.TFile("%s/GJets_efficiency_plots_full.root"%(options.inDir),"READ")
        outputFile = r.TFile("%s/gen_fits_%dto8_bin%d_new_%s.root"%(options.outDir,options.fitRange,myFitBin,extra),"RECREATE")
    else:
        inputFile   = r.TFile("%s/ZGammaRatio_reco_plots_full.root"%(options.inDir),"READ")
        dataFitFile = r.TFile("%s/dataMCplots_new_v4.root"%(options.inDir),"READ")
        efficiencyFile = r.TFile("%s/ZGammaRatio_reco_plots_full.root"%(options.inDir),"READ")
        outputFile = r.TFile("%s/reco_fits_%dto8_bin%d_new_%s.root"%(options.outDir,options.fitRange,myFitBin,extra),"RECREATE")

    purityInputFile = r.TFile("%s/purityTemplates.root"%(options.inDir),"READ")

    purityFunction    = {}
    purityFunction["barrel"] = purityInputFile.Get("barrelPurityVsNJets_MHT200toInfGraph")
    purityFunction["endcap"] = purityInputFile.Get("endcapPurityVsNJets_MHT200toInfGraph")
    purityErrFunction = {}
    purityErrFunction["barrel"] = {}
    purityErrFunction["barrel"]["stat"] = {}
    purityErrFunction["barrel"]["syst"] = {}
    purityErrFunction["barrel"]["stat"]["UP"] = purityInputFile.Get("barrelPurityVsNJets_MHT200toInfGraphStatUP")
    purityErrFunction["barrel"]["stat"]["DN"] = purityInputFile.Get("barrelPurityVsNJets_MHT200toInfGraphStatDN")
    purityErrFunction["barrel"]["syst"]["UP"] = purityInputFile.Get("barrelPurityVsNJets_MHT200toInfGraphSystUP")
    purityErrFunction["barrel"]["syst"]["DN"] = purityInputFile.Get("barrelPurityVsNJets_MHT200toInfGraphSystDN")

    purityErrFunction["endcap"] = {}
    purityErrFunction["endcap"]["stat"] = {}
    purityErrFunction["endcap"]["syst"] = {}
    purityErrFunction["endcap"]["stat"]["UP"] = purityInputFile.Get("endcapPurityVsNJets_MHT200toInfGraphStatUP")
    purityErrFunction["endcap"]["stat"]["DN"] = purityInputFile.Get("endcapPurityVsNJets_MHT200toInfGraphStatDN")
    purityErrFunction["endcap"]["syst"]["UP"] = purityInputFile.Get("endcapPurityVsNJets_MHT200toInfGraphSystUP")
    purityErrFunction["endcap"]["syst"]["DN"] = purityInputFile.Get("endcapPurityVsNJets_MHT200toInfGraphSystDN")

        
    print inputFile
    print efficiencyFile
    print doubleFitFile
    print outputFile
    
    dirs = [
        ["nJetbin2to25",["mhtbin",100,5000,"Inf"],"bin32"],
        ["nJetbin2to25",["mhtbin",200,5000,"Inf"],"bin31"],
        ["nJetbin2to25",["mhtbin",100,200,"200"] ,"bin23"],
        ["nJetbin2to25",["mhtbin",200,300,"300"] ,"bin24"],
        ["nJetbin2to25",["mhtbin",300,450,"450"] ,"bin19"],
        ["nJetbin2to25",["mhtbin",450,5000,"Inf"],"bin21"],
        ]

    efficiencies = [
        ["acc",  "acceptance"],
        ["reco", "recotightid"],
        ["pixel","recotightidpixv"],
        ["iso",  "recotightidisopixv"],
        ]
        
    fitFunctions     = {}
    dataFitFunctions = {}
    doubleFitFunctions = {}

    plotCanvas = r.TCanvas("plotCanvas","",800,800)

    for dir in dirs:
        htdir = "htbin350to8000"
        mhtdir = "%s%dto%d"%(dir[1][0],dir[1][1],dir[1][2])

        directory = dir[0]+"_"+htdir+"_"+mhtdir
        print directory
        plotDir = inputFile.Get(directory)
        print plotDir
        plotDir.cd()
        inputFile.cd(directory)

        #####Phenomenological Ratio############
        ratioHisto = plotDir.Get("nJetsHT_ratio")
        fit = r.TF1("%s_fit"%(directory),"pol1",options.fitRange,8)
        fitFunction = r.TF1("%s_function"%(directory),"pol1",0,25)
        
        fitHisto = ratioHisto.Clone("pheno_nJetsHT_ratio_"+htdir+mhtdir)
        print "fitting pheno_nJetsHT_ratio %s"%(directory)
        sys.stdout.flush()
        ##"REMFSO+"
        #r.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2","minimize")
        result = ratioHisto.Fit(fit,"REMFSO+")
        #fitter = r.TVirtualFitter.GetFitter( r.TVirtualFitter() )        
        covm = result.GetCovarianceMatrix()
        corm = result.GetCorrelationMatrix()
        result.Print("V")
        chi2 = fit.GetChisquare()
        ndf  = fit.GetNDF()
        #chi2ndf = chi2/ndf
        p0   = fit.GetParameter(0)
        e0   = fit.GetParError(0)
        p1   = fit.GetParameter(1)
        e1   = fit.GetParError(1)        
        covp0p1 = covm[0][1]
        
        #print "**************************************************************"
        #print "* fit:p0(+/-dp0)  p1(+/-dp1)      chi2  ndf   chi2/ndf       *"
        #print "* %2.2e(%2.2e)    %2.2e(%2.2e)  %2.2e    %d     %2.2e   *"%(p0,e0,p1,e1,chi2,ndf,chi2ndf)
        #print "*                                                            *"
        #print "* fit parameter covariance matrix                            *"
        #print "* -------------     -------------                            *"
        #print "* |p0p0 |p1p0 |     |%2.2e|%2.2e|                     *"%(covm[0][0],covm[0][1])
        #print "* |-----|------     |-----|------                            *"
        #print "* |p0p1 |p1p1 |     |%2.2e|%2.2e|                     *"%(covm[1][0],covm[1][1])
        #print "* -------------     -------------                            *"
        #print "* fit parameter correlation matrix                           *"
        #print "* -------------     -------------                            *"
        #print "* |p0p0 |p1p0 |     |%2.2e|%2.2e|                     *"%(corm[0][0],corm[0][1])
        #print "* |-----|------     |-----|------                            *"
        #print "* |p0p1 |p1p1 |     |%2.2e|%2.2e|                     *"%(corm[1][0],corm[1][1])
        #print "* -------------     -------------                            *"
        #print "**************************************************************"
        #sys.stdout.flush()
        ##raw_input("Press Enter to continue...")
        
        fitFunction.SetParameter(0,p0)
        fitFunction.SetParError(0,e0)
        fitFunction.SetParameter(1,p1)
        fitFunction.SetParError(1,e1)
        fitFunction.SetLineColor(r.kRed)
        fitFunction.SetLineStyle(1)
        fitFunction.SetLineWidth(2)

        plotCanvas.cd()
        yVals = makeNJetErrorBands(25,0,fitFunction,covp0p1)
        xBins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
        pol1FitCorrUP   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["UP"]["raw"]))
        pol1FitCorrDN   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["DN"]["raw"]))
        pol1FitCorrUP.SetLineColor(r.kBlue)
        pol1FitCorrDN.SetLineColor(r.kBlue)
        pol1FitCorrUP.SetLineWidth(2)
        pol1FitCorrDN.SetLineWidth(2)
        pol1FitCorrUP.SetName("%s_fitPol1_PhenoCorrUP"%(directory))
        pol1FitCorrDN.SetName("%s_fitPol1_PhenoCorrDN"%(directory))
        pol1FitUncUP   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncUP"]["raw"]))
        pol1FitUncDN   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncDN"]["raw"]))
        pol1FitUncUP.SetLineColor(r.kMagenta+3)
        pol1FitUncDN.SetLineColor(r.kMagenta+3)
        pol1FitUncUP.SetLineWidth(2)
        pol1FitUncDN.SetLineWidth(2)
        pol1FitUncUP.SetName("%s_fitPol1_PhenoUncUP"%(directory))
        pol1FitUncDN.SetName("%s_fitPol1_PhenoUncDN"%(directory))

        fitHisto.GetXaxis().SetRangeUser(0,8)
        fitHisto.SetNdivisions(10)
        #fitHisto.SetMaximum(max(pol1FitUncUP.Eval(-3),pol1FitUncUP.Eval(15)))
        #fitHisto.SetMinimum(min(pol1FitUncDN.Eval(-3),pol1FitUncDN.Eval(15)))
        fitHisto.SetMaximum(0.5)
        fitHisto.SetMinimum(0.0)
        fitHisto.SetLineColor(r.kBlack)
        fitHisto.SetLineWidth(2)
        fitHisto.SetMarkerColor(r.kBlack)
        fitHisto.GetXaxis().SetNdivisions(10)
        fitHisto.GetYaxis().SetNdivisions(520)
        #fitHisto.GetYaxis().SetNdivisions(210)
        fitHisto.Draw("e1p0")
        plotCanvas.SetGridx()
        plotCanvas.SetGridy()

        fitStats = r.TPaveText(0.6,0.7,0.9,0.9)
        fitStats.ConvertNDCtoPad()
        fitStats.SetX1NDC(0.6)
        fitStats.SetX2NDC(0.9)
        fitStats.SetY1NDC(0.7)
        fitStats.SetY2NDC(0.9)
        fitStats.SetFillStyle(0)
        fitStats.AddText("#chi^{2}/ndf = %2.4f(%2.4f/%d)"%(chi2/ndf,chi2,ndf))
        fitStats.AddText("p_{0} = %2.4f #pm %2.4f"%(p0,e0))
        fitStats.AddText("p_{1} = %2.4f #pm %2.4f"%(p1,e1))
        fitStats.AddText("Cov[p0,p1] = %2.4f"%(covp0p1))

        fitFunction.Draw("same")
        fitStats.Draw("same")
        pol1FitCorrUP.Draw("same")
        pol1FitCorrDN.Draw("same")
        ###pol1FitUncUP.Draw("same")
        ###pol1FitUncDN.Draw("same")
        #raw_input("Press Enter to continue...")
        plotCanvas.SaveAs("%s/%s_fitPol1_pheno_can.eps"%(options.outDir,directory))

        fitFunctions[dir[2]] = {"pheno":{"func":fitFunction,"cov":covp0p1,
                                         "corrUP":pol1FitCorrUP,"corrDN":pol1FitCorrDN,
                                         "uncUP" :pol1FitUncUP ,"uncDN" :pol1FitUncDN},
                                "htBins":[350,8000],"mhtBins":[dir[1][1],dir[1][2]]}
        
        outputFile.cd()
        fitHisto.Write()
        fitFunction.Write()
        pol1FitCorrUP.Write()
        pol1FitCorrDN.Write()
        pol1FitUncUP.Write()
        pol1FitUncDN.Write()

        ######Double Ratio###########
        ## Treatment of the double ratio measured in data, perform a fit on the ratio
        ## in data or in simulation, obtain the uncertainty from this, and correct for
        ## disagreement between data and MC by and additional scale factor
        ratioHisto = dataFitFile.Get("zmumuGammaDataBkgdSub_ratio_%dto%s"%(dir[1][1],dir[1][3]))
        if options.zmumuMC:
            ratioHisto = dataFitFile.Get("zmumuGammaMC_ratio_%dto%s"%(dir[1][1],dir[1][3]))

        print "zmumuGammaDataBkgdSub_ratio_%dto%s"%(dir[1][1],dir[1][3])
        print "zmumuGammaMC_ratio_%dto%s"%(dir[1][1],dir[1][3])
        print "data ratio histo:: ",ratioHisto
        sys.stdout.flush()
        fit = r.TF1("%s_fit"%(directory),"pol1",options.fitRange,8)
        fitFunction = r.TF1("%s_function_data"%(directory),"pol1",0,25)
        
        print "fitting zmumugamma_nJetsHT_ratio %s"%(directory)
        sys.stdout.flush()
        fitHisto = ratioHisto.Clone("zmumugamma_nJetsHT_ratio_"+htdir+mhtdir)
        #print "fitting zmumugamma_nJetsHT_ratio %s"%(directory)
        #sys.stdout.flush()
        #r.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2","minimize")
        result = ratioHisto.Fit(fit,"REMFSO+")
        #fitter = r.TVirtualFitter.GetFitter( r.TVirtualFitter() )        
        covm = result.GetCovarianceMatrix()
        corm = result.GetCorrelationMatrix()
        result.Print("V")
        
        chi2 = fit.GetChisquare()
        ndf  = fit.GetNDF()
        #chi2ndf = chi2/ndf
        p0   = fit.GetParameter(0)
        e0   = fit.GetParError(0)
        p1   = fit.GetParameter(1)
        e1   = fit.GetParError(1)        
        covp0p1 = covm[0][1]

        fitFunction.SetParameter(0,p0)
        fitFunction.SetParError(0,e0)
        fitFunction.SetParameter(1,p1)
        fitFunction.SetParError(1,e1)
        fitFunction.SetLineColor(r.kRed)
        fitFunction.SetLineStyle(1)
        fitFunction.SetLineWidth(2)

        yVals = makeNJetErrorBands(25,0,fitFunction,covp0p1)
        xBins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
        pol1FitCorrUP   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["UP"]["raw"]))
        pol1FitCorrDN   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["DN"]["raw"]))
        pol1FitCorrUP.SetLineColor(r.kBlue)
        pol1FitCorrDN.SetLineColor(r.kBlue)
        pol1FitCorrUP.SetLineWidth(2)
        pol1FitCorrDN.SetLineWidth(2)
        pol1FitCorrUP.SetName("%s_fitPol1_TheoryCorrUP"%(directory))
        pol1FitCorrDN.SetName("%s_fitPol1_TheoryCorrDN"%(directory))
        pol1FitUncUP   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncUP"]["raw"]))
        pol1FitUncDN   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncDN"]["raw"]))
        pol1FitUncUP.SetLineColor(r.kMagenta+3)
        pol1FitUncDN.SetLineColor(r.kMagenta+3)
        pol1FitUncUP.SetLineWidth(2)
        pol1FitUncDN.SetLineWidth(2)
        pol1FitUncUP.SetName("%s_fitPol1_TheoryUncUP"%(directory))
        pol1FitUncDN.SetName("%s_fitPol1_TheoryUncDN"%(directory))

        fitHisto.GetXaxis().SetRangeUser(0,8)
        fitHisto.SetNdivisions(10)
        fitHisto.SetMaximum(max(pol1FitUncUP.Eval(-3),pol1FitUncUP.Eval(15)))
        fitHisto.SetMinimum(min(pol1FitUncDN.Eval(-3),pol1FitUncDN.Eval(15)))
        fitHisto.SetLineColor(r.kBlack)
        fitHisto.SetLineWidth(2)
        fitHisto.SetMarkerColor(r.kBlack)
        fitHisto.GetXaxis().SetNdivisions(10)
        fitHisto.GetYaxis().SetNdivisions(520)
        #fitHisto.GetYaxis().SetNdivisions(210)
        fitHisto.Draw("e1p0")
        plotCanvas.SetGridx()
        plotCanvas.SetGridy()

        fitStats.Clear()
        fitStats.AddText("#chi^{2}/ndf = %2.4f(%2.4f/%d)"%(chi2/ndf,chi2,ndf))
        fitStats.AddText("p_{0} = %2.4f #pm %2.4f"%(p0,e0))
        fitStats.AddText("p_{1} = %2.4f #pm %2.4f"%(p1,e1))
        fitStats.AddText("Cov[p0,p1] = %2.4f"%(covp0p1))
        fitFunction.Draw("same")
        fitStats.Draw("same")
        pol1FitCorrUP.Draw("same")
        pol1FitCorrDN.Draw("same")
        ##pol1FitUncUP.Draw("same")
        ##pol1FitUncDN.Draw("same")
        #raw_input("Press Enter to continue...")
        plotCanvas.SaveAs("%s/%s_fitPol1_theory_can.eps"%(options.outDir,directory))

        dataFitFunctions[dir[2]] = {"pheno":{"func":fitFunction,"cov":covp0p1,
                                             "corrUP":pol1FitCorrUP,"corrDN":pol1FitCorrDN,
                                             "uncUP" :pol1FitUncUP ,"uncDN" :pol1FitUncDN},
                                    "htBins":[350,8000],"mhtBins":[dir[1][1],dir[1][2]]}
        
        outputFile.cd()
        fitHisto.Write()
        fitFunction.Write()
        pol1FitCorrUP.Write()
        pol1FitCorrDN.Write()
        pol1FitUncUP.Write()
        pol1FitUncDN.Write()

        #######fits on double ratio###########
        plotCanvas.cd()
        print "trying to get doubleDataMC_bkgd_sub_%dto%s"%(dir[1][1],dir[1][3])
        ratioHisto = doubleFitFile.Get("doubleDataMC_bkgd_sub_%dto%s"%(dir[1][1],dir[1][3]))
        print "double ratio histo:: ",ratioHisto
        sys.stdout.flush()
        fitPol0 = r.TF1("%s_fitPol0"%(directory),"pol0",options.fitRange,8)
        #fitPol0.FixParameter(0,1.0)
        fitFunctionPol0 = r.TF1("%s_function_double_pol0"%(directory),"pol0",0,25)
        fitPol1 = r.TF1("%s_fitPol1"%(directory),"pol1",options.fitRange,8)
        #fitPol1.FixParameter(0,1.0)
        fitFunctionPol1 = r.TF1("%s_function_double_pol1"%(directory),"pol1",0,25)

        ratioHisto.Draw("e1p0")
        fitHisto = ratioHisto.Clone("zmumugamma_nJetsHT_doubleratio_"+htdir+mhtdir)
        print "fitting zmumugamma_nJetsHT_doubleratio pol1 %s"%(directory)
        sys.stdout.flush()
        #r.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2","minimize")
        result = ratioHisto.Fit(fitPol1,"REMFSO+")
        #fitter = r.TVirtualFitter.GetFitter( r.TVirtualFitter() )        
        covm = result.GetCovarianceMatrix()
        corm = result.GetCorrelationMatrix()
        result.Print("V")
        
        chi2 = fitPol1.GetChisquare()
        ndf  = fitPol1.GetNDF()
        #chi2ndf = chi2/ndf
        p0   = fitPol1.GetParameter(0)
        e0   = fitPol1.GetParError(0)
        p1   = fitPol1.GetParameter(1)
        e1   = fitPol1.GetParError(1)        
        covp0p1 = covm[0][1]
        print p0,e0,p1,e1,covp0p1,chi2,ndf
        fitFunctionPol1.SetParameter(0,p0)
        fitFunctionPol1.SetParError(0,e0)
        fitFunctionPol1.SetParameter(1,p1)
        fitFunctionPol1.SetParError(1,e1)
        fitFunctionPol1.SetLineColor(r.kRed)
        fitFunctionPol1.SetLineStyle(1)
        fitFunctionPol1.SetLineWidth(2)
        #pol0FitUncUP   = r.TGraphAsymmErrors()
        #pol0FitUncDN   = r.TGraphAsymmErrors()
        yVals = makeNJetErrorBands(25,1,fitFunctionPol1,covp0p1)
        #xBins = [-0.5,0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]
        xBins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
        pol1FitCorrUP    = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["UP"]["raw"]))
        pol1FitCorrDN    = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["DN"]["raw"]))
        pol1FitCorrSymUP = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["UP"]["sym"]))
        pol1FitCorrSymDN = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["DN"]["sym"]))
        pol1FitCorrUP.SetLineColor(r.kBlue)
        pol1FitCorrDN.SetLineColor(r.kBlue)
        pol1FitCorrUP.SetLineWidth(2)
        pol1FitCorrDN.SetLineWidth(2)
        pol1FitCorrSymUP.SetLineColor(r.kBlue)
        pol1FitCorrSymDN.SetLineColor(r.kBlue)
        pol1FitCorrSymUP.SetLineWidth(2)
        pol1FitCorrSymDN.SetLineWidth(2)
        pol1FitCorrSymUP.SetLineStyle(2)
        pol1FitCorrSymDN.SetLineStyle(2)
        pol1FitCorrUP.SetName("%s_fitPol1_DoubleCorrUP"%(directory))
        pol1FitCorrDN.SetName("%s_fitPol1_DoubleCorrDN"%(directory))
        pol1FitCorrSymUP.SetName("%s_fitPol1_DoubleCorrSymUP"%(directory))
        pol1FitCorrSymDN.SetName("%s_fitPol1_DoubleCorrSymDN"%(directory))

        pol1FitUncUP    = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncUP"]["raw"]))
        pol1FitUncDN    = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncDN"]["raw"]))
        pol1FitUncSymUP = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncUP"]["sym"]))
        pol1FitUncSymDN = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncDN"]["sym"]))
        pol1FitUncUP.SetLineColor(r.kMagenta+3)
        pol1FitUncDN.SetLineColor(r.kMagenta+3)
        pol1FitUncUP.SetLineWidth(2)
        pol1FitUncDN.SetLineWidth(2)
        pol1FitUncSymUP.SetLineColor(r.kMagenta+3)
        pol1FitUncSymDN.SetLineColor(r.kMagenta+3)
        pol1FitUncSymUP.SetLineWidth(2)
        pol1FitUncSymDN.SetLineWidth(2)
        pol1FitUncSymUP.SetLineStyle(2)
        pol1FitUncSymDN.SetLineStyle(2)
        pol1FitUncUP.SetName("%s_fitPol1_DoubleUncUP"%(directory))
        pol1FitUncDN.SetName("%s_fitPol1_DoubleUncDN"%(directory))
        pol1FitUncSymUP.SetName("%s_fitPol1_DoubleUncSymUP"%(directory))
        pol1FitUncSymDN.SetName("%s_fitPol1_DoubleUncSymDN"%(directory))

        #if mhtdir in ["mhtbin100to5000","mhtbin200to5000"]:
        fitHisto.SetMaximum(3.0)
        fitHisto.SetMinimum(-1.0)
        fitHisto.SetLineColor(r.kBlack)
        fitHisto.SetLineWidth(2)
        fitHisto.SetMarkerColor(r.kBlack)
        fitHisto.GetXaxis().SetRangeUser(0,8)
        fitHisto.GetXaxis().SetNdivisions(10)
        fitHisto.GetYaxis().SetNdivisions(520)
        fitHisto.Draw("e1p0")
        plotCanvas.SetGridx()
        plotCanvas.SetGridy()
        fitStats.Clear()
        fitStats.AddText("#chi^{2}/ndf = %2.4f(%2.4f/%d)"%(chi2/ndf,chi2,ndf))
        fitStats.AddText("p_{0} = %2.4f #pm %2.4f"%(p0,e0))
        fitStats.AddText("p_{1} = %2.4f #pm %2.4f"%(p1,e1))
        fitStats.AddText("Cov[p0,p1] = %2.4f"%(covp0p1))
        fitFunctionPol1.Draw("same")
        fitStats.Draw("same")
        pol1FitCorrUP.Draw("same")
        pol1FitCorrDN.Draw("same")
        #pol1FitCorrSymUP.Draw("same")
        #pol1FitCorrSymDN.Draw("same")

        plotCanvas.SaveAs("%s/%s_fitPol1_double_can.eps"%(options.outDir,directory))

        plotCanvas.Clear()
        plotCanvas.cd()
        plotCanvas.SetTicks(1,1)
        plotCanvas.SetLeftMargin(0.15)
        plotCanvas.SetRightMargin(0.05)
        plotCanvas.SetBottomMargin(0.15)
        fitHisto.SetMaximum(2.0)
        fitHisto.SetMinimum(0.0)
        fitHisto.Draw("e1p0")
        fitHisto.SetYTitle("Z(#rightarrow#mu#mu)/#gamma #frac{Data}{Sim.}")
        fitHisto.SetXTitle("N_{Jets}")
        fitHisto.GetXaxis().SetTitleOffset(1.5)
        fitHisto.GetYaxis().SetTitleOffset(1.4)
        fitFunctionPol1.Draw("same")
        pol1FitCorrUP.Draw("same")
        pol1FitCorrDN.Draw("same")
        plotCanvas.SetGridx(0)
        plotCanvas.SetGridy(0)
        plotCanvas.cd()
        latexLabel = r.TPaveText(0.,2.1,0.9,2.3)
        latexLabel.SetTextSize(0.035)
        latexLabel.SetTextAlign(13)
        latexLabel.SetTextColor(1)
        latexText = "#splitline{%s}{%s}"%(topText,bottomText)
        latexLabel.SetFillColor(0)
        latexLabel.SetFillStyle(0)
        latexLabel.SetBorderSize(0)
        mhtlabelname = "%d<#slashH_{T}<%d"%(dir[1][1],dir[1][2])
        if dir[1][2]>1000:
            mhtlabelname = "#slashH_{T}>%d"%(dir[1][1])
            
        latexLabel.AddText(topText+" "+bottomText)
        latexLabel.AddText("H_{T}>500, %s"%(mhtlabelname))
        #latexLabel.AddText(bottomText)
        latexLabel.SetX1NDC(0.15)
        latexLabel.SetX2NDC(0.6)
        latexLabel.SetY1NDC(0.8)
        latexLabel.SetY2NDC(0.9)
        ##latexLabel.ConvertNDCtoPad()
        latexLabel.Draw()
        plotCanvas.SaveAs("%s/%s_fitPol1_double_can_pas.eps"%(options.outDir,directory))
        plotCanvas.SaveAs("%s/%s_fitPol1_double_can_pas.C"%(options.outDir,directory))
        print "fitting zmumugamma_nJetsHT_doubleratio pol0 %s"%(directory)
        sys.stdout.flush()

        ##fit the pol0
        #r.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2","minimize")
        result = ratioHisto.Fit(fitPol0,"REMFSO+")
        #fitter = r.TVirtualFitter.GetFitter( r.TVirtualFitter() )        
        #covm = fitter.GetCovarianceMatrix()
        result.Print("V")
        
        chi2 = fitPol0.GetChisquare()
        ndf  = fitPol0.GetNDF()
        #chi2ndf = chi2/ndf
        p0   = fitPol0.GetParameter(0)
        e0   = fitPol0.GetParError(0)
        p1   = fitPol0.GetParameter(1)
        e1   = fitPol0.GetParError(1)        
        fitFunctionPol0.SetParameter(0,p0)
        fitFunctionPol0.SetParError(0,e0)
        fitFunctionPol0.SetParameter(1,p1)
        fitFunctionPol0.SetParError(1,e1)
        fitFunctionPol0.SetLineColor(r.kOrange)
        fitFunctionPol0.SetLineStyle(1)
        fitFunctionPol0.SetLineWidth(2)

        #fitHisto.SetLineColor(r.kBlack)
        #fitHisto.SetLineWidth(2)
        #fitHisto.SetMarkerColor(r.kBlack)
        #if not(mhtdir in ["mhtbin100to5000","mhtbin200to5000"]):
        fitHisto.SetMaximum(3.0)
        fitHisto.SetMinimum(-1.0)
        fitHisto.SetLineColor(r.kBlack)
        fitHisto.SetLineWidth(2)
        fitHisto.SetMarkerColor(r.kBlack)
        fitHisto.GetXaxis().SetRangeUser(0,8)
        fitHisto.GetXaxis().SetNdivisions(10)
        fitHisto.GetYaxis().SetNdivisions(520)
        fitHisto.Draw("e1p0")
        plotCanvas.SetGridx()
        plotCanvas.SetGridy()
        
        fitStats.Clear()
        fitStats.AddText("#chi^{2}/ndf = %2.4f(%2.4f/%d)"%(chi2/ndf,chi2,ndf))
        fitStats.AddText("p_{0} = %2.4f #pm %2.4f"%(p0,e0))
        fitFunctionPol0.Draw("same")
        fitStats.Draw("same")
        ##pol1FitUncUP.Draw("same")
        ##pol1FitUncSymUP.Draw("same")
        ##pol1FitUncDN.Draw("same")
        ##pol1FitUncSymDN.Draw("same")
        #raw_input("Press Enter to continue...")
        plotCanvas.SaveAs("%s/%s_fitPol0_double_can.eps"%(options.outDir,directory))

        #doubleFitFunctions[dir[2]] = {"pol0":{"func":fitFunctionPol0,"cov":0.0},
        dataFitFunctions[dir[2]]["double"] = {"pol0":{"func":fitFunctionPol0,"cov":0.0},
                                              "pol1":{"func":fitFunctionPol1,"cov":covp0p1,
                                                      "corrUP"   :pol1FitCorrUP   ,"corrDN"   :pol1FitCorrDN,
                                                      "corrSymUP":pol1FitCorrSymUP,"corrSymDN":pol1FitCorrSymDN,
                                                      "uncUP"    :pol1FitUncUP    ,"uncDN"    :pol1FitUncDN,
                                                      "uncSymUP" :pol1FitUncSymUP ,"uncSymDN" :pol1FitUncSymDN}}
        #"htBins":[350,8000],"mhtBins":[dir[1][1],dir[1][2]]}
        
        outputFile.cd()
        fitHisto.Write()
        fitFunctionPol0.Write()
        fitFunctionPol1.Write()
        pol1FitCorrUP.Write()
        pol1FitCorrDN.Write()
        pol1FitUncUP.Write()
        pol1FitUncDN.Write()
        pol1FitCorrSymUP.Write()
        pol1FitCorrSymDN.Write()
        pol1FitUncSymUP.Write()
        pol1FitUncSymDN.Write()
######        
        if options.genreco:
            plotDir = efficiencyFile.Get(directory)
            print directory
            print plotDir
            sys.stdout.flush()

            plotDir.cd()
            efficiencyFile.cd(directory)
            for eff in efficiencies:
                ratioHisto = plotDir.Get("nJetsHT_%s_eff"%(eff[1]))
                effFit = r.TF1("%s_%s"%(directory,eff[0]),"pol1",options.fitRange,8)
                effFunction = r.TF1("%s_%s"%(directory,eff[1]),"pol1",0,25)
            
                effHisto = ratioHisto.Clone("%s_nJetsHT_%s%s"%(eff[0],htdir,mhtdir))
                print "fitting %s_nJetsHT %s"%(eff[0],directory)
                sys.stdout.flush()
                #r.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2","minimize")
                result = ratioHisto.Fit(effFit,"REMFSO+")
                #fitter = r.TVirtualFitter.GetFitter( r.TVirtualFitter() )        
                covm = result.GetCovarianceMatrix()
                corm = result.GetCorrelationMatrix()
                result.Print("V")
                
                chi2 = effFit.GetChisquare()
                ndf  = effFit.GetNDF()
                #chi2ndf = chi2/ndf
                p0   = effFit.GetParameter(0)
                e0   = effFit.GetParError(0)
                p1   = effFit.GetParameter(1)
                e1   = effFit.GetParError(1)        
                covp0p1 = covm[0][1]

                effFunction.SetParameter(0,p0)
                effFunction.SetParError(0,e0)
                effFunction.SetParameter(1,p1)
                effFunction.SetParError(1,e1)
                effFunction.SetLineColor(r.kRed)
                effFunction.SetLineStyle(1)
                effFunction.SetLineWidth(2)
                
                plotCanvas.cd()
                yVals = makeNJetErrorBands(25,0,effFunction,covp0p1)
                xBins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
                pol1FitCorrUP   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["UP"]["raw"]))
                pol1FitCorrDN   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["DN"]["raw"]))
                pol1FitCorrUP.SetLineColor(r.kBlue)
                pol1FitCorrDN.SetLineColor(r.kBlue)
                pol1FitCorrUP.SetLineWidth(2)
                pol1FitCorrDN.SetLineWidth(2)
                pol1FitCorrUP.SetName("%s_fitPol1_%sCorrUP"%(directory,eff[0]))
                pol1FitCorrDN.SetName("%s_fitPol1_%sCorrDN"%(directory,eff[0]))
                pol1FitUncUP   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncUP"]["raw"]))
                pol1FitUncDN   = r.TGraphAsymmErrors(25,array('d',xBins),array('d',yVals["uncDN"]["raw"]))
                pol1FitUncUP.SetLineColor(r.kMagenta+3)
                pol1FitUncDN.SetLineColor(r.kMagenta+3)
                pol1FitUncUP.SetLineWidth(2)
                pol1FitUncDN.SetLineWidth(2)
                pol1FitUncUP.SetName("%s_fitPol1_%sUncUP"%(directory,eff[0]))
                pol1FitUncDN.SetName("%s_fitPol1_%sUncDN"%(directory,eff[0]))
                
                effHisto.GetXaxis().SetRangeUser(0,8)
                effHisto.SetNdivisions(10)
                effHisto.SetMaximum(max(pol1FitUncUP.Eval(-3),pol1FitUncUP.Eval(15)))
                effHisto.SetMinimum(min(pol1FitUncDN.Eval(-3),pol1FitUncDN.Eval(15)))
                effHisto.SetLineColor(r.kBlack)
                effHisto.SetLineWidth(2)
                effHisto.SetMarkerColor(r.kBlack)
                effHisto.GetXaxis().SetNdivisions(10)
                effHisto.GetYaxis().SetNdivisions(520)
                # effHisto.GetYaxis().SetNdivisions(210)
                effHisto.Draw("e1p0")
                plotCanvas.SetGridx()
                plotCanvas.SetGridy()

                fitStats.Clear()
                fitStats.AddText("#chi^{2}/ndf = %2.4f(%2.4f/%d)"%(chi2/ndf,chi2,ndf))
                fitStats.AddText("p_{0} = %2.4f #pm %2.4f"%(p0,e0))
                fitStats.AddText("p_{1} = %2.4f #pm %2.4f"%(p1,e1))
                fitStats.AddText("Cov[p0,p1] = %2.4f"%(covp0p1))
                effFunction.Draw("same")
                fitStats.Draw("same")
                pol1FitCorrUP.Draw("same")
                pol1FitCorrDN.Draw("same")
                ##pol1FitUncUP.Draw("same")
                ##pol1FitUncDN.Draw("same")
                #raw_input("Press Enter to continue...")
                plotCanvas.SaveAs("%s/%s_fitPol1_%s_can.eps"%(options.outDir,directory,eff[0]))
                
                #fitFunctions[dir[2]]["%s"%(eff[0])] = {"func":effFunction,"cov":covp0p1}
                fitFunctions[dir[2]]["%s"%(eff[0])] = {"func":effFunction,"cov":covp0p1,
                                                       "corrUP":pol1FitCorrUP,"corrDN":pol1FitCorrDN,
                                                       "uncUP" :pol1FitUncUP ,"uncDN" :pol1FitUncDN}
                
                outputFile.cd()
                effHisto.Write()
                effFunction.Write()
                pol1FitCorrUP.Write()
                pol1FitCorrDN.Write()
                pol1FitUncUP.Write()
                pol1FitUncDN.Write()
                
            
    ##loop over events and perform prediction
    myChain = r.TChain("reco")
    myChain.Add("%s/recoTreeDR0.0_photon2012abcd.root"%(options.inDir))
    predictionTree = r.TTree('data', 'tree for prediction ')

    runNum    = array( 'i', [ 0 ] )
    eventNum  = array( 'i', [ 0 ] )
    lumiBlock = array( 'i', [ 0 ] )
    nJets     = array( 'i', [ 0 ] )
    nPhotons  = array( 'i', [ 0 ] )
    ht        = array( 'd', [ 0.] )
    mht       = array( 'd', [ 0.] )
    photonPt  = array( 'd', [ 0.] )
    photonEta = array( 'd', [ 0.] )
    photonMinDR = array( 'd', [ 0.] )
    scaleFactor   = array( 'd', [ 0.] )
    scaleFactorUP = array( 'd', [ 0.] )
    scaleFactorDN = array( 'd', [ 0.] )
    scaleFactorTotUP = array( 'd', [ 0.] )
    scaleFactorTotDN = array( 'd', [ 0.] )
    phenoFactor  = array( 'd', [ 0.] )
    phenoErr2UP    = array( 'd', [ 0.] )
    phenoErr2DN    = array( 'd', [ 0.] )
    scaleFactorPhenUP = array( 'd', [ 0.] )
    scaleFactorPhenDN = array( 'd', [ 0.] )
    theoryErr2UP   = array( 'd', [ 0.] )
    theoryErr2DN   = array( 'd', [ 0.] )
    scaleFactorThFitUP = array( 'd', [ 0.] )
    scaleFactorThFitDN = array( 'd', [ 0.] )
    phenoDataMC   = array( 'd', [ 0.] )
    phenoDataMCErr2UP   = array( 'd', [ 0.] )
    phenoDataMCErr2DN   = array( 'd', [ 0.] )
    scaleFactorThDoubleUP = array( 'd', [ 0.] )
    scaleFactorThDoubleDN = array( 'd', [ 0.] )
    scaleFactorThUP = array( 'd', [ 0.] )
    scaleFactorThDN = array( 'd', [ 0.] )
    scaleFactorPhenThUP = array( 'd', [ 0.] )
    scaleFactorPhenThDN = array( 'd', [ 0.] )
    accEff       = array( 'd', [ 0.] )
    accErr2UP      = array( 'd', [ 0.] )
    accErr2DN      = array( 'd', [ 0.] )
    scaleFactorAccUP = array( 'd', [ 0.] )
    scaleFactorAccDN = array( 'd', [ 0.] )
    recoEff      = array( 'd', [ 0.] )
    recoErr2UP     = array( 'd', [ 0.] )
    recoErr2DN     = array( 'd', [ 0.] )
    scaleFactorIDUP = array( 'd', [ 0.] )
    scaleFactorIDDN = array( 'd', [ 0.] )
    pixelEff     = array( 'd', [ 0.] )
    pixelErr2UP    = array( 'd', [ 0.] )
    pixelErr2DN    = array( 'd', [ 0.] )
    scaleFactorPixUP = array( 'd', [ 0.] )
    scaleFactorPixDN = array( 'd', [ 0.] )
    isoEff       = array( 'd', [ 0.] )
    isoErr2UP      = array( 'd', [ 0.] )
    isoErr2DN      = array( 'd', [ 0.] )
    scaleFactorIsoUP = array( 'd', [ 0.] )
    scaleFactorIsoDN = array( 'd', [ 0.] )
    purity       = array( 'd', [ 0.] )
    #purityErr2   = array( 'd', [ 0.] )
    purityErr2UP   = array( 'd', [ 0.] )
    purityErr2DN   = array( 'd', [ 0.] )
    scaleFactorPurUP = array( 'd', [ 0.] )
    scaleFactorPurDN = array( 'd', [ 0.] )
    datamcSF     = array( 'd', [ 0.] )
    datamcSFErr2 = array( 'd', [ 0.] )
    #datamcSFErr2UP = array( 'd', [ 0.] )
    #datamcSFErr2DN = array( 'd', [ 0.] )
    scaleFactorDMCSFUP = array( 'd', [ 0.] )
    scaleFactorDMCSFDN = array( 'd', [ 0.] )
    totalErr2    = array( 'd', [ 0.] )
    eventWeight  = array( 'd', [ 0.] )
    puWeight  = array( 'd', [ 0.] )
    
    predictionTree.Branch( 'runNum',    runNum,    'runNum/I' )
    predictionTree.Branch( 'eventNum',  eventNum,  'eventNum/I' )
    predictionTree.Branch( 'lumiBlock', lumiBlock, 'lumiBlock/I' )
    predictionTree.Branch( 'nJets',     nJets,     'nJets/I' )
    predictionTree.Branch( 'nPhotons',  nPhotons,  'nPhotons/I' )
    
    predictionTree.Branch( 'ht'          ,ht          ,'ht/D' )
    predictionTree.Branch( 'mht'         ,mht         ,'mht/D' )
    predictionTree.Branch( 'photonPt'    ,photonPt    ,'photonPt/D' )
    predictionTree.Branch( 'photonEta'   ,photonEta   ,'photonEta/D' )
    predictionTree.Branch( 'photonMinDR' ,photonMinDR ,'photonMinDR/D' )
    predictionTree.Branch( 'scaleFactor' ,scaleFactor ,'scaleFactor/D' )
    predictionTree.Branch( 'scaleFactorUP' ,scaleFactorUP ,'scaleFactorUP/D' )
    predictionTree.Branch( 'scaleFactorDN' ,scaleFactorDN ,'scaleFactorDN/D' )
    predictionTree.Branch( 'scaleFactorTotUP' ,scaleFactorTotUP ,'scaleFactorTotUP/D' )
    predictionTree.Branch( 'scaleFactorTotDN' ,scaleFactorTotDN ,'scaleFactorTotDN/D' )
    predictionTree.Branch( 'phenoFactor' ,phenoFactor ,'phenoFactor/D' )
    predictionTree.Branch( 'phenoErr2UP'   ,phenoErr2UP   ,'phenoErr2UP/D' )
    predictionTree.Branch( 'phenoErr2DN'   ,phenoErr2DN   ,'phenoErr2DN/D' )
    predictionTree.Branch( 'scaleFactorPhenUP' ,scaleFactorPhenUP ,'scaleFactorPhenUP/D' )
    predictionTree.Branch( 'scaleFactorPhenDN' ,scaleFactorPhenDN ,'scaleFactorPhenDN/D' )
    predictionTree.Branch( 'theoryErr2UP'  ,theoryErr2UP  ,'theoryErr2UP/D' )
    predictionTree.Branch( 'theoryErr2DN'  ,theoryErr2DN  ,'theoryErr2DN/D' )
    predictionTree.Branch( 'scaleFactorThFitUP' ,scaleFactorThFitUP ,'scaleFactorThFitUP/D' )
    predictionTree.Branch( 'scaleFactorThFitDN' ,scaleFactorThFitDN ,'scaleFactorThFitDN/D' )
    predictionTree.Branch( 'phenoDataMC'  ,phenoDataMC  ,'phenoDataMC/D' )
    predictionTree.Branch( 'phenoDataMCErr2UP'  ,phenoDataMCErr2UP  ,'phenoDataMCErr2UP/D' )
    predictionTree.Branch( 'phenoDataMCErr2DN'  ,phenoDataMCErr2DN  ,'phenoDataMCErr2DN/D' )
    predictionTree.Branch( 'scaleFactorThDoubleUP' ,scaleFactorThDoubleUP ,'scaleFactorThDoubleUP/D' )
    predictionTree.Branch( 'scaleFactorThDoubleDN' ,scaleFactorThDoubleDN ,'scaleFactorThDoubleDN/D' )
    predictionTree.Branch( 'scaleFactorThUP' ,scaleFactorThUP ,'scaleFactorThUP/D' )
    predictionTree.Branch( 'scaleFactorThDN' ,scaleFactorThDN ,'scaleFactorThDN/D' )
    predictionTree.Branch( 'scaleFactorPhenThUP' ,scaleFactorPhenThUP ,'scaleFactorPhenThUP/D' )
    predictionTree.Branch( 'scaleFactorPhenThDN' ,scaleFactorPhenThDN ,'scaleFactorPhenThDN/D' )
    predictionTree.Branch( 'accEff'      ,accEff      ,'accEff/D' )
    predictionTree.Branch( 'accErr2UP'     ,accErr2UP     ,'accErr2UP/D' )
    predictionTree.Branch( 'accErr2DN'     ,accErr2DN     ,'accErr2DN/D' )
    predictionTree.Branch( 'scaleFactorAccUP' ,scaleFactorAccUP ,'scaleFactorAccUP/D' )
    predictionTree.Branch( 'scaleFactorAccDN' ,scaleFactorAccDN ,'scaleFactorAccDN/D' )
    predictionTree.Branch( 'recoEff'     ,recoEff     ,'recoEff/D' )
    predictionTree.Branch( 'recoErr2UP'    ,recoErr2UP    ,'recoErr2UP/D' )
    predictionTree.Branch( 'recoErr2DN'    ,recoErr2DN    ,'recoErr2DN/D' )
    predictionTree.Branch( 'scaleFactorIDUP' ,scaleFactorIDUP ,'scaleFactorIDUP/D' )
    predictionTree.Branch( 'scaleFactorIDDN' ,scaleFactorIDDN ,'scaleFactorIDDN/D' )
    predictionTree.Branch( 'pixelEff'    ,pixelEff    ,'pixelEff/D' )
    predictionTree.Branch( 'pixelErr2UP'   ,pixelErr2UP   ,'pixelErr2UP/D' )
    predictionTree.Branch( 'pixelErr2DN'   ,pixelErr2DN   ,'pixelErr2DN/D' )
    predictionTree.Branch( 'scaleFactorPixUP' ,scaleFactorPixUP ,'scaleFactorPixUP/D' )
    predictionTree.Branch( 'scaleFactorPixDN' ,scaleFactorPixDN ,'scaleFactorPixDN/D' )
    predictionTree.Branch( 'isoEff'      ,isoEff      ,'isoEff/D' )
    predictionTree.Branch( 'isoErr2UP'     ,isoErr2UP     ,'isoErr2UP/D' )
    predictionTree.Branch( 'isoErr2DN'     ,isoErr2DN     ,'isoErr2DN/D' )
    predictionTree.Branch( 'scaleFactorIsoUP' ,scaleFactorIsoUP ,'scaleFactorIsoUP/D' )
    predictionTree.Branch( 'scaleFactorIsoDN' ,scaleFactorIsoDN ,'scaleFactorIsoDN/D' )
    predictionTree.Branch( 'purity'      ,purity      ,'purity/D' )
    #predictionTree.Branch( 'purityErr2'  ,purityErr2  ,'purityErr2/D' )
    predictionTree.Branch( 'purityErr2UP'  ,purityErr2UP  ,'purityErr2UP/D' )
    predictionTree.Branch( 'purityErr2DN'  ,purityErr2DN  ,'purityErr2DN/D' )
    predictionTree.Branch( 'scaleFactorPurUP' ,scaleFactorPurUP ,'scaleFactorPurUP/D' )
    predictionTree.Branch( 'scaleFactorPurDN' ,scaleFactorPurDN ,'scaleFactorPurDN/D' )
    predictionTree.Branch( 'datamcSF'    ,datamcSF    ,'datamcSF/D' )
    predictionTree.Branch( 'datamcSFErr2',datamcSFErr2,'datamcSFErr2/D' )
    #predictionTree.Branch( 'datamcSFErr2UP',datamcSFErr2UP,'datamcSFErr2UP/D' )
    #predictionTree.Branch( 'datamcSFErr2DN',datamcSFErr2DN,'datamcSFErr2DN/D' )
    predictionTree.Branch( 'scaleFactorDMCSFUP' ,scaleFactorDMCSFUP ,'scaleFactorDMCSFUP/D' )
    predictionTree.Branch( 'scaleFactorDMCSFDN' ,scaleFactorDMCSFDN ,'scaleFactorDMCSFDN/D' )
    predictionTree.Branch( 'totalErr2'   ,totalErr2   ,'totalErr2/D' )
    predictionTree.Branch( 'eventWeight' ,eventWeight ,'eventWeight/D' )
    predictionTree.Branch( 'puWeight' ,puWeight ,'puWeight/D' )
    
  ###Timing information
    decade  = 0
    century = 0
    tsw = r.TStopwatch()
    tenpcount = 1
    onepcount = 1
    
    
    nentries = myChain.GetEntries()
    print "nentries %d"%(nentries)
    sys.stdout.flush()
    i = 0
    for event in myChain:
        if (event.photonPt > 100 and event.photonIsTightIso and event.photonPixelVeto and event.dphi1>0.5 and event.dphi2>0.5 and event.dphi3>0.3 and event.nJetsHT>1):
            if (event.htVal<500 or (event.htVal<800 and event.mhtVal<200)):
                continue
            if not (event.passRA2ElVeto and event.passRA2MuVeto):
                continue
            
            if myFitBin == 0:
                if (event.mhtVal>100 and event.mhtVal<200):
                    ibin = "bin23"
                elif (event.mhtVal<300):
                    ibin = "bin24"
                elif (event.mhtVal<450):
                    ibin = "bin19"
                else:
                    ibin = "bin21"
            else:
                if (event.mhtVal>100 and event.mhtVal<125):
                    ibin = "bin1"
                elif (event.mhtVal>125 and event.mhtVal<150):
                    ibin = "bin2"
                elif (event.mhtVal>150 and event.mhtVal<175):
                    ibin = "bin3"
                elif (event.mhtVal>175 and event.mhtVal<200):
                    ibin = "bin4"
                elif (event.mhtVal>200 and event.mhtVal<225):
                    ibin = "bin5"
                elif (event.mhtVal>225 and event.mhtVal<250):
                    ibin = "bin6"
                elif (event.mhtVal>250 and event.mhtVal<275):
                    ibin = "bin7"
                elif (event.mhtVal>275 and event.mhtVal<300):
                    ibin = "bin8"
                    
                else:
                ##standard fine binning
                    if myFitBin == 1:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<425):
                            ibin = "bin13"
                        elif (event.mhtVal>425 and event.mhtVal<450):
                            ibin = "bin14"
                        elif (event.mhtVal>450 and event.mhtVal<500):
                            ibin = "bin15"
                        elif (event.mhtVal>500 and event.mhtVal<550):
                            ibin = "bin16"
                        elif (event.mhtVal>550 and event.mhtVal<600):
                            ibin = "bin17"
                        else:
                            ibin = "bin18"
                #####bin coarser for high mht 450-inf
                    elif myFitBin == 2:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<425):
                            ibin = "bin13"
                        elif (event.mhtVal>425 and event.mhtVal<450):
                            ibin = "bin14"
                        else:
                            ibin = "bin21"
                #####bin coarser for high mht 400-450-inf
                    elif myFitBin == 3:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<450):
                            ibin = "bin27"
                        else:
                            ibin = "bin21"
                #####bin coarser for high mht 300-450-600-inf
                    elif myFitBin == 4:
                        if(event.mhtVal>300 and event.mhtVal<450):
                            ibin = "bin19"
                        elif(event.mhtVal>450 and event.mhtVal<600):
                            ibin = "bin20"
                        else:
                            ibin = "bin18"
                ###bin coarser for high mht 300-450-inf
                    elif myFitBin == 5:
                        if(event.mhtVal>300 and event.mhtVal<450):
                            ibin = "bin19"
                        else:
                            ibin = "bin21"
                ###bin coarser for high mht 300-inf
                    elif myFitBin == 6:
                        ibin = "bin22"
            #######
            nJets[0]     = event.nJetsHT
            nPhotons[0]  = event.nPhotonsTight
            mht[0]       = event.mhtVal
            ht[0]        = event.htVal
            photonPt[0]  = event.photonPt
            photonEta[0] = event.photonEta
            photonMinDR[0] = event.photonMinDR
    
            runNum[0]    = event.ra2_run
            lumiBlock[0] = event.ra2_lumi
            eventNum[0]  = event.ra2_event
            #
            fitExtrapolation = fitFunctions[ibin]
            fitDataExtrapolation = dataFitFunctions[ibin]
            fitDataDouble        = dataFitFunctions["bin31"]
            phenoFactor[0] = fitExtrapolation["pheno"]["func"].Eval(nJets[0])
            #print "computing squared errors on pheno ratio"
            phenoErr2UP[0]   = squaredErrorFromGraph(nJets[0],fitExtrapolation["pheno"],"corrUP")
            phenoErr2DN[0]   = squaredErrorFromGraph(nJets[0],fitExtrapolation["pheno"],"corrDN")
            #print "pheno: %2.4e(+%2.4e/-%2.4e)"%(phenoFactor[0],math.sqrt(phenoErr2UP[0]),math.sqrt(phenoErr2DN[0]))
            #phenoErr2[0]   = pol1FitError2(nJets[0],
            #                               fitExtrapolation["pheno"]["func"],
            #                               fitExtrapolation["pheno"]["cov"])["UP"]
            #print "computing relative squared errors on theory ratio"
            theoryErr2UP[0] = phenoFactor[0]*phenoFactor[0]*squaredRelErrorFromGraph(
                nJets[0],fitDataExtrapolation["pheno"],"corrUP")
            theoryErr2DN[0] = phenoFactor[0]*phenoFactor[0]*squaredRelErrorFromGraph(
                nJets[0],fitDataExtrapolation["pheno"],"corrDN")
            
            ## correct for the data/mc disagreement vs. njets in zmumu/gamma
            phenoDataMC[0] = fitDataDouble["double"]["pol1"]["func"].Eval(nJets[0])
            # think I have to do this differently, should it be (mean value - error)
            # error/(mean value)
            ##old version##phenoDataMCErr2UP[0] = fitDataDouble["double"]["pol1"]["func"].GetParError(0)
            ## take mean value, subtract the error from the envelope
            phenoDataMCErr2UP[0] = phenoDataMC[0]-fitDataDouble["double"]["pol1"]["corrSymDN"].Eval(nJets[0])
            #phenoDataMCErr2UP[0] = phenoDataMC[0]-fitDataDouble["double"]["pol1"]["corrDN"].Eval(nJets[0])
            #phenoDataMCErr2UP[0] = phenoDataMC[0]-fitDataDouble["double"]["pol1"]["uncSymDN"].Eval(nJets[0])
            #phenoDataMCErr2UP[0] = phenoDataMC[0]-fitDataDouble["double"]["pol1"]["uncDN"].Eval(nJets[0])
            phenoDataMCErr2UP[0] = phenoDataMCErr2UP[0]*phenoDataMCErr2UP[0]
            phenoDataMCErr2DN[0] = phenoDataMCErr2UP[0]
            
            ##taking error on double ratio from symmetrized fit###print "theo. unc: +%2.4e/-%2.4e"%(theoryErr2UP[0],theoryErr2DN[0])
            ##taking error on double ratio from symmetrized fit###print "computing squared errors on double ratio"
            ##taking error on double ratio from symmetrized fit##phenoDataMCErr2UP[0] = phenoFactor[0]*phenoFactor[0]*squaredErrorFromGraph(
            ##taking error on double ratio from symmetrized fit##    nJets[0],fitDataDouble["double"]["pol1"],"corrSymUP")
            ##taking error on double ratio from symmetrized fit##phenoDataMCErr2DN[0] = phenoFactor[0]*phenoFactor[0]*squaredErrorFromGraph(
            ##taking error on double ratio from symmetrized fit##    nJets[0],fitDataDouble["double"]["pol1"],"corrSymDN")
            #print "data/MC unc.: +%2.4e/-%2.4e"%(phenoDataMCErr2UP[0],phenoDataMCErr2DN[0])
            #theoryErr2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            #                                                                fitDataExtrapolation["pheno"]["func"],
            #                                                                fitDataExtrapolation["pheno"]["cov"])["UP"]
            #doublePol0Err2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            #                                                                    fitDoubleExtrapolation["pol0"]["func"],0)
            #doublePol1Err2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            #                                                                    fitDoubleExtrapolation["pol1"]["func"],
            #                                                                    fitDoubleExtrapolation["pol1"]["cov"])["UP"]
            if options.debug:
                print "nJets:%d, pheno:%2.4f - phenoErr:%2.2e(%2.2e), theory:%2.2e theoryErr:%2.2e(%2.2e)"%(
                    nJets[0],phenoFactor[0],
                    math.sqrt(phenoErr2[0]),math.sqrt(pol1FitError2(nJets[0],
                                                                    fitExtrapolation["pheno"]["func"],
                                                                    fitExtrapolation["pheno"]["cov"])["UP"]),
                    fitDataExtrapolation["pheno"]["func"].Eval(nJets[0]),
                    math.sqrt(theoryErr2[0]),math.sqrt(fitRelError2(nJets[0],
                                                                    fitDataExtrapolation["pheno"]["func"],
                                                                    fitDataExtrapolation["pheno"]["cov"])["UP"])
                    )
            ##purity[0]      = 0.925       ##mostly pulled from thin air
            ##purityErr2UP[0]  = 0.075*0.075 ##mostly pulled from thin air
            ##purityErr2DN[0]  = 0.075*0.075 ##mostly pulled from thin air
            photonBarEnc = "barrel"
            if abs(photonEta[0]) > 1.5:
                photonBarEnc = "endcap"
            
            purity[0]       = purityFunction[photonBarEnc].Eval(nJets[0])
            purityErr2UP[0] = (purityErrFunction[photonBarEnc]["syst"]["UP"].Eval(nJets[0])-purity[0])*(
                purityErrFunction[photonBarEnc]["syst"]["UP"].Eval(nJets[0])-purity[0])
            purityErr2DN[0] = (purity[0]-purityErrFunction[photonBarEnc]["syst"]["DN"].Eval(nJets[0]))*(
                purity[0]-purityErrFunction[photonBarEnc]["syst"]["DN"].Eval(nJets[0]))
            
            datamcSF[0] = dataMCSF(event.photonEta)["cv"]
            datamcSFErr2[0] = (dataMCSF(event.photonEta)["stat"]*dataMCSF(event.photonEta)["stat"])
            datamcSFErr2[0] = datamcSFErr2[0]+(dataMCSF(event.photonEta)["syst"]*dataMCSF(event.photonEta)["syst"])
            if options.genreco:
                accEff[0]      = fitExtrapolation["acc"]["func"].Eval(nJets[0])
                #print "computing squared errors on acceptance"
                accErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["acc"],"corrUP")
                accErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["acc"],"corrDN")
                #print "acceptance: %2.4e(+%2.4e/-%2.4e)"%(accEff[0],accErr2UP[0],accErr2DN[0])
                #accErr2[0]     = pol1FitError2(nJets[0],
                #                               fitExtrapolation["acc"]["func"],
                #                               fitExtrapolation["acc"]["cov"])["UP"]
                #print "computing squared errors on reco"
                recoEff[0]     = fitExtrapolation["reco"]["func"].Eval(nJets[0])
                recoErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["reco"],"corrUP")
                recoErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["reco"],"corrDN")
                #print "reco: %2.4e(+%2.4e/-%2.4e)"%(recoEff[0],recoErr2UP[0],recoErr2DN[0])
                #recoErr2[0]    = pol1FitError2(nJets[0],
                #                               fitExtrapolation["reco"]["func"],
                #                               fitExtrapolation["reco"]["cov"])["UP"]
                #print "computing squared errors on pixel"
                pixelEff[0]    = fitExtrapolation["pixel"]["func"].Eval(nJets[0])
                pixelErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["pixel"],"corrUP")
                pixelErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["pixel"],"corrDN")
                #print "pixel: %2.4e(+%2.4e/-%2.4e)"%(pixelEff[0],pixelErr2UP[0],pixelErr2DN[0])
                #pixelErr2[0]   = pol1FitError2(nJets[0],
                #                               fitExtrapolation["pixel"]["func"],
                #                               fitExtrapolation["pixel"]["cov"])["UP"]
                #print "computing squared errors on isolation"
                isoEff[0]      = fitExtrapolation["iso"]["func"].Eval(nJets[0])
                isoErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["iso"],"corrUP")
                isoErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["iso"],"corrDN")
                #print "isolation: %2.4e(+%2.4e/-%2.4e)"%(isoEff[0],isoErr2UP[0],isoErr2DN[0])
                #isoErr2[0]     = pol1FitError2(nJets[0],
                #                               fitExtrapolation["iso"]["func"],
                #                               fitExtrapolation["iso"]["cov"])["UP"]
            else:
                accEff[0]    = 1.0
                recoEff[0]   = 1.0
                pixelEff[0]  = 1.0
                isoEff[0]    = 1.0
                #accErr2[0]   = 0.0
                #recoErr2[0]  = 0.0
                #pixelErr2[0] = 0.0
                #isoErr2[0]   = 0.0
                accErr2UP[0]   = 0.0
                recoErr2UP[0]  = 0.0
                pixelErr2UP[0] = 0.0
                isoErr2UP[0]   = 0.0
                accErr2DN[0]   = 0.0
                recoErr2DN[0]  = 0.0
                pixelErr2DN[0] = 0.0
                isoErr2DN[0]   = 0.0
                
            scaleFactor[0] = purity[0]*phenoFactor[0]*phenoDataMC[0]/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ## Calculate the uncertainties
            numVals    = [purity[0],phenoFactor[0],phenoDataMC[0]]
            denVals    = [accEff[0],recoEff[0],pixelEff[0],isoEff[0],datamcSF[0]]

            #pheno up/dn
            numErrs2UP = [0.0,phenoErr2UP[0],0.0]
            numErrs2DN = [0.0,phenoErr2DN[0],0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            
            ##scaleFactorPhenUP[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPhenDN[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPhenUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorPhenDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            #pheno+theory up/dn
            numErrs2UP = [0.0,phenoErr2UP[0]+theoryErr2UP[0],0.0]
            numErrs2DN = [0.0,phenoErr2DN[0]+theoryErr2DN[0],0.0]
            
            ##scaleFactorPhenThUP[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPhenThDN[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPhenThUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorPhenThDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            ####pheno + theory + data/mc up/dn
            ###numErrs2UP = [0.0,phenoErr2UP[0]+theoryErr2UP[0],phenoDataMCErr2UP[0]]
            ###numErrs2DN = [0.0,phenoErr2DN[0]+theoryErr2DN[0],phenoDataMCErr2DN[0]]
            ###
            #####scaleFactorPhenDataMCUP[0]    = purity[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenDataMCDN[0]    = purity[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenThUP[0]    = purity[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]+phenoDataMCErr2UP[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenThDN[0]    = purity[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]+phenoDataMCErr2DN[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ###
            ###scaleFactorPhenThDataMCUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
            ###                                                                  denVals,denErrs2UP))
            ###scaleFactorPhenThDataMCDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
            ###                                                                  denVals,denErrs2DN))

            #purity up/dn
            numErrs2UP = [purityErr2UP[0],0.0,0.0]
            numErrs2DN = [purityErr2DN[0],0.0,0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            ##scaleFactorPurUP[0]    = (purity[0]+math.sqrt(purityErr2UP[0]))*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPurDN[0]    = (purity[0]-math.sqrt(purityErr2DN[0]))*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPurUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorPurDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #acc up/dn
            numErrs2UP = [0.0,0.0,0.0]
            numErrs2DN = [0.0,0.0,0.0]
            
            denErrs2UP = [accErr2UP[0],       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [accErr2DN[0],       0.0,        0.0,      0.0,        0.0]
            ##scaleFactorAccUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    (accEff[0]+math.sqrt(accErr2UP[0]))*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorAccDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    (accEff[0]-math.sqrt(accErr2DN[0]))*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorAccUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorAccDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #reco id up/dn
            denErrs2UP = [0.0,recoErr2UP[0],        0.0,      0.0,        0.0]
            denErrs2DN = [0.0,recoErr2DN[0],        0.0,      0.0,        0.0]
            ##scaleFactorIDUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*(recoEff[0]+math.sqrt(recoErr2UP[0]))*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorIDDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*(recoEff[0]-math.sqrt(recoErr2DN[0]))*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorIDUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorIDDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #pixel veto up/dn
            denErrs2UP = [0.0,       0.0,pixelErr2UP[0],      0.0,        0.0]
            denErrs2DN = [0.0,       0.0,pixelErr2DN[0],      0.0,        0.0]
            ##scaleFactorPixUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*(pixelEff[0]+math.sqrt(pixelErr2UP[0]))*isoEff[0])
            ##scaleFactorPixDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*(pixelEff[0]-math.sqrt(pixelErr2DN[0]))*isoEff[0])
            scaleFactorPixUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorPixDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #isolation up/dn
            denErrs2UP = [0.0,       0.0,        0.0,isoErr2UP[0],        0.0]
            denErrs2DN = [0.0,       0.0,        0.0,isoErr2DN[0],        0.0]
            ##scaleFactorIsoUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*(isoEff[0]+math.sqrt(isoErr2UP[0])))
            ##scaleFactorIsoDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*(isoEff[0]-math.sqrt(isoErr2DN[0])))
            scaleFactorIsoUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorIsoDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #data/mc s.f. up/dn
            denErrs2UP = [0.0,       0.0,        0.0,      0.0,datamcSFErr2[0]]
            denErrs2DN = [0.0,       0.0,        0.0,      0.0,datamcSFErr2[0]]
            ##scaleFactorDMCSFUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*(datamcSF[0]+math.sqrt(datamcSFErr2[0]))*pixelEff[0]*isoEff[0])
            ##scaleFactorDMCSFDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*(datamcSF[0]-math.sqrt(datamcSFErr2[0]))*pixelEff[0]*isoEff[0])
            scaleFactorDMCSFUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorDMCSFDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))
            
            
            ### do the variation of the scale factor not including the zmumu/gamma fit and the 
            ## data/mc correction uncertainty
            numErrs2UP = [purityErr2UP[0],phenoErr2UP[0],0.0]
            numErrs2DN = [purityErr2DN[0],phenoErr2DN[0],0.0]
            
            denErrs2UP = [accErr2UP[0],recoErr2UP[0],pixelErr2UP[0],isoErr2UP[0],datamcSFErr2[0]]
            denErrs2DN = [accErr2DN[0],recoErr2DN[0],pixelErr2DN[0],isoErr2DN[0],datamcSFErr2[0]]
            
            scaleFactorUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            ## do the variation of the pheno zmumu error only
            numErrs2UP = [0.0      ,theoryErr2UP[0],           0.0]
            numErrs2DN = [0.0      ,theoryErr2DN[0],           0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            
            ##scaleFactorThFitUP[0]  = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThFitDN[0]  = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])

            scaleFactorThFitUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorThFitDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            ## do the variation of the pheno data/mc correction only
            numErrs2UP = [0.0,0.0,phenoDataMCErr2UP[0]]
            numErrs2DN = [0.0,0.0,phenoDataMCErr2DN[0]]

            ##scaleFactorThDoubleUP[0]  = purity[0]*phenoFactor[0]*(phenoDataMC[0]+math.sqrt(phenoDataMCErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDoubleDN[0]  = purity[0]*phenoFactor[0]*(phenoDataMC[0]-math.sqrt(phenoDataMCErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorThDoubleUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                      denVals,denErrs2UP))
            scaleFactorThDoubleDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                      denVals,denErrs2DN))

            ##scaleFactorThDoubleUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(phenoDataMCErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDoubleDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(phenoDataMCErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            

            ## do the variation of both zmumu/gamma fit and double ratio uncertainty
            numErrs2UP = [0.0,theoryErr2UP[0],phenoDataMCErr2UP[0]]
            numErrs2DN = [0.0,theoryErr2DN[0],phenoDataMCErr2DN[0]]
            
            ##scaleFactorThUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0]+phenoDataMCErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0]+phenoDataMCErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0]))*(
            ##    phenoDataMC[0]+math.sqrt(phenoDataMCErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0]))*(
            ##    phenoDataMC[0]-math.sqrt(phenoDataMCErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            
            scaleFactorThUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                denVals,denErrs2UP))
            scaleFactorThDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                denVals,denErrs2DN))

            
            ### do the total variation from all systematic sources
            ##numErrs2UP = [purityErr2UP[0],phenoErr2UP[0]+theoryErr2UP[0]+phenoDataMCErr2UP[0]]
            ##numErrs2DN = [purityErr2DN[0],phenoErr2DN[0]+theoryErr2DN[0]+phenoDataMCErr2DN[0]]
            numErrs2UP = [purityErr2UP[0],phenoErr2UP[0]+theoryErr2UP[0],phenoDataMCErr2UP[0]]
            numErrs2DN = [purityErr2DN[0],phenoErr2DN[0]+theoryErr2DN[0],phenoDataMCErr2DN[0]]
            
            denErrs2UP = [accErr2UP[0],recoErr2UP[0],pixelErr2UP[0],isoErr2UP[0],datamcSFErr2[0]]
            denErrs2DN = [accErr2DN[0],recoErr2DN[0],pixelErr2DN[0],isoErr2DN[0],datamcSFErr2[0]]
            
            scaleFactorTotUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorTotDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))
            
            
            print "photon2012abcd::ht:%2.2f, mht:%2.2f, nJets:%d, nPhotons:%d, photonPt:%2.2f, photonEta:%2.2f, photonMinDR:%2.2f -- scaleFactor:%2.4f"%(
                event.htVal,event.mhtVal,nJets[0],event.nPhotonsTight,event.photonPt,event.photonEta,event.photonMinDR,scaleFactor[0])
            print "photon2012abcd::pheno:%2.4f(%2.4f[%2.4f]{%2.4f}), purity:%2.4f(%2.4f), accEff:%2.4f(%2.4f), recoEff:%2.4f(%2.4f),  pixelEff:%2.4f(%2.4f),  isoEff:%2.4f(%2.4f), dataMCSF:%2.4f(%2.4f)"%(
                phenoFactor[0],math.sqrt(phenoErr2UP[0]),math.sqrt(theoryErr2UP[0]),math.sqrt(phenoDataMCErr2UP[0]),
                purity[0],math.sqrt(purityErr2UP[0]),
                accEff[0],math.sqrt(accErr2UP[0]),
                recoEff[0],math.sqrt(recoErr2UP[0]),
                pixelEff[0],math.sqrt(pixelErr2UP[0]),
                isoEff[0],math.sqrt(isoErr2UP[0]),
                datamcSF[0],math.sqrt(datamcSFErr2[0]))

            eventWeight[0] = event.eventWt
            puWeight[0]    = event.puWt
            print "UP:%2.2e, DN:%2.2e, thUP:%2.2e, thDN:%2.2e,  totUP:%2.2e, totDN:%2.2e\n"%(scaleFactorUP[0],
                                                                                           scaleFactorDN[0],
                                                                                           scaleFactorThUP[0],
                                                                                           scaleFactorThDN[0],
                                                                                           scaleFactorTotUP[0],
                                                                                           scaleFactorTotDN[0],
                                                                                           )
            
    
            predictionTree.Fill()
    
        else:
            continue
        ###
    predictionTree.Write()
    
    ###Gjets as Data (for predictions with zero data events)
    gjetsChain = r.TChain("reco")
    gjetsChain.Add("%s/recoTreeDR0.0_gjets.root"%(options.inDir))
    gjetsTree = r.TTree('gjets', 'tree for gjets as data ')
    
    nJets[0]       = 0    
    nPhotons[0]    = 0    
    ht[0]          = 0.0
    mht[0]         = 0.0
    photonPt[0]    = 0.0
    photonEta[0]   = 0.0
    photonMinDR[0] = 0.0
    scaleFactor[0] = 1.0
    scaleFactorUP[0] = 1.0
    scaleFactorDN[0] = 1.0
    scaleFactorTotUP[0] = 1.0
    scaleFactorTotDN[0] = 1.0
    phenoFactor[0]   = 1.0
    phenoErr2UP[0]   = 1.0
    phenoErr2DN[0]   = 1.0
    scaleFactorPhenUP[0] = 1.0
    scaleFactorPhenDN[0] = 1.0
    theoryErr2UP[0]   = 1.0
    theoryErr2DN[0]   = 1.0
    scaleFactorThFitUP[0] = 1.0
    scaleFactorThFitDN[0] = 1.0
    phenoDataMC[0]   = 1.0
    phenoDataMCErr2UP[0]   = 1.0
    phenoDataMCErr2DN[0]   = 1.0
    scaleFactorThDoubleUP[0] = 1.0
    scaleFactorThDoubleDN[0] = 1.0
    scaleFactorThUP[0] = 1.0
    scaleFactorThDN[0] = 1.0
    scaleFactorPhenThUP[0] = 1.0
    scaleFactorPhenThDN[0] = 1.0
    accEff[0]       = 1.0
    accErr2UP[0]      = 1.0
    accErr2DN[0]      = 1.0
    scaleFactorAccUP[0] = 1.0
    scaleFactorAccDN[0] = 1.0
    recoEff[0]      = 1.0
    recoErr2UP[0]     = 1.0
    recoErr2DN[0]     = 1.0
    scaleFactorIDUP[0] = 1.0
    scaleFactorIDDN[0] = 1.0
    pixelEff[0]     = 1.0
    pixelErr2UP[0]    = 1.0
    pixelErr2DN[0]    = 1.0
    scaleFactorPixUP[0] = 1.0
    scaleFactorPixDN[0] = 1.0
    isoEff[0]       = 1.0
    isoErr2UP[0]      = 1.0
    isoErr2DN[0]      = 1.0
    scaleFactorIsoUP[0] = 1.0
    scaleFactorIsoDN[0] = 1.0
    purity[0]       = 1.0
    #purityErr2[0]   = 1.0
    purityErr2UP[0]   = 1.0
    purityErr2DN[0]   = 1.0
    scaleFactorPurUP[0] = 1.0
    scaleFactorPurDN[0] = 1.0
    datamcSF[0]     = 1.0
    datamcSFErr2[0] = 1.0
    scaleFactorDMCSFUP[0] = 1.0
    scaleFactorDMCSFDN[0] = 1.0
    totalErr2[0]     = 1.0
    eventWeight[0]   = 1.0
    puWeight[0]   = 1.0
    
    gjetsTree.Branch( 'nJets',      nJets,      'nJets/I' )
    gjetsTree.Branch( 'nPhotons',   nPhotons,   'nPhotons/I' )
    gjetsTree.Branch( 'ht',         ht,         'ht/D' )
    gjetsTree.Branch( 'mht',        mht,        'mht/D' )
    gjetsTree.Branch( 'photonPt',   photonPt,   'photonPt/D' )
    gjetsTree.Branch( 'photonEta',  photonEta,  'photonEta/D' )
    gjetsTree.Branch( 'photonMinDR',photonMinDR,'photonMinDR/D' )
    gjetsTree.Branch( 'scaleFactor',scaleFactor,'scaleFactor/D' )
    gjetsTree.Branch( 'scaleFactorUP' ,scaleFactorUP ,'scaleFactorUP/D' )
    gjetsTree.Branch( 'scaleFactorDN' ,scaleFactorDN ,'scaleFactorDN/D' )
    gjetsTree.Branch( 'scaleFactorTotUP' ,scaleFactorTotUP ,'scaleFactorTotUP/D' )
    gjetsTree.Branch( 'scaleFactorTotDN' ,scaleFactorTotDN ,'scaleFactorTotDN/D' )
    gjetsTree.Branch( 'phenoFactor' ,phenoFactor ,'phenoFactor/D' )
    gjetsTree.Branch( 'phenoErr2UP'   ,phenoErr2UP   ,'phenoErr2UP/D' )
    gjetsTree.Branch( 'phenoErr2DN'   ,phenoErr2DN   ,'phenoErr2DN/D' )
    gjetsTree.Branch( 'scaleFactorPhenUP' ,scaleFactorPhenUP ,'scaleFactorPhenUP/D' )
    gjetsTree.Branch( 'scaleFactorPhenDN' ,scaleFactorPhenDN ,'scaleFactorPhenDN/D' )
    gjetsTree.Branch( 'theoryErr2UP'  ,theoryErr2UP  ,'theoryErr2UP/D' )
    gjetsTree.Branch( 'theoryErr2DN'  ,theoryErr2DN  ,'theoryErr2DN/D' )
    gjetsTree.Branch( 'scaleFactorThFitUP' ,scaleFactorThFitUP ,'scaleFactorThFitUP/D' )
    gjetsTree.Branch( 'scaleFactorThFitDN' ,scaleFactorThFitDN ,'scaleFactorThFitDN/D' )
    gjetsTree.Branch( 'phenoDataMC'  ,phenoDataMC  ,'phenoDataMC/D' )
    gjetsTree.Branch( 'phenoDataMCErr2UP'  ,phenoDataMCErr2UP  ,'phenoDataMCErr2UP/D' )
    gjetsTree.Branch( 'phenoDataMCErr2DN'  ,phenoDataMCErr2DN  ,'phenoDataMCErr2DN/D' )
    gjetsTree.Branch( 'scaleFactorThDoubleUP' ,scaleFactorThDoubleUP ,'scaleFactorThDoubleUP/D' )
    gjetsTree.Branch( 'scaleFactorThDoubleDN' ,scaleFactorThDoubleDN ,'scaleFactorThDoubleDN/D' )
    gjetsTree.Branch( 'scaleFactorThUP' ,scaleFactorThUP ,'scaleFactorThUP/D' )
    gjetsTree.Branch( 'scaleFactorThDN' ,scaleFactorThDN ,'scaleFactorThDN/D' )
    gjetsTree.Branch( 'scaleFactorPhenThUP' ,scaleFactorPhenThUP ,'scaleFactorPhenThUP/D' )
    gjetsTree.Branch( 'scaleFactorPhenThDN' ,scaleFactorPhenThDN ,'scaleFactorPhenThDN/D' )
    gjetsTree.Branch( 'accEff'      ,accEff      ,'accEff/D' )
    gjetsTree.Branch( 'accErr2UP'     ,accErr2UP     ,'accErr2UP/D' )
    gjetsTree.Branch( 'accErr2DN'     ,accErr2DN     ,'accErr2DN/D' )
    gjetsTree.Branch( 'scaleFactorAccUP' ,scaleFactorAccUP ,'scaleFactorAccUP/D' )
    gjetsTree.Branch( 'scaleFactorAccDN' ,scaleFactorAccDN ,'scaleFactorAccDN/D' )
    gjetsTree.Branch( 'recoEff'     ,recoEff     ,'recoEff/D' )
    gjetsTree.Branch( 'recoErr2UP'    ,recoErr2UP    ,'recoErr2UP/D' )
    gjetsTree.Branch( 'recoErr2DN'    ,recoErr2DN    ,'recoErr2DN/D' )
    gjetsTree.Branch( 'scaleFactorIDUP' ,scaleFactorIDUP ,'scaleFactorIDUP/D' )
    gjetsTree.Branch( 'scaleFactorIDDN' ,scaleFactorIDDN ,'scaleFactorIDDN/D' )
    gjetsTree.Branch( 'pixelEff'    ,pixelEff    ,'pixelEff/D' )
    gjetsTree.Branch( 'pixelErr2UP'   ,pixelErr2UP   ,'pixelErr2UP/D' )
    gjetsTree.Branch( 'pixelErr2DN'   ,pixelErr2DN   ,'pixelErr2DN/D' )
    gjetsTree.Branch( 'scaleFactorPixUP' ,scaleFactorPixUP ,'scaleFactorPixUP/D' )
    gjetsTree.Branch( 'scaleFactorPixDN' ,scaleFactorPixDN ,'scaleFactorPixDN/D' )
    gjetsTree.Branch( 'isoEff'      ,isoEff      ,'isoEff/D' )
    gjetsTree.Branch( 'isoErr2UP'     ,isoErr2UP     ,'isoErr2UP/D' )
    gjetsTree.Branch( 'isoErr2DN'     ,isoErr2DN     ,'isoErr2DN/D' )
    gjetsTree.Branch( 'scaleFactorIsoUP' ,scaleFactorIsoUP ,'scaleFactorIsoUP/D' )
    gjetsTree.Branch( 'scaleFactorIsoDN' ,scaleFactorIsoDN ,'scaleFactorIsoDN/D' )
    gjetsTree.Branch( 'purity'      ,purity      ,'purity/D' )
    #gjetsTree.Branch( 'purityErr2'  ,purityErr2  ,'purityErr2/D' )
    gjetsTree.Branch( 'purityErr2UP'  ,purityErr2UP  ,'purityErr2UP/D' )
    gjetsTree.Branch( 'purityErr2DN'  ,purityErr2DN  ,'purityErr2DN/D' )
    gjetsTree.Branch( 'scaleFactorPurUP' ,scaleFactorPurUP ,'scaleFactorPurUP/D' )
    gjetsTree.Branch( 'scaleFactorPurDN' ,scaleFactorPurDN ,'scaleFactorPurDN/D' )
    gjetsTree.Branch( 'datamcSF'    ,datamcSF    ,'datamcSF/D' )
    gjetsTree.Branch( 'datamcSFErr2',datamcSFErr2,'datamcSFErr2/D' )
    gjetsTree.Branch( 'scaleFactorDMCSFUP' ,scaleFactorDMCSFUP ,'scaleFactorDMCSFUP/D' )
    gjetsTree.Branch( 'scaleFactorDMCSFDN' ,scaleFactorDMCSFDN ,'scaleFactorDMCSFDN/D' )
    gjetsTree.Branch( 'totalErr2'   ,totalErr2   ,'totalErr2/D' )
    gjetsTree.Branch( 'eventWeight',eventWeight,'eventWeight/D' )
    gjetsTree.Branch( 'puWeight',puWeight,'puWeight/D' )
    
    for event in gjetsChain:
        if (event.photonPt > 100 and event.photonIsTightIso and event.photonPixelVeto and event.dphi1>0.5 and event.dphi2>0.5 and event.dphi3>0.3 and event.nJetsHT>1):
            if (event.htVal<500 or (event.htVal<800 and event.mhtVal<200)):
                continue
            if not (event.passRA2ElVeto and event.passRA2MuVeto):
                continue

            if myFitBin == 0:
                if (event.mhtVal>100 and event.mhtVal<200):
                    ibin = "bin23"
                elif (event.mhtVal<300):
                    ibin = "bin24"
                elif (event.mhtVal<450):
                    ibin = "bin19"
                else:
                    ibin = "bin21"
            else:
                if (event.mhtVal>100 and event.mhtVal<125):
                    ibin = "bin1"
                elif (event.mhtVal>125 and event.mhtVal<150):
                    ibin = "bin2"
                elif (event.mhtVal>150 and event.mhtVal<175):
                    ibin = "bin3"
                elif (event.mhtVal>175 and event.mhtVal<200):
                    ibin = "bin4"
                elif (event.mhtVal>200 and event.mhtVal<225):
                    ibin = "bin5"
                elif (event.mhtVal>225 and event.mhtVal<250):
                    ibin = "bin6"
                elif (event.mhtVal>250 and event.mhtVal<275):
                    ibin = "bin7"
                elif (event.mhtVal>275 and event.mhtVal<300):
                    ibin = "bin8"
                    
                else:
                ##standard fine binning
                    if myFitBin == 1:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<425):
                            ibin = "bin13"
                        elif (event.mhtVal>425 and event.mhtVal<450):
                            ibin = "bin14"
                        elif (event.mhtVal>450 and event.mhtVal<500):
                            ibin = "bin15"
                        elif (event.mhtVal>500 and event.mhtVal<550):
                            ibin = "bin16"
                        elif (event.mhtVal>550 and event.mhtVal<600):
                            ibin = "bin17"
                        else:
                            ibin = "bin18"
                #####bin coarser for high mht 450-inf
                    elif myFitBin == 2:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<425):
                            ibin = "bin13"
                        elif (event.mhtVal>425 and event.mhtVal<450):
                            ibin = "bin14"
                        else:
                            ibin = "bin21"
                #####bin coarser for high mht 400-450-inf
                    elif myFitBin == 3:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<450):
                            ibin = "bin27"
                        else:
                            ibin = "bin21"
                #####bin coarser for high mht 300-450-600-inf
                    elif myFitBin == 4:
                        if(event.mhtVal>300 and event.mhtVal<450):
                            ibin = "bin19"
                        elif(event.mhtVal>450 and event.mhtVal<600):
                            ibin = "bin20"
                        else:
                            ibin = "bin18"
                ###bin coarser for high mht 300-450-inf
                    elif myFitBin == 5:
                        if(event.mhtVal>300 and event.mhtVal<450):
                            ibin = "bin19"
                        else:
                            ibin = "bin21"
                ###bin coarser for high mht 300-inf
                    elif myFitBin == 6:
                        ibin = "bin22"
            #
            nJets[0]     = event.nJetsHT
            nPhotons[0]  = event.nPhotonsTight
            mht[0]       = event.mhtVal
            ht[0]        = event.htVal
            photonPt[0]  = event.photonPt
            photonEta[0] = event.photonEta
            photonMinDR[0] = event.photonMinDR
            #
            fitExtrapolation = fitFunctions[ibin]
            fitDataExtrapolation = dataFitFunctions[ibin]
            phenoFactor[0] = fitExtrapolation["pheno"]["func"].Eval(event.nJetsHT)
            #print "computing squared errors on pheno ratio"
            phenoErr2UP[0]   = squaredErrorFromGraph(nJets[0],fitExtrapolation["pheno"],"corrUP")
            phenoErr2DN[0]   = squaredErrorFromGraph(nJets[0],fitExtrapolation["pheno"],"corrDN")
            #print "pheno: %2.4e(+%2.4e/-%2.4e)"%(phenoFactor[0],math.sqrt(phenoErr2UP[0]),math.sqrt(phenoErr2DN[0]))
            #phenoErr2[0]   = pol1FitError2(nJets[0],
            #                               fitExtrapolation["pheno"]["func"],
            #                               fitExtrapolation["pheno"]["cov"])["UP"]
            #print "computing relative squared errors on theory ratio"
            theoryErr2UP[0] = phenoFactor[0]*phenoFactor[0]*squaredRelErrorFromGraph(
                nJets[0],fitDataExtrapolation["pheno"],"corrUP")
            theoryErr2DN[0] = phenoFactor[0]*phenoFactor[0]*squaredRelErrorFromGraph(
                nJets[0],fitDataExtrapolation["pheno"],"corrDN")
            #print "theo. unc: +%2.4e/-%2.4e"%(theoryErr2UP[0],theoryErr2DN[0])

            ## correct for the data/mc disagreement vs. njets in zmumu/gamma
            phenoDataMC[0] = fitDataDouble["double"]["pol1"]["func"].Eval(nJets[0])
            #phenoDataMCErr2UP[0] = fitDataDouble["double"]["pol1"]["func"].GetParError(0)
            # think I have to do this differently, should it be (mean value - error)
            # error/(mean value)
            ##old version##phenoDataMCErr2UP[0] = fitDataDouble["double"]["pol1"]["func"].GetParError(0)
            ## take mean value, subtract the error from the envelope
            phenoDataMCErr2UP[0] = phenoDataMC[0]-fitDataDouble["double"]["pol1"]["corrSymDN"].Eval(nJets[0])
            #phenoDataMCErr2UP[0] = phenoDataMC[0]-fitDataDouble["double"]["pol1"]["corrDN"].Eval(nJets[0])
            #phenoDataMCErr2UP[0] = phenoDataMC[0]-fitDataDouble["double"]["pol1"]["uncSymDN"].Eval(nJets[0])
            #phenoDataMCErr2UP[0] = phenoDataMC[0]-fitDataDouble["double"]["pol1"]["uncDN"].Eval(nJets[0])
            phenoDataMCErr2UP[0] = phenoDataMCErr2UP[0]*phenoDataMCErr2UP[0]
            phenoDataMCErr2DN[0] = phenoDataMCErr2UP[0]

            ###print "computing squared errors on double ratio"
            ##phenoDataMCErr2UP[0] = phenoFactor[0]*phenoFactor[0]*squaredErrorFromGraph(
            ##    nJets[0],fitDataDouble["double"]["pol1"],"corrSymUP")
            ##phenoDataMCErr2DN[0] = phenoFactor[0]*phenoFactor[0]*squaredErrorFromGraph(
            ##    nJets[0],fitDataDouble["double"]["pol1"],"corrSymDN")
            ###print "data/MC unc.: +%2.4e/-%2.4e"%(phenoDataMCErr2UP[0],phenoDataMCErr2DN[0])
            ###theoryErr2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            ###                                                                fitDataExtrapolation["pheno"]["func"],
            ###                                                                fitDataExtrapolation["pheno"]["cov"])["UP"]
            ###doublePol0Err2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            ###                                                                    fitDoubleExtrapolation["pol0"]["func"],0)
            ###doublePol1Err2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            ###                                                                    fitDoubleExtrapolation["pol1"]["func"],
            ###                                                                    fitDoubleExtrapolation["pol1"]["cov"])["UP"]
            if options.debug:
                print "nJets:%d, pheno:%2.4f - phenoErr:%2.2e(%2.2e), theory:%2.2e theoryErr:%2.2e(%2.2e)"%(
                    nJets[0],phenoFactor[0],
                    math.sqrt(phenoErr2[0]),math.sqrt(pol1FitError2(nJets[0],
                                                                    fitExtrapolation["pheno"]["func"],
                                                                    fitExtrapolation["pheno"]["cov"])["UP"]),
                    fitDataExtrapolation["pheno"]["func"].Eval(nJets[0]),
                    math.sqrt(theoryErr2[0]),math.sqrt(fitRelError2(nJets[0],
                                                                    fitDataExtrapolation["pheno"]["func"],
                                                                    fitDataExtrapolation["pheno"]["cov"])["UP"])
                    )
            ###Treat gjets sample as data for the zero data prediction bins
            photonBarEnc = "barrel"
            if abs(photonEta[0]) > 1.5:
                photonBarEnc = "endcap"
            
            purity[0]       = purityFunction[photonBarEnc].Eval(nJets[0])
            purityErr2UP[0] = (purityErrFunction[photonBarEnc]["syst"]["UP"].Eval(nJets[0])-purity[0])*(
                purityErrFunction[photonBarEnc]["syst"]["UP"].Eval(nJets[0])-purity[0])
            purityErr2DN[0] = (purity[0]-purityErrFunction[photonBarEnc]["syst"]["DN"].Eval(nJets[0]))*(
                purity[0]-purityErrFunction[photonBarEnc]["syst"]["DN"].Eval(nJets[0]))

            datamcSF[0]     = dataMCSF(event.photonEta)["cv"]
            datamcSFErr2[0] = (dataMCSF(event.photonEta)["stat"]*dataMCSF(event.photonEta)["stat"])
            datamcSFErr2[0] = datamcSFErr2[0]+(dataMCSF(event.photonEta)["syst"]*dataMCSF(event.photonEta)["syst"])
            if options.genreco:
                accEff[0]      = fitExtrapolation["acc"]["func"].Eval(nJets[0])
                #print "computing squared errors on acceptance"
                accErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["acc"],"corrUP")
                accErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["acc"],"corrDN")
                #print "acceptance: %2.4e(+%2.4e/-%2.4e)"%(accEff[0],accErr2UP[0],accErr2DN[0])
                #accErr2[0]     = pol1FitError2(nJets[0],
                #                               fitExtrapolation["acc"]["func"],
                #                               fitExtrapolation["acc"]["cov"])["UP"]
                #print "computing squared errors on reco"
                recoEff[0]     = fitExtrapolation["reco"]["func"].Eval(nJets[0])
                recoErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["reco"],"corrUP")
                recoErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["reco"],"corrDN")
                #print "reco: %2.4e(+%2.4e/-%2.4e)"%(recoEff[0],recoErr2UP[0],recoErr2DN[0])
                #recoErr2[0]    = pol1FitError2(nJets[0],
                #                               fitExtrapolation["reco"]["func"],
                #                               fitExtrapolation["reco"]["cov"])["UP"]
                #print "computing squared errors on pixel"
                pixelEff[0]    = fitExtrapolation["pixel"]["func"].Eval(nJets[0])
                pixelErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["pixel"],"corrUP")
                pixelErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["pixel"],"corrDN")
                #print "pixel: %2.4e(+%2.4e/-%2.4e)"%(pixelEff[0],pixelErr2UP[0],pixelErr2DN[0])
                #pixelErr2[0]   = pol1FitError2(nJets[0],
                #                               fitExtrapolation["pixel"]["func"],
                #                               fitExtrapolation["pixel"]["cov"])["UP"]
                #print "computing squared errors on isolation"
                isoEff[0]      = fitExtrapolation["iso"]["func"].Eval(nJets[0])
                isoErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["iso"],"corrUP")
                isoErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["iso"],"corrDN")
                #print "isolation: %2.4e(+%2.4e/-%2.4e)"%(isoEff[0],isoErr2UP[0],isoErr2DN[0])
                #isoErr2[0]     = pol1FitError2(nJets[0],
                #                               fitExtrapolation["iso"]["func"],
                #                               fitExtrapolation["iso"]["cov"])["UP"]
            else:
                accEff[0]    = 1.0
                recoEff[0]   = 1.0
                pixelEff[0]  = 1.0
                isoEff[0]    = 1.0
                #accErr2[0]   = 0.0
                #recoErr2[0]  = 0.0
                #pixelErr2[0] = 0.0
                #isoErr2[0]   = 0.0
                accErr2UP[0]   = 0.0
                recoErr2UP[0]  = 0.0
                pixelErr2UP[0] = 0.0
                isoErr2UP[0]   = 0.0
                accErr2DN[0]   = 0.0
                recoErr2DN[0]  = 0.0
                pixelErr2DN[0] = 0.0
                isoErr2DN[0]   = 0.0
                
            scaleFactor[0] = purity[0]*phenoFactor[0]*phenoDataMC[0]/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ## Calculate the uncertainties
            numVals    = [purity[0],phenoFactor[0],phenoDataMC[0]]
            denVals    = [accEff[0],recoEff[0],pixelEff[0],isoEff[0],datamcSF[0]]

            #pheno up/dn
            numErrs2UP = [0.0,phenoErr2UP[0],0.0]
            numErrs2DN = [0.0,phenoErr2DN[0],0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            
            ##scaleFactorPhenUP[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPhenDN[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPhenUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorPhenDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            #pheno+theory up/dn
            numErrs2UP = [0.0,phenoErr2UP[0]+theoryErr2UP[0],0.0]
            numErrs2DN = [0.0,phenoErr2DN[0]+theoryErr2DN[0],0.0]
            
            ##scaleFactorPhenThUP[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPhenThDN[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPhenThUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorPhenThDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            ####pheno + theory + data/mc up/dn
            ###numErrs2UP = [0.0,phenoErr2UP[0]+theoryErr2UP[0],phenoDataMCErr2UP[0]]
            ###numErrs2DN = [0.0,phenoErr2DN[0]+theoryErr2DN[0],phenoDataMCErr2DN[0]]
            ###
            #####scaleFactorPhenDataMCUP[0]    = purity[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenDataMCDN[0]    = purity[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenThUP[0]    = purity[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]+phenoDataMCErr2UP[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenThDN[0]    = purity[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]+phenoDataMCErr2DN[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ###
            ###scaleFactorPhenThDataMCUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
            ###                                                                  denVals,denErrs2UP))
            ###scaleFactorPhenThDataMCDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
            ###                                                                  denVals,denErrs2DN))

            #purity up/dn
            numErrs2UP = [purityErr2UP[0],0.0,0.0]
            numErrs2DN = [purityErr2DN[0],0.0,0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            ##scaleFactorPurUP[0]    = (purity[0]+math.sqrt(purityErr2UP[0]))*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPurDN[0]    = (purity[0]-math.sqrt(purityErr2DN[0]))*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPurUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorPurDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #acc up/dn
            numErrs2UP = [0.0,0.0,0.0]
            numErrs2DN = [0.0,0.0,0.0]
            
            denErrs2UP = [accErr2UP[0],       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [accErr2DN[0],       0.0,        0.0,      0.0,        0.0]
            ##scaleFactorAccUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    (accEff[0]+math.sqrt(accErr2UP[0]))*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorAccDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    (accEff[0]-math.sqrt(accErr2DN[0]))*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorAccUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorAccDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #reco id up/dn
            denErrs2UP = [0.0,recoErr2UP[0],        0.0,      0.0,        0.0]
            denErrs2DN = [0.0,recoErr2DN[0],        0.0,      0.0,        0.0]
            ##scaleFactorIDUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*(recoEff[0]+math.sqrt(recoErr2UP[0]))*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorIDDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*(recoEff[0]-math.sqrt(recoErr2DN[0]))*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorIDUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorIDDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #pixel veto up/dn
            denErrs2UP = [0.0,       0.0,pixelErr2UP[0],      0.0,        0.0]
            denErrs2DN = [0.0,       0.0,pixelErr2DN[0],      0.0,        0.0]
            ##scaleFactorPixUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*(pixelEff[0]+math.sqrt(pixelErr2UP[0]))*isoEff[0])
            ##scaleFactorPixDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*(pixelEff[0]-math.sqrt(pixelErr2DN[0]))*isoEff[0])
            scaleFactorPixUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorPixDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #isolation up/dn
            denErrs2UP = [0.0,       0.0,        0.0,isoErr2UP[0],        0.0]
            denErrs2DN = [0.0,       0.0,        0.0,isoErr2DN[0],        0.0]
            ##scaleFactorIsoUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*(isoEff[0]+math.sqrt(isoErr2UP[0])))
            ##scaleFactorIsoDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*(isoEff[0]-math.sqrt(isoErr2DN[0])))
            scaleFactorIsoUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorIsoDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #data/mc s.f. up/dn
            denErrs2UP = [0.0,       0.0,        0.0,      0.0,datamcSFErr2[0]]
            denErrs2DN = [0.0,       0.0,        0.0,      0.0,datamcSFErr2[0]]
            ##scaleFactorDMCSFUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*(datamcSF[0]+math.sqrt(datamcSFErr2[0]))*pixelEff[0]*isoEff[0])
            ##scaleFactorDMCSFDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*(datamcSF[0]-math.sqrt(datamcSFErr2[0]))*pixelEff[0]*isoEff[0])
            scaleFactorDMCSFUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorDMCSFDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))
            
            
            ### do the variation of the scale factor not including the zmumu/gamma fit and the 
            ## data/mc correction uncertainty
            numErrs2UP = [purityErr2UP[0],phenoErr2UP[0],0.0]
            numErrs2DN = [purityErr2DN[0],phenoErr2DN[0],0.0]
            
            denErrs2UP = [accErr2UP[0],recoErr2UP[0],pixelErr2UP[0],isoErr2UP[0],datamcSFErr2[0]]
            denErrs2DN = [accErr2DN[0],recoErr2DN[0],pixelErr2DN[0],isoErr2DN[0],datamcSFErr2[0]]
            
            scaleFactorUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            ## do the variation of the pheno zmumu error only
            numErrs2UP = [0.0      ,theoryErr2UP[0],           0.0]
            numErrs2DN = [0.0      ,theoryErr2DN[0],           0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            
            ##scaleFactorThFitUP[0]  = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThFitDN[0]  = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])

            scaleFactorThFitUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorThFitDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))

            ## do the variation of the pheno data/mc correction only
            numErrs2UP = [0.0,0.0,phenoDataMCErr2UP[0]]
            numErrs2DN = [0.0,0.0,phenoDataMCErr2DN[0]]

            ##scaleFactorThDoubleUP[0]  = purity[0]*phenoFactor[0]*(phenoDataMC[0]+math.sqrt(phenoDataMCErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDoubleDN[0]  = purity[0]*phenoFactor[0]*(phenoDataMC[0]-math.sqrt(phenoDataMCErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorThDoubleUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                      denVals,denErrs2UP))
            scaleFactorThDoubleDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                      denVals,denErrs2DN))

            ##scaleFactorThDoubleUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(phenoDataMCErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDoubleDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(phenoDataMCErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            

            ## do the variation of both zmumu/gamma fit and double ratio uncertainty
            numErrs2UP = [0.0,theoryErr2UP[0],phenoDataMCErr2UP[0]]
            numErrs2DN = [0.0,theoryErr2DN[0],phenoDataMCErr2DN[0]]
            
            ##scaleFactorThUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0]+phenoDataMCErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0]+phenoDataMCErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0]))*(
            ##    phenoDataMC[0]+math.sqrt(phenoDataMCErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0]))*(
            ##    phenoDataMC[0]-math.sqrt(phenoDataMCErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            
            scaleFactorThUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                denVals,denErrs2UP))
            scaleFactorThDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                denVals,denErrs2DN))

            
            ### do the total variation from all systematic sources
            ##numErrs2UP = [purityErr2UP[0],phenoErr2UP[0]+theoryErr2UP[0]+phenoDataMCErr2UP[0]]
            ##numErrs2DN = [purityErr2DN[0],phenoErr2DN[0]+theoryErr2DN[0]+phenoDataMCErr2DN[0]]
            numErrs2UP = [purityErr2UP[0],phenoErr2UP[0]+theoryErr2UP[0],phenoDataMCErr2UP[0]]
            numErrs2DN = [purityErr2DN[0],phenoErr2DN[0]+theoryErr2DN[0],phenoDataMCErr2DN[0]]
            
            denErrs2UP = [accErr2UP[0],recoErr2UP[0],pixelErr2UP[0],isoErr2UP[0],datamcSFErr2[0]]
            denErrs2DN = [accErr2DN[0],recoErr2DN[0],pixelErr2DN[0],isoErr2DN[0],datamcSFErr2[0]]
            
            scaleFactorTotUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorTotDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))
            
            print "gjets::ht:%2.2f, mht:%2.2f, nJets:%d, nPhotons:%d, photonPt:%2.2f, photonEta:%2.2f, photonMinDR:%2.2f -- scaleFactor:%2.4f"%(
                event.htVal,event.mhtVal,event.nJetsHT,event.nPhotonsTight,event.photonPt,event.photonEta,event.photonMinDR,scaleFactor[0])
            print "gjets::pheno:%2.4f(%2.4f[%2.4f]{%2.4f}), purity:%2.4f(%2.4f), accEff:%2.4f(%2.4f), recoEff:%2.4f(%2.4f),  pixelEff:%2.4f(%2.4f),  isoEff:%2.4f(%2.4f), dataMCSF:%2.4f(%2.4f)"%(
                phenoFactor[0],math.sqrt(phenoErr2UP[0]),math.sqrt(theoryErr2UP[0]),math.sqrt(phenoDataMCErr2UP[0]),
                purity[0],math.sqrt(purityErr2UP[0]),
                accEff[0],math.sqrt(accErr2UP[0]),
                recoEff[0],math.sqrt(recoErr2UP[0]),
                pixelEff[0],math.sqrt(pixelErr2UP[0]),
                isoEff[0],math.sqrt(isoErr2UP[0]),
                datamcSF[0],math.sqrt(datamcSFErr2[0]))

            eventWeight[0] = 19.4/10*event.eventWt
            puWeight[0]    = event.puWt
            print "UP:%2.2e, DN:%2.2e, thUP:%2.2e, thDN:%2.2e,  totUP:%2.2e, totDN:%2.2e\n"%(scaleFactorUP[0],
                                                                                             scaleFactorDN[0],
                                                                                             scaleFactorThUP[0],
                                                                                             scaleFactorThDN[0],
                                                                                             scaleFactorTotUP[0],
                                                                                             scaleFactorTotDN[0],
                                                                        )
    
    
            gjetsTree.Fill()
    
    gjetsTree.Write()
    
    ###Gjets as MC
    mcChain = r.TChain("reco")
    mcChain.Add("%s/recoTreeDR0.0_gjets.root"%(options.inDir))
    mcTree = r.TTree('mc', 'tree for mc ')
    
    nJets[0]       = 0    
    nPhotons[0]    = 0    
    ht[0]          = 0.0
    mht[0]         = 0.0
    photonPt[0]    = 0.0
    photonEta[0]   = 0.0
    photonMinDR[0] = 0.0
    scaleFactor[0] = 1.0
    scaleFactorUP[0] = 1.0
    scaleFactorDN[0] = 1.0
    scaleFactorTotUP[0] = 1.0
    scaleFactorTotDN[0] = 1.0
    phenoFactor[0]   = 1.0
    phenoErr2UP[0]   = 1.0
    phenoErr2DN[0]   = 1.0
    scaleFactorPhenUP[0] = 1.0
    scaleFactorPhenDN[0] = 1.0
    theoryErr2UP[0]   = 1.0
    theoryErr2DN[0]   = 1.0
    scaleFactorThFitUP[0] = 1.0
    scaleFactorThFitDN[0] = 1.0
    phenoDataMC[0]   = 1.0
    phenoDataMCErr2UP[0]   = 1.0
    phenoDataMCErr2DN[0]   = 1.0
    scaleFactorThDoubleUP[0] = 1.0
    scaleFactorThDoubleDN[0] = 1.0
    scaleFactorThUP[0] = 1.0
    scaleFactorThDN[0] = 1.0
    scaleFactorPhenThUP[0] = 1.0
    scaleFactorPhenThDN[0] = 1.0
    accEff[0]       = 1.0
    accErr2UP[0]      = 1.0
    accErr2DN[0]      = 1.0
    scaleFactorAccUP[0] = 1.0
    scaleFactorAccDN[0] = 1.0
    recoEff[0]      = 1.0
    recoErr2UP[0]     = 1.0
    recoErr2DN[0]     = 1.0
    scaleFactorIDUP[0] = 1.0
    scaleFactorIDDN[0] = 1.0
    pixelEff[0]     = 1.0
    pixelErr2UP[0]    = 1.0
    pixelErr2DN[0]    = 1.0
    scaleFactorPixUP[0] = 1.0
    scaleFactorPixDN[0] = 1.0
    isoEff[0]       = 1.0
    isoErr2UP[0]      = 1.0
    isoErr2DN[0]      = 1.0
    scaleFactorIsoUP[0] = 1.0
    scaleFactorIsoDN[0] = 1.0
    purity[0]       = 1.0
    purityErr2   = array( 'd', [ 0.] )
    purityErr2[0]   = 1.0
    scaleFactorPurUP[0] = 1.0
    scaleFactorPurDN[0] = 1.0
    datamcSF[0]     = 1.0
    datamcSFErr2[0] = 1.0
    scaleFactorDMCSFUP[0] = 1.0
    scaleFactorDMCSFDN[0] = 1.0
    totalErr2[0]     = 1.0
    eventWeight[0]   = 1.0
    puWeight[0]   = 1.0
    
    mcTree.Branch( 'nJets',      nJets,      'nJets/I' )
    mcTree.Branch( 'nPhotons',   nPhotons,   'nPhotons/I' )
    mcTree.Branch( 'ht',         ht,         'ht/D' )
    mcTree.Branch( 'mht',        mht,        'mht/D' )
    mcTree.Branch( 'photonPt',   photonPt,   'photonPt/D' )
    mcTree.Branch( 'photonEta',  photonEta,  'photonEta/D' )
    mcTree.Branch( 'photonMinDR',photonMinDR,'photonMinDR/D' )
    mcTree.Branch( 'scaleFactor',scaleFactor,'scaleFactor/D' )
    mcTree.Branch( 'scaleFactorUP' ,scaleFactorUP ,'scaleFactorUP/D' )
    mcTree.Branch( 'scaleFactorDN' ,scaleFactorDN ,'scaleFactorDN/D' )
    mcTree.Branch( 'scaleFactorTotUP' ,scaleFactorTotUP ,'scaleFactorTotUP/D' )
    mcTree.Branch( 'scaleFactorTotDN' ,scaleFactorTotDN ,'scaleFactorTotDN/D' )
    mcTree.Branch( 'phenoFactor' ,phenoFactor ,'phenoFactor/D' )
    mcTree.Branch( 'phenoErr2UP'   ,phenoErr2UP   ,'phenoErr2UP/D' )
    mcTree.Branch( 'phenoErr2DN'   ,phenoErr2DN   ,'phenoErr2DN/D' )
    mcTree.Branch( 'scaleFactorPhenUP' ,scaleFactorPhenUP ,'scaleFactorPhenUP/D' )
    mcTree.Branch( 'scaleFactorPhenDN' ,scaleFactorPhenDN ,'scaleFactorPhenDN/D' )
    mcTree.Branch( 'theoryErr2UP'  ,theoryErr2UP  ,'theoryErr2UP/D' )
    mcTree.Branch( 'theoryErr2DN'  ,theoryErr2DN  ,'theoryErr2DN/D' )
    mcTree.Branch( 'scaleFactorThFitUP' ,scaleFactorThFitUP ,'scaleFactorThFitUP/D' )
    mcTree.Branch( 'scaleFactorThFitDN' ,scaleFactorThFitDN ,'scaleFactorThFitDN/D' )
    mcTree.Branch( 'phenoDataMC'  ,phenoDataMC  ,'phenoDataMC/D' )
    mcTree.Branch( 'phenoDataMCErr2UP'  ,phenoDataMCErr2UP  ,'phenoDataMCErr2UP/D' )
    mcTree.Branch( 'phenoDataMCErr2DN'  ,phenoDataMCErr2DN  ,'phenoDataMCErr2DN/D' )
    mcTree.Branch( 'scaleFactorThDoubleUP' ,scaleFactorThDoubleUP ,'scaleFactorThDoubleUP/D' )
    mcTree.Branch( 'scaleFactorThDoubleDN' ,scaleFactorThDoubleDN ,'scaleFactorThDoubleDN/D' )
    mcTree.Branch( 'scaleFactorThUP' ,scaleFactorThUP ,'scaleFactorThUP/D' )
    mcTree.Branch( 'scaleFactorThDN' ,scaleFactorThDN ,'scaleFactorThDN/D' )
    mcTree.Branch( 'scaleFactorPhenThUP' ,scaleFactorPhenThUP ,'scaleFactorPhenThUP/D' )
    mcTree.Branch( 'scaleFactorPhenThDN' ,scaleFactorPhenThDN ,'scaleFactorPhenThDN/D' )
    mcTree.Branch( 'accEff'      ,accEff      ,'accEff/D' )
    mcTree.Branch( 'accErr2UP'     ,accErr2UP     ,'accErr2UP/D' )
    mcTree.Branch( 'accErr2DN'     ,accErr2DN     ,'accErr2DN/D' )
    mcTree.Branch( 'scaleFactorAccUP' ,scaleFactorAccUP ,'scaleFactorAccUP/D' )
    mcTree.Branch( 'scaleFactorAccDN' ,scaleFactorAccDN ,'scaleFactorAccDN/D' )
    mcTree.Branch( 'recoEff'     ,recoEff     ,'recoEff/D' )
    mcTree.Branch( 'recoErr2UP'    ,recoErr2UP    ,'recoErr2UP/D' )
    mcTree.Branch( 'recoErr2DN'    ,recoErr2DN    ,'recoErr2DN/D' )
    mcTree.Branch( 'scaleFactorIDUP' ,scaleFactorIDUP ,'scaleFactorIDUP/D' )
    mcTree.Branch( 'scaleFactorIDDN' ,scaleFactorIDDN ,'scaleFactorIDDN/D' )
    mcTree.Branch( 'pixelEff'    ,pixelEff    ,'pixelEff/D' )
    mcTree.Branch( 'pixelErr2UP'   ,pixelErr2UP   ,'pixelErr2UP/D' )
    mcTree.Branch( 'pixelErr2DN'   ,pixelErr2DN   ,'pixelErr2DN/D' )
    mcTree.Branch( 'scaleFactorPixUP' ,scaleFactorPixUP ,'scaleFactorPixUP/D' )
    mcTree.Branch( 'scaleFactorPixDN' ,scaleFactorPixDN ,'scaleFactorPixDN/D' )
    mcTree.Branch( 'isoEff'      ,isoEff      ,'isoEff/D' )
    mcTree.Branch( 'isoErr2UP'     ,isoErr2UP     ,'isoErr2UP/D' )
    mcTree.Branch( 'isoErr2DN'     ,isoErr2DN     ,'isoErr2DN/D' )
    mcTree.Branch( 'scaleFactorIsoUP' ,scaleFactorIsoUP ,'scaleFactorIsoUP/D' )
    mcTree.Branch( 'scaleFactorIsoDN' ,scaleFactorIsoDN ,'scaleFactorIsoDN/D' )
    mcTree.Branch( 'purity'      ,purity      ,'purity/D' )
    mcTree.Branch( 'purityErr2'  ,purityErr2  ,'purityErr2/D' )
    mcTree.Branch( 'scaleFactorPurUP' ,scaleFactorPurUP ,'scaleFactorPurUP/D' )
    mcTree.Branch( 'scaleFactorPurDN' ,scaleFactorPurDN ,'scaleFactorPurDN/D' )
    mcTree.Branch( 'datamcSF'    ,datamcSF    ,'datamcSF/D' )
    mcTree.Branch( 'datamcSFErr2',datamcSFErr2,'datamcSFErr2/D' )
    mcTree.Branch( 'scaleFactorDMCSFUP' ,scaleFactorDMCSFUP ,'scaleFactorDMCSFUP/D' )
    mcTree.Branch( 'scaleFactorDMCSFDN' ,scaleFactorDMCSFDN ,'scaleFactorDMCSFDN/D' )
    mcTree.Branch( 'totalErr2'   ,totalErr2   ,'totalErr2/D' )
    mcTree.Branch( 'eventWeight',eventWeight,'eventWeight/D' )
    mcTree.Branch( 'puWeight',puWeight,'puWeight/D' )
    
    for event in mcChain:
        if (event.photonPt > 100 and event.photonIsTightIso and event.photonPixelVeto and event.dphi1>0.5 and event.dphi2>0.5 and event.dphi3>0.3 and event.nJetsHT>1):
            if (event.htVal<500 or (event.htVal<800 and event.mhtVal<200)):
                continue
            if not (event.passRA2ElVeto and event.passRA2MuVeto):
                continue

            if myFitBin == 0:
                if (event.mhtVal>100 and event.mhtVal<200):
                    ibin = "bin23"
                elif (event.mhtVal<300):
                    ibin = "bin24"
                elif (event.mhtVal<450):
                    ibin = "bin19"
                else:
                    ibin = "bin21"
            else:
                if (event.mhtVal>100 and event.mhtVal<125):
                    ibin = "bin1"
                elif (event.mhtVal>125 and event.mhtVal<150):
                    ibin = "bin2"
                elif (event.mhtVal>150 and event.mhtVal<175):
                    ibin = "bin3"
                elif (event.mhtVal>175 and event.mhtVal<200):
                    ibin = "bin4"
                elif (event.mhtVal>200 and event.mhtVal<225):
                    ibin = "bin5"
                elif (event.mhtVal>225 and event.mhtVal<250):
                    ibin = "bin6"
                elif (event.mhtVal>250 and event.mhtVal<275):
                    ibin = "bin7"
                elif (event.mhtVal>275 and event.mhtVal<300):
                    ibin = "bin8"
                    
                else:
                ##standard fine binning
                    if myFitBin == 1:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<425):
                            ibin = "bin13"
                        elif (event.mhtVal>425 and event.mhtVal<450):
                            ibin = "bin14"
                        elif (event.mhtVal>450 and event.mhtVal<500):
                            ibin = "bin15"
                        elif (event.mhtVal>500 and event.mhtVal<550):
                            ibin = "bin16"
                        elif (event.mhtVal>550 and event.mhtVal<600):
                            ibin = "bin17"
                        else:
                            ibin = "bin18"
                #####bin coarser for high mht 450-inf
                    elif myFitBin == 2:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<425):
                            ibin = "bin13"
                        elif (event.mhtVal>425 and event.mhtVal<450):
                            ibin = "bin14"
                        else:
                            ibin = "bin21"
                #####bin coarser for high mht 400-450-inf
                    elif myFitBin == 3:
                        if (event.mhtVal>300 and event.mhtVal<325):
                            ibin = "bin9"
                        elif (event.mhtVal>325 and event.mhtVal<350):
                            ibin = "bin10"
                        elif (event.mhtVal>350 and event.mhtVal<375):
                            ibin = "bin11"
                        elif (event.mhtVal>375 and event.mhtVal<400):
                            ibin = "bin12"
                        elif (event.mhtVal>400 and event.mhtVal<450):
                            ibin = "bin27"
                        else:
                            ibin = "bin21"
                #####bin coarser for high mht 300-450-600-inf
                    elif myFitBin == 4:
                        if(event.mhtVal>300 and event.mhtVal<450):
                            ibin = "bin19"
                        elif(event.mhtVal>450 and event.mhtVal<600):
                            ibin = "bin20"
                        else:
                            ibin = "bin18"
                ###bin coarser for high mht 300-450-inf
                    elif myFitBin == 5:
                        if(event.mhtVal>300 and event.mhtVal<450):
                            ibin = "bin19"
                        else:
                            ibin = "bin21"
                ###bin coarser for high mht 300-inf
                    elif myFitBin == 6:
                        ibin = "bin22"
            #
            nJets[0]     = event.nJetsHT
            nPhotons[0]  = event.nPhotonsTight
            mht[0]       = event.mhtVal
            ht[0]        = event.htVal
            photonPt[0]  = event.photonPt
            photonEta[0] = event.photonEta
            photonMinDR[0] = event.photonMinDR
            #
            fitExtrapolation = fitFunctions[ibin]
            fitDataExtrapolation = dataFitFunctions[ibin]
            phenoFactor[0] = fitExtrapolation["pheno"]["func"].Eval(event.nJetsHT)
            #print "computing squared errors on pheno ratio"
            phenoErr2UP[0]   = squaredErrorFromGraph(nJets[0],fitExtrapolation["pheno"],"corrUP")
            phenoErr2DN[0]   = squaredErrorFromGraph(nJets[0],fitExtrapolation["pheno"],"corrDN")
            #print "pheno: %2.4e(+%2.4e/-%2.4e)"%(phenoFactor[0],math.sqrt(phenoErr2UP[0]),math.sqrt(phenoErr2DN[0]))
            #phenoErr2[0]   = pol1FitError2(nJets[0],
            #                               fitExtrapolation["pheno"]["func"],
            #                               fitExtrapolation["pheno"]["cov"])["UP"]
            #print "computing relative squared errors on theory ratio"
            theoryErr2UP[0] = phenoFactor[0]*phenoFactor[0]*squaredRelErrorFromGraph(
                nJets[0],fitDataExtrapolation["pheno"],"corrUP")
            theoryErr2DN[0] = phenoFactor[0]*phenoFactor[0]*squaredRelErrorFromGraph(
                nJets[0],fitDataExtrapolation["pheno"],"corrDN")
            #print "theo. unc: +%2.4e/-%2.4e"%(theoryErr2UP[0],theoryErr2DN[0])

            ## no correction for the data/mc disagreement vs. njets in zmumu/gamma since this is MC
            phenoDataMC[0] = 1.0
            phenoDataMCErr2UP[0] = 0.0
            phenoDataMCErr2DN[0] = 0.0

            ###print "computing squared errors on double ratio"
            ##phenoDataMCErr2UP[0] = phenoFactor[0]*phenoFactor[0]*squaredErrorFromGraph(
            ##    nJets[0],fitDataDouble["double"]["pol1"],"corrSymUP")
            ##phenoDataMCErr2DN[0] = phenoFactor[0]*phenoFactor[0]*squaredErrorFromGraph(
            ##    nJets[0],fitDataDouble["double"]["pol1"],"corrSymDN")
            ###print "data/MC unc.: +%2.4e/-%2.4e"%(phenoDataMCErr2UP[0],phenoDataMCErr2DN[0])
            ###theoryErr2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            ###                                                                fitDataExtrapolation["pheno"]["func"],
            ###                                                                fitDataExtrapolation["pheno"]["cov"])["UP"]
            ###doublePol0Err2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            ###                                                                    fitDoubleExtrapolation["pol0"]["func"],0)
            ###doublePol1Err2[0]  = phenoFactor[0]*phenoFactor[0]*pol1FitRelError2(nJets[0],
            ###                                                                    fitDoubleExtrapolation["pol1"]["func"],
            ###                                                                    fitDoubleExtrapolation["pol1"]["cov"])["UP"]
            if options.debug:
                print "nJets:%d, pheno:%2.4f - phenoErr:%2.2e(%2.2e), theory:%2.2e theoryErr:%2.2e(%2.2e)"%(
                    nJets[0],phenoFactor[0],
                    math.sqrt(phenoErr2[0]),math.sqrt(pol1FitError2(nJets[0],
                                                                    fitExtrapolation["pheno"]["func"],
                                                                    fitExtrapolation["pheno"]["cov"])["UP"]),
                    fitDataExtrapolation["pheno"]["func"].Eval(nJets[0]),
                    math.sqrt(theoryErr2[0]),math.sqrt(fitRelError2(nJets[0],
                                                                    fitDataExtrapolation["pheno"]["func"],
                                                                    fitDataExtrapolation["pheno"]["cov"])["UP"])
                    )
            
            purity[0]       = 1.0##no purity correction for GJets MC
            purityErr2[0]   = 0.0##no purity correction for GJets MC
            datamcSF[0]     = 1.0
            datamcSFErr2[0] = 0.0

            if options.genreco:
                accEff[0]      = fitExtrapolation["acc"]["func"].Eval(nJets[0])
                #print "computing squared errors on acceptance"
                accErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["acc"],"corrUP")
                accErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["acc"],"corrDN")
                #print "acceptance: %2.4e(+%2.4e/-%2.4e)"%(accEff[0],accErr2UP[0],accErr2DN[0])
                #accErr2[0]     = pol1FitError2(nJets[0],
                #                               fitExtrapolation["acc"]["func"],
                #                               fitExtrapolation["acc"]["cov"])["UP"]
                #print "computing squared errors on reco"
                recoEff[0]     = fitExtrapolation["reco"]["func"].Eval(nJets[0])
                recoErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["reco"],"corrUP")
                recoErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["reco"],"corrDN")
                #print "reco: %2.4e(+%2.4e/-%2.4e)"%(recoEff[0],recoErr2UP[0],recoErr2DN[0])
                #recoErr2[0]    = pol1FitError2(nJets[0],
                #                               fitExtrapolation["reco"]["func"],
                #                               fitExtrapolation["reco"]["cov"])["UP"]
                #print "computing squared errors on pixel"
                pixelEff[0]    = fitExtrapolation["pixel"]["func"].Eval(nJets[0])
                pixelErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["pixel"],"corrUP")
                pixelErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["pixel"],"corrDN")
                #print "pixel: %2.4e(+%2.4e/-%2.4e)"%(pixelEff[0],pixelErr2UP[0],pixelErr2DN[0])
                #pixelErr2[0]   = pol1FitError2(nJets[0],
                #                               fitExtrapolation["pixel"]["func"],
                #                               fitExtrapolation["pixel"]["cov"])["UP"]
                #print "computing squared errors on isolation"
                isoEff[0]      = fitExtrapolation["iso"]["func"].Eval(nJets[0])
                isoErr2UP[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["iso"],"corrUP")
                isoErr2DN[0] = squaredErrorFromGraph(nJets[0],fitExtrapolation["iso"],"corrDN")
                #print "isolation: %2.4e(+%2.4e/-%2.4e)"%(isoEff[0],isoErr2UP[0],isoErr2DN[0])
                #isoErr2[0]     = pol1FitError2(nJets[0],
                #                               fitExtrapolation["iso"]["func"],
                #                               fitExtrapolation["iso"]["cov"])["UP"]
            else:
                accEff[0]    = 1.0
                recoEff[0]   = 1.0
                pixelEff[0]  = 1.0
                isoEff[0]    = 1.0
                #accErr2[0]   = 0.0
                #recoErr2[0]  = 0.0
                #pixelErr2[0] = 0.0
                #isoErr2[0]   = 0.0
                accErr2UP[0]   = 0.0
                recoErr2UP[0]  = 0.0
                pixelErr2UP[0] = 0.0
                isoErr2UP[0]   = 0.0
                accErr2DN[0]   = 0.0
                recoErr2DN[0]  = 0.0
                pixelErr2DN[0] = 0.0
                isoErr2DN[0]   = 0.0
                
            scaleFactor[0] = purity[0]*phenoFactor[0]/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ## Calculate the uncertainties
            numVals    = [purity[0],phenoFactor[0],phenoDataMC[0]]
            denVals    = [accEff[0],recoEff[0],pixelEff[0],isoEff[0],datamcSF[0]]

            #pheno up/dn
            numErrs2UP = [0.0,phenoErr2UP[0],0.0]
            numErrs2DN = [0.0,phenoErr2DN[0],0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            
            ##scaleFactorPhenUP[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPhenDN[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPhenUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorPhenDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            #pheno+theory up/dn
            numErrs2UP = [0.0,phenoErr2UP[0]+theoryErr2UP[0],0.0]
            numErrs2DN = [0.0,phenoErr2DN[0]+theoryErr2DN[0],0.0]
            
            ##scaleFactorPhenThUP[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPhenThDN[0]    = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPhenThUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorPhenThDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            ####pheno + theory + data/mc up/dn
            ###numErrs2UP = [0.0,phenoErr2UP[0]+theoryErr2UP[0],phenoDataMCErr2UP[0]]
            ###numErrs2DN = [0.0,phenoErr2DN[0]+theoryErr2DN[0],phenoDataMCErr2DN[0]]
            ###
            #####scaleFactorPhenDataMCUP[0]    = purity[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenDataMCDN[0]    = purity[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenThUP[0]    = purity[0]*(phenoFactor[0]+math.sqrt(phenoErr2UP[0]+theoryErr2UP[0]+phenoDataMCErr2UP[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            #####scaleFactorPhenThDN[0]    = purity[0]*(phenoFactor[0]-math.sqrt(phenoErr2DN[0]+theoryErr2DN[0]+phenoDataMCErr2DN[0]))/(
            #####    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ###
            ###scaleFactorPhenThDataMCUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
            ###                                                                  denVals,denErrs2UP))
            ###scaleFactorPhenThDataMCDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
            ###                                                                  denVals,denErrs2DN))

            #purity up/dn
            numErrs2UP = [purityErr2UP[0],0.0,0.0]
            numErrs2DN = [purityErr2DN[0],0.0,0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            ##scaleFactorPurUP[0]    = (purity[0]+math.sqrt(purityErr2UP[0]))*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorPurDN[0]    = (purity[0]-math.sqrt(purityErr2DN[0]))*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorPurUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorPurDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #acc up/dn
            numErrs2UP = [0.0,0.0,0.0]
            numErrs2DN = [0.0,0.0,0.0]
            
            denErrs2UP = [accErr2UP[0],       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [accErr2DN[0],       0.0,        0.0,      0.0,        0.0]
            ##scaleFactorAccUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    (accEff[0]+math.sqrt(accErr2UP[0]))*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorAccDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    (accEff[0]-math.sqrt(accErr2DN[0]))*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorAccUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorAccDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #reco id up/dn
            denErrs2UP = [0.0,recoErr2UP[0],        0.0,      0.0,        0.0]
            denErrs2DN = [0.0,recoErr2DN[0],        0.0,      0.0,        0.0]
            ##scaleFactorIDUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*(recoEff[0]+math.sqrt(recoErr2UP[0]))*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorIDDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*(recoEff[0]-math.sqrt(recoErr2DN[0]))*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorIDUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorIDDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #pixel veto up/dn
            denErrs2UP = [0.0,       0.0,pixelErr2UP[0],      0.0,        0.0]
            denErrs2DN = [0.0,       0.0,pixelErr2DN[0],      0.0,        0.0]
            ##scaleFactorPixUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*(pixelEff[0]+math.sqrt(pixelErr2UP[0]))*isoEff[0])
            ##scaleFactorPixDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*(pixelEff[0]-math.sqrt(pixelErr2DN[0]))*isoEff[0])
            scaleFactorPixUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorPixDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #isolation up/dn
            denErrs2UP = [0.0,       0.0,        0.0,isoErr2UP[0],        0.0]
            denErrs2DN = [0.0,       0.0,        0.0,isoErr2DN[0],        0.0]
            ##scaleFactorIsoUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*(isoEff[0]+math.sqrt(isoErr2UP[0])))
            ##scaleFactorIsoDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*(isoEff[0]-math.sqrt(isoErr2DN[0])))
            scaleFactorIsoUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorIsoDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            #data/mc s.f. up/dn
            denErrs2UP = [0.0,       0.0,        0.0,      0.0,datamcSFErr2[0]]
            denErrs2DN = [0.0,       0.0,        0.0,      0.0,datamcSFErr2[0]]
            ##scaleFactorDMCSFUP[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*(datamcSF[0]+math.sqrt(datamcSFErr2[0]))*pixelEff[0]*isoEff[0])
            ##scaleFactorDMCSFDN[0]    = purity[0]*phenoFactor[0]*phenoDataMC[0]/(
            ##    accEff[0]*recoEff[0]*(datamcSF[0]-math.sqrt(datamcSFErr2[0]))*pixelEff[0]*isoEff[0])
            scaleFactorDMCSFUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorDMCSFDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))
            
            
            ### do the variation of the scale factor not including the zmumu/gamma fit and the 
            ## data/mc correction uncertainty
            numErrs2UP = [purityErr2UP[0],phenoErr2UP[0],0.0]
            numErrs2DN = [purityErr2DN[0],phenoErr2DN[0],0.0]
            
            denErrs2UP = [accErr2UP[0],recoErr2UP[0],pixelErr2UP[0],isoErr2UP[0],datamcSFErr2[0]]
            denErrs2DN = [accErr2DN[0],recoErr2DN[0],pixelErr2DN[0],isoErr2DN[0],datamcSFErr2[0]]
            
            scaleFactorUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))
            
            ## do the variation of the pheno zmumu error only
            numErrs2UP = [0.0      ,theoryErr2UP[0],           0.0]
            numErrs2DN = [0.0      ,theoryErr2DN[0],           0.0]
            
            denErrs2UP = [      0.0,       0.0,        0.0,      0.0,        0.0]
            denErrs2DN = [      0.0,       0.0,        0.0,      0.0,        0.0]
            
            ##scaleFactorThFitUP[0]  = purity[0]*phenoDataMC[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThFitDN[0]  = purity[0]*phenoDataMC[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])

            scaleFactorThFitUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                              denVals,denErrs2UP))
            scaleFactorThFitDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                              denVals,denErrs2DN))

            ## do the variation of the pheno data/mc correction only
            numErrs2UP = [0.0,0.0,phenoDataMCErr2UP[0]]
            numErrs2DN = [0.0,0.0,phenoDataMCErr2DN[0]]

            ##scaleFactorThDoubleUP[0]  = purity[0]*phenoFactor[0]*(phenoDataMC[0]+math.sqrt(phenoDataMCErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDoubleDN[0]  = purity[0]*phenoFactor[0]*(phenoDataMC[0]-math.sqrt(phenoDataMCErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            scaleFactorThDoubleUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                      denVals,denErrs2UP))
            scaleFactorThDoubleDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                      denVals,denErrs2DN))

            ##scaleFactorThDoubleUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(phenoDataMCErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDoubleDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(phenoDataMCErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            

            ## do the variation of both zmumu/gamma fit and double ratio uncertainty
            numErrs2UP = [0.0,theoryErr2UP[0],phenoDataMCErr2UP[0]]
            numErrs2DN = [0.0,theoryErr2DN[0],phenoDataMCErr2DN[0]]
            
            ##scaleFactorThUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0]+phenoDataMCErr2UP[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0]+phenoDataMCErr2DN[0])
            ##                                 )/(accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThUP[0]  = purity[0]*(phenoFactor[0]+math.sqrt(theoryErr2UP[0]))*(
            ##    phenoDataMC[0]+math.sqrt(phenoDataMCErr2UP[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            ##scaleFactorThDN[0]  = purity[0]*(phenoFactor[0]-math.sqrt(theoryErr2DN[0]))*(
            ##    phenoDataMC[0]-math.sqrt(phenoDataMCErr2DN[0]))/(
            ##    accEff[0]*recoEff[0]*datamcSF[0]*pixelEff[0]*isoEff[0])
            
            scaleFactorThUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                denVals,denErrs2UP))
            scaleFactorThDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                denVals,denErrs2DN))

            
            ### do the total variation from all systematic sources
            ##numErrs2UP = [purityErr2UP[0],phenoErr2UP[0]+theoryErr2UP[0]+phenoDataMCErr2UP[0]]
            ##numErrs2DN = [purityErr2DN[0],phenoErr2DN[0]+theoryErr2DN[0]+phenoDataMCErr2DN[0]]
            numErrs2UP = [purityErr2UP[0],phenoErr2UP[0]+theoryErr2UP[0],phenoDataMCErr2UP[0]]
            numErrs2DN = [purityErr2DN[0],phenoErr2DN[0]+theoryErr2DN[0],phenoDataMCErr2DN[0]]
            
            denErrs2UP = [accErr2UP[0],recoErr2UP[0],pixelErr2UP[0],isoErr2UP[0],datamcSFErr2[0]]
            denErrs2DN = [accErr2DN[0],recoErr2DN[0],pixelErr2DN[0],isoErr2DN[0],datamcSFErr2[0]]
            
            scaleFactorTotUP[0]    = scaleFactor[0] + math.sqrt(ratioTotalError2(numVals,numErrs2UP,
                                                                                 denVals,denErrs2UP))
            scaleFactorTotDN[0]    = scaleFactor[0] - math.sqrt(ratioTotalError2(numVals,numErrs2DN,
                                                                                 denVals,denErrs2DN))

            eventWeight[0] = 19.4/10*event.eventWt
            puWeight[0]    = event.puWt
            print "mc::ht:%2.2f, mht:%2.2f, nJets:%d, nPhotons:%d, photonPt:%2.2f, photonEta:%2.2f, photonMinDR:%2.2f -- scaleFactor:%2.4f"%(
                event.htVal,event.mhtVal,event.nJetsHT,event.nPhotonsTight,event.photonPt,event.photonEta,event.photonMinDR,scaleFactor[0])
            print "mc::pheno:%2.4f(%2.4f[%2.4f]{%2.4f}), accEff:%2.4f(%2.4f), recoEff:%2.4f(%2.4f),  pixelEff:%2.4f(%2.4f),  isoEff:%2.4f(%2.4f)"%(
                phenoFactor[0],math.sqrt(phenoErr2UP[0]),math.sqrt(theoryErr2UP[0]),math.sqrt(phenoDataMCErr2UP[0]),
                accEff[0],math.sqrt(accErr2UP[0]),
                recoEff[0],math.sqrt(recoErr2UP[0]),
                pixelEff[0],math.sqrt(pixelErr2UP[0]),
                isoEff[0],math.sqrt(isoErr2UP[0]))
            print "UP:%2.2e, DN:%2.2e, thUP:%2.2e, thDN:%2.2e,  totUP:%2.2e, totDN:%2.2e\n"%(scaleFactorUP[0],
                                                                                           scaleFactorDN[0],
                                                                                           scaleFactorThUP[0],
                                                                                           scaleFactorThDN[0],
                                                                                           scaleFactorTotUP[0],
                                                                                           scaleFactorTotDN[0],
                                                                        )
    
            mcTree.Fill()
    
    mcTree.Write()
    
    ##zjets tree
    zinvChain = r.TChain("reco")
    zinvChain.Add("%s/recoTreeDR0.0_zinv.root"%(options.inDir))
    zinvTree = r.TTree('zinv', 'tree for zinv ')
    
    nJets[0] = 0
    ht[0]  = 0.0
    mht[0] = 0.0
    scaleFactor[0] = 1.0
    eventWeight[0] = 1.0
    puWeight[0] = 1.0
    
    zinvTree.Branch( 'nJets',    nJets,    'nJets/I' )
    zinvTree.Branch( 'ht',       ht,       'ht/D' )
    zinvTree.Branch( 'mht',      mht,      'mht/D' )
    zinvTree.Branch( 'scaleFactor',scaleFactor,'scaleFactor/D' )
    zinvTree.Branch( 'eventWeight',eventWeight,'eventWeight/D' )
    zinvTree.Branch( 'puWeight',puWeight,'puWeight/D' )
    
    for event in zinvChain:
        if (event.dphi1>0.5 and event.dphi2>0.5 and event.dphi3>0.3 and event.nJetsHT>1):
            if (event.htVal<500 or (event.htVal<800 and event.mhtVal<200)):
                continue
            if not (event.passRA2ElVeto and event.passRA2MuVeto):
                continue
            nJets[0]     = event.nJetsHT
            mht[0]       = event.mhtVal
            ht[0]        = event.htVal
            scaleFactor[0] = 1.0
            eventWeight[0] = 19.4/10*event.eventWt
            puWeight[0]    = event.puWt
            print "zinvisible::ht:%2.2f, mht:%2.2f, nJets:%d -- scaleFactor:%2.4f"%(
                event.htVal,event.mhtVal,event.nJetsHT,scaleFactor[0])
            zinvTree.Fill()
    
    zinvTree.Write()
    outputFile.Write()
    outputFile.Close()
    inputFile.Close()

##########################
def fitError2(nJets,fitFunction) :
    y = fitFunction.Eval(nJets)
    p0  = fitFunction.GetParameter(0)
    dp0 = fitFunction.GetParError(0)
    p1  = fitFunction.GetParameter(1)
    dp1 = fitFunction.GetParError(1)
    
    dyp1 = y*(dp1/p1)
    dy2 = dyp1*dyp1+(dp0*dp0)
    #print "fitError2::y(%2.2e+/-%2.2e) = p0(%2.2e+/-%2.2e)+x(%d)*p1(%2.2e+/-%2.2e)"%(
    #y,math.sqrt(dy2),p0,dp0,nJets,p1,dp1)
    return dy2

################
def fitRelError2(nJets,fitFunction) :
    ## y = mx+b
    ## (dy/y)^2 = (dm/m)^2+(db/b)^2
    y = fitFunction.Eval(nJets)
    p0  = fitFunction.GetParameter(0)
    dp0 = fitFunction.GetParError(0)
    p1  = fitFunction.GetParameter(1)
    dp1 = fitFunction.GetParError(1)
    
    dyp0 = (dp0/p0)
    dyp1 = (dp1/p1)
    dy2 = dyp1*dyp1+(dyp0*dyp0)
    #print "fitRelError2::y(%2.2e+/-%2.2e) = p0(%2.2e+/-%2.2e)+x(%d)*p1(%2.2e+/-%2.2e)"%(
    #y,math.sqrt(dy2/(y*y)),p0,dp0,nJets,p1,dp1)
    return dy2/(y*y)

################
def pol1FitError2(nJets,fitFunction,covp0p1) :
    #print nJets,covp0p1
    y = fitFunction.Eval(nJets)
    p0  = fitFunction.GetParameter(0)
    dp0 = fitFunction.GetParError(0)
    p1  = fitFunction.GetParameter(1)
    dp1 = fitFunction.GetParError(1)
    #print y,p0,dp0,p1,dp1
    dyp0 = dp0
    dyp1 = nJets*dp1
    dy2 = dyp1*dyp1+(dp0*dp0)
    dy2UP = dy2+(2*nJets*covp0p1)
    dy2DN = dy2-(2*nJets*covp0p1)
    #print "pol1FitError2::y(%2.2e+/-%2.2e) = p0(%2.2e+/-%2.2e)+x(%d)*p1(%2.2e+/-%2.2e)"%(
    #y,math.sqrt(dy2),p0,dp0,nJets,p1,dp1)
    dy2full = {"uncorr":dy2,
               "UP":dy2UP,
               "DN":dy2DN}
    ##print dy2full
    #passSensible = False
    #if (y+math.sqrt(dy2UP)>y) and (y-math.sqrt(dy2UP)<y):
    #    passSensible = True
    #print "%d  %2.4f  %2.4f  %2.4f  %2.2e  %2.2e  %2.2e %d"%(
    #    nJets, y, y+math.sqrt(dy2UP), y-math.sqrt(dy2UP), covp0p1, math.sqrt(dy2), math.sqrt(dy2UP),
    #    passSensible)
    return dy2full

################
def pol1FitRelError2(nJets,fitFunction,covp0p1) :
    y = fitFunction.Eval(nJets)
    dy2full = pol1FitError2(nJets,fitFunction,covp0p1)
    dy2   = dy2full["uncorr"]
    dy2UP = dy2full["UP"]
    dy2DN = dy2full["DN"]
    reldy2full = {"uncorr":dy2/(y*y),
                  "UP":dy2UP/(y*y),
                  "DN":dy2DN/(y*y)}
    return reldy2full

################
def product2(vals) :
    ##computes the total product squared with components 'vals' 
    totalVal2 = 1
    for val in vals:
        totalVal2 = totalVal2*(val*val)
    return totalVal2
################
def productError2(vals,errs2) :
    ##computes the total squared error on a product with components 'vals' 
    ## and associated squared errors 'errs2'
    totalErr2 = 0
    for val,err2 in itertools.izip(vals,errs2):
        #print val,err2
        totalVal2 = product2(vals)
        totalErr2 = totalErr2 + err2*totalVal2/(val*val)
    return totalErr2

################
def ratioTotalError2(numVals,numErrs2,denVals,denErrs2) :
    ##reads in the components of the ratio and their errors and 
    ## computes the total squared error
    numTotalErr2 = productError2(numVals,numErrs2)
    numProd2 = product2(numVals)

    denTotalErr2 = productError2(denVals,denErrs2)
    denProd2 = product2(denVals)

    ratioTotErr2 = (numTotalErr2/denProd2) + (denTotalErr2/numProd2)
    return ratioTotErr2

################
def makeNJetErrorBands(nJetBins,symVal,fitFunction,covp0p1):
    yvals = {}
    yvals["UP"] = {}
    yvals["DN"] = {}
    yvals["uncUP"] = {}
    yvals["uncDN"] = {}

    yvals["UP"]["raw"] = []
    yvals["UP"]["sym"] = []
    yvals["DN"]["raw"] = []
    yvals["DN"]["sym"] = []

    yvals["uncUP"]["raw"] = []
    yvals["uncUP"]["sym"] = []
    yvals["uncDN"]["raw"] = []
    yvals["uncDN"]["sym"] = []
    #print "nJets", "y","y+err", "y-err", "covp0p1", "sqrt(dy2)", "sqrt(dy2UP)"
    print "deltaY, symVal, fitFunction.Eval(jet),math.sqrt(pol1Error[\"UP\"]),math.sqrt(pol1Error[\"uncorr\"])"
    for jet in range(nJetBins):
        pol1Error = pol1FitError2(jet,fitFunction,covp0p1)
        #pol1Error = pol1FitError2(jet,fitFunction,covp0p1)["UP"]
        #yvals["UP"   ]["raw"].append(fitFunction.Eval(jet)+math.sqrt(pol1Error["UP"]))
        yvals["UP"   ]["raw"].append(fitFunction.Eval(jet)+math.sqrt(pol1Error["UP"]))
        yvals["DN"   ]["raw"].append(fitFunction.Eval(jet)-math.sqrt(pol1Error["UP"]))
        yvals["uncUP"]["raw"].append(fitFunction.Eval(jet)+math.sqrt(pol1Error["uncorr"]))
        yvals["uncDN"]["raw"].append(fitFunction.Eval(jet)-math.sqrt(pol1Error["uncorr"]))
        deltaY = fitFunction.Eval(jet) - symVal
        print deltaY, symVal, fitFunction.Eval(jet),math.sqrt(pol1Error["UP"]),math.sqrt(pol1Error["uncorr"])
        yvals["UP"   ]["sym"].append(symVal+(math.sqrt(pol1Error["UP"]    )+abs(deltaY)))
        yvals["uncUP"]["sym"].append(symVal+(math.sqrt(pol1Error["uncorr"])+abs(deltaY)))
        yvals["DN"   ]["sym"].append(symVal-(math.sqrt(pol1Error["UP"]    )+abs(deltaY)))
        yvals["uncDN"]["sym"].append(symVal-(math.sqrt(pol1Error["uncorr"])+abs(deltaY)))
        #if deltaY > 0:
        #    yvals["UP"   ]["sym"].append(fitFunction.Eval(jet)+math.sqrt(pol1Error["UP"]))
        #    yvals["uncUP"]["sym"].append(fitFunction.Eval(jet)+math.sqrt(pol1Error["uncorr"]))
        #    ##yvals["DN"   ]["sym"].append(fitFunction.Eval(jet)-math.sqrt(pol1Error["UP"])    -(2*deltaY))
        #    ##yvals["uncDN"]["sym"].append(fitFunction.Eval(jet)-math.sqrt(pol1Error["uncorr"])-(2*deltaY))
        #    yvals["DN"   ]["sym"].append(symVal-(math.sqrt(pol1Error["UP"]    )+deltaY))
        #    yvals["uncDN"]["sym"].append(symVal-(math.sqrt(pol1Error["uncorr"])+deltaY))
        #else:
        #    ##yvals["UP"   ]["sym"].append(fitFunction.Eval(jet)+math.sqrt(pol1Error["UP"])    -(2*deltaY))
        #    ##yvals["uncUP"]["sym"].append(fitFunction.Eval(jet)+math.sqrt(pol1Error["uncorr"])-(2*deltaY))
        #    yvals["UP"   ]["sym"].append(symVal-(math.sqrt(pol1Error["UP"]    )+deltaY))
        #    yvals["uncUP"]["sym"].append(symVal-(math.sqrt(pol1Error["uncorr"])+deltaY))
        #    yvals["DN"   ]["sym"].append(fitFunction.Eval(jet)-math.sqrt(pol1Error["UP"]))
        #    yvals["uncDN"]["sym"].append(fitFunction.Eval(jet)-math.sqrt(pol1Error["uncorr"]))
    return yvals
################
def squaredErrorFromGraph(nJets,graphSet,correction):
    #print graphSet
    #print graphSet["func"]

    #print "using %s correction for error"%(correction)
    y = graphSet["func"].Eval(nJets)
    #print "f(nJets=%d) = %2.4e"%(nJets,y)
    #print "f(nJets=%d)+error = %2.4e"%(nJets,graphSet[correction].Eval(nJets))
    dy = abs(y-graphSet[correction].Eval(nJets))
    #print "dy = %2.4e"%(dy)
    
    return dy*dy

################
def squaredRelErrorFromGraph(nJets,graphSet,correction):
    y = graphSet["func"].Eval(nJets)
    #print "f(nJets=%d) = %2.4e"%(nJets,y)
    #print "using %s correction for relative error"%(correction)
    #dy = abs(y-graphSet[correction].Eval(nJets))
    errSq = squaredErrorFromGraph(nJets,graphSet,correction)
    relErr2 = errSq/(y*y)
    #print "err2:%2.4e, relErr2:%2.4e"%(errSq,relErr2)
    return relErr2

################
def dataMCSF(eta):
    datamcsf = {}
    if abs(eta) < 0.8:
        datamcsf["cv"] = 0.9725
        datamcsf["stat"] = 0.0030
        datamcsf["syst"] = 0.0013
    elif abs(eta) < 1.4442:
        datamcsf["cv"] = 0.9826
        datamcsf["stat"] = 0.0039
        datamcsf["syst"] = 0.0002
    elif abs(eta) < 2.0:
        datamcsf["cv"] = 1.0057
        datamcsf["stat"] = 0.0054
        datamcsf["syst"] = 0.0002
    else:# abs(eta) < 2.5:
        datamcsf["cv"] = 1.0133
        datamcsf["stat"] = 0.0057
        datamcsf["syst"] = 0.0005

    return datamcsf

####very end####
if __name__ == '__main__':
    main()

