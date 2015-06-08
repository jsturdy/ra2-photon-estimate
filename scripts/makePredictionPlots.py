import sys,os
import ROOT as r
from array import array
import math
import optparse
from specialFunctions import mkdir_p

########Main
def main() :
    parser = optparse.OptionParser(description="Driver parameters for makeGenRatioPlots.py")
    parser.add_option('-d', '--debug',   action="store_true", default=False, dest="debug")
    parser.add_option('-z', '--zmumuMC', action="store_true", default=False, dest="zmumuMC")
    parser.add_option('-g', '--genreco', action="store_true", default=False, dest="genreco")
    parser.add_option('-o', '--outDir',  type='string', action="store", default="/tmp", dest="outDir")
    parser.add_option('-i', '--inDir',   type='string', action="store", default="/tmp", dest="inDir")
    parser.add_option('-s', '--sample',  type='string', action="store", default="data", dest="sample")
    parser.add_option('-b', '--fitBin',  type='int',    action="store", default=0, dest="fitBin")
    parser.add_option('-r', '--fitRange',type='int',    action="store", default=2, dest="fitRange")

    options, args = parser.parse_args()

    r.gROOT.SetBatch(True)
    mkdir_p("%s"%(options.outDir))

    myWorkingDir = os.getcwd()

    goodFitBins = [0,1,2,3,4,5,6]
    myFitBin = options.fitBin
    if options.fitBin not in goodFitBins:
        print "invalid option for fit bins, using default 0"
        myFitBin = 0

    extra = "gen"
    if options.genreco:
        extra = "gen"
    else:
        extra = "reco"

    zmumuextra = "zmumuGammaData"
    if options.zmumuMC:
        zmumuextra = "zmumuGammaMC"

    outFile = "%s/%s_%s_predictions_%dto8_bin%d_%s_new.root"%(options.outDir,
                                                              options.sample,
                                                              extra,
                                                              options.fitRange,myFitBin,
                                                              zmumuextra)
    print outFile
    outputFile = r.TFile("%s"%(outFile),"RECREATE")
    
    lowjetHTBins  = [400,500,800,1000,1250,1500,3000]
    lowjetMHTBins = [50,100,200,300,450,600,1000]

    midjetHTBins  = [400,500,800,1000,1250,1500,3000]
    midjetMHTBins = [50,100,200,300,450,1000]

    highjetHTBins  = [400,500,800,1000,1250,1500,3000]
    highjetMHTBins = [50,100,200,1000]

    htvsmht_raw_2plus = r.TH2D("htvsmht_raw_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
    htvsmht_raw_3plus = r.TH2D("htvsmht_raw_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
    htvsmht_raw_2jets = r.TH2D("htvsmht_raw_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
    htvsmht_raw_3to5  = r.TH2D("htvsmht_raw_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
    htvsmht_raw_6to7  = r.TH2D("htvsmht_raw_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
    htvsmht_raw_8plus = r.TH2D("htvsmht_raw_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
    htvsmht_scaled_2plus = r.TH2D("htvsmht_scaled_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
    htvsmht_scaled_3plus = r.TH2D("htvsmht_scaled_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
    htvsmht_scaled_2jets = r.TH2D("htvsmht_scaled_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
    htvsmht_scaled_3to5  = r.TH2D("htvsmht_scaled_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
    htvsmht_scaled_6to7  = r.TH2D("htvsmht_scaled_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
    htvsmht_scaled_8plus = r.TH2D("htvsmht_scaled_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))

    htvsmht_raw_2plus.Sumw2()
    htvsmht_raw_3plus.Sumw2()
    htvsmht_raw_2jets.Sumw2()
    htvsmht_raw_3to5 .Sumw2()
    htvsmht_raw_6to7 .Sumw2()
    htvsmht_raw_8plus.Sumw2()
    
    htvsmht_scaled_2plus.Sumw2()
    htvsmht_scaled_3plus.Sumw2()
    htvsmht_scaled_2jets.Sumw2()
    htvsmht_scaled_3to5 .Sumw2()
    htvsmht_scaled_6to7 .Sumw2()
    htvsmht_scaled_8plus.Sumw2()

    mht_raw_2plus = r.TH1D("mht_raw_2jet" ,"#slashH_{T}",30,0,1500)
    mht_raw_3plus = r.TH1D("mht_raw_3jet" ,"#slashH_{T}",30,0,1500)
    mht_raw_2jets = r.TH1D("mht_raw_dijet","#slashH_{T}",30,0,1500)
    mht_raw_3to5  = r.TH1D("mht_raw_3to5" ,"#slashH_{T}",30,0,1500)
    mht_raw_6to7  = r.TH1D("mht_raw_6to7" ,"#slashH_{T}",30,0,1500)
    mht_raw_8plus = r.TH1D("mht_raw_8jet" ,"#slashH_{T}",30,0,1500)
    
    mht_scaled_2plus = r.TH1D("mht_scaled_2jet" ,"#slashH_{T}",30,0,1500)
    mht_scaled_3plus = r.TH1D("mht_scaled_3jet" ,"#slashH_{T}",30,0,1500)
    mht_scaled_2jets = r.TH1D("mht_scaled_dijet","#slashH_{T}",30,0,1500)
    mht_scaled_3to5  = r.TH1D("mht_scaled_3to5" ,"#slashH_{T}",30,0,1500)
    mht_scaled_6to7  = r.TH1D("mht_scaled_6to7" ,"#slashH_{T}",30,0,1500)
    mht_scaled_8plus = r.TH1D("mht_scaled_8jet" ,"#slashH_{T}",30,0,1500)

    mht_raw_2plus.Sumw2()
    mht_raw_3plus.Sumw2()
    mht_raw_2jets.Sumw2()
    mht_raw_3to5 .Sumw2()
    mht_raw_6to7 .Sumw2()
    mht_raw_8plus.Sumw2()
    
    mht_scaled_2plus.Sumw2()
    mht_scaled_3plus.Sumw2()
    mht_scaled_2jets.Sumw2()
    mht_scaled_3to5 .Sumw2()
    mht_scaled_6to7 .Sumw2()
    mht_scaled_8plus.Sumw2()

    ht_raw_2plus = r.TH1D("ht_raw_2jet" ,"H_{T}",30,0,3000)
    ht_raw_3plus = r.TH1D("ht_raw_3jet" ,"H_{T}",30,0,3000)
    ht_raw_2jets = r.TH1D("ht_raw_dijet","H_{T}",30,0,3000)
    ht_raw_3to5  = r.TH1D("ht_raw_3to5" ,"H_{T}",30,0,3000)
    ht_raw_6to7  = r.TH1D("ht_raw_6to7" ,"H_{T}",30,0,3000)
    ht_raw_8plus = r.TH1D("ht_raw_8jet" ,"H_{T}",30,0,3000)
    
    ht_scaled_2plus = r.TH1D("ht_scaled_2jet" ,"H_{T}",30,0,3000)
    ht_scaled_3plus = r.TH1D("ht_scaled_3jet" ,"H_{T}",30,0,3000)
    ht_scaled_2jets = r.TH1D("ht_scaled_dijet","H_{T}",30,0,3000)
    ht_scaled_3to5  = r.TH1D("ht_scaled_3to5" ,"H_{T}",30,0,3000)
    ht_scaled_6to7  = r.TH1D("ht_scaled_6to7" ,"H_{T}",30,0,3000)
    ht_scaled_8plus = r.TH1D("ht_scaled_8jet" ,"H_{T}",30,0,3000)

    ht_raw_2plus.Sumw2()
    ht_raw_3plus.Sumw2()
    ht_raw_2jets.Sumw2()
    ht_raw_3to5 .Sumw2()
    ht_raw_6to7 .Sumw2()
    ht_raw_8plus.Sumw2()
    
    ht_scaled_2plus.Sumw2()
    ht_scaled_3plus.Sumw2()
    ht_scaled_2jets.Sumw2()
    ht_scaled_3to5 .Sumw2()
    ht_scaled_6to7 .Sumw2()
    ht_scaled_8plus.Sumw2()

    njets_raw_htinc = r.TH1D("njets_raw_ht500toinf" ,"N_{Jets}",15,-0.5,14.5)
    njets_raw_ht5to8 = r.TH1D("njets_raw_ht500to800" ,"N_{Jets}",15,-0.5,14.5)
    njets_raw_ht8to10 = r.TH1D("njets_raw_ht800to1000","N_{Jets}",15,-0.5,14.5)
    njets_raw_ht10to125  = r.TH1D("njets_raw_ht1000to1250" ,"N_{Jets}",15,-0.5,14.5)
    njets_raw_ht125to15  = r.TH1D("njets_raw_ht1250to1500" ,"N_{Jets}",15,-0.5,14.5)
    njets_raw_ht15to30 = r.TH1D("njets_raw_ht1500toinf" ,"N_{Jets}",15,-0.5,14.5)
    
    njets_scaled_htinc = r.TH1D("njets_scaled_ht500toinf" ,"N_{Jets}",15,-0.5,14.5)
    njets_scaled_ht5to8 = r.TH1D("njets_scaled_ht500to800" ,"N_{Jets}",15,-0.5,14.5)
    njets_scaled_ht8to10 = r.TH1D("njets_scaled_ht800to1000","N_{Jets}",15,-0.5,14.5)
    njets_scaled_ht10to125  = r.TH1D("njets_scaled_ht1000to1250" ,"N_{Jets}",15,-0.5,14.5)
    njets_scaled_ht125to15  = r.TH1D("njets_scaled_ht1250to1500" ,"N_{Jets}",15,-0.5,14.5)
    njets_scaled_ht15to30 = r.TH1D("njets_scaled_ht1500toinf" ,"N_{Jets}",15,-0.5,14.5)

    njets_raw_htinc.Sumw2()
    njets_raw_ht5to8.Sumw2()
    njets_raw_ht8to10.Sumw2()
    njets_raw_ht10to125.Sumw2()
    njets_raw_ht125to15.Sumw2()
    njets_raw_ht15to30.Sumw2()
    
    njets_scaled_htinc.Sumw2()
    njets_scaled_ht5to8.Sumw2()
    njets_scaled_ht8to10.Sumw2()
    njets_scaled_ht10to125.Sumw2()
    njets_scaled_ht125to15.Sumw2()
    njets_scaled_ht15to30.Sumw2()

    if not options.sample=="zinv":
        htvsmht_prediction_2plus = r.TH2D("htvsmht_prediction_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_prediction_3plus = r.TH2D("htvsmht_prediction_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_prediction_2jets = r.TH2D("htvsmht_prediction_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_prediction_3to5  = r.TH2D("htvsmht_prediction_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_prediction_6to7  = r.TH2D("htvsmht_prediction_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_prediction_8plus = r.TH2D("htvsmht_prediction_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_prediction_2plus.Sumw2()
        htvsmht_prediction_3plus.Sumw2()
        htvsmht_prediction_2jets.Sumw2()
        htvsmht_prediction_3to5 .Sumw2()
        htvsmht_prediction_6to7 .Sumw2()
        htvsmht_prediction_8plus.Sumw2()

        htvsmht_predictionSystUP_2plus = r.TH2D("htvsmht_predictionSystUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionSystUP_3plus = r.TH2D("htvsmht_predictionSystUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionSystUP_2jets = r.TH2D("htvsmht_predictionSystUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionSystUP_3to5  = r.TH2D("htvsmht_predictionSystUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionSystUP_6to7  = r.TH2D("htvsmht_predictionSystUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionSystUP_8plus = r.TH2D("htvsmht_predictionSystUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionSystUP_2plus.Sumw2()
        htvsmht_predictionSystUP_3plus.Sumw2()
        htvsmht_predictionSystUP_2jets.Sumw2()
        htvsmht_predictionSystUP_3to5 .Sumw2()
        htvsmht_predictionSystUP_6to7 .Sumw2()
        htvsmht_predictionSystUP_8plus.Sumw2()

        htvsmht_predictionSystDN_2plus = r.TH2D("htvsmht_predictionSystDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionSystDN_3plus = r.TH2D("htvsmht_predictionSystDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionSystDN_2jets = r.TH2D("htvsmht_predictionSystDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionSystDN_3to5  = r.TH2D("htvsmht_predictionSystDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionSystDN_6to7  = r.TH2D("htvsmht_predictionSystDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionSystDN_8plus = r.TH2D("htvsmht_predictionSystDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionSystDN_2plus.Sumw2()
        htvsmht_predictionSystDN_3plus.Sumw2()
        htvsmht_predictionSystDN_2jets.Sumw2()
        htvsmht_predictionSystDN_3to5 .Sumw2()
        htvsmht_predictionSystDN_6to7 .Sumw2()
        htvsmht_predictionSystDN_8plus.Sumw2()

        htvsmht_predictionTheoryUP_2plus = r.TH2D("htvsmht_predictionTheoryUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTheoryUP_3plus = r.TH2D("htvsmht_predictionTheoryUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTheoryUP_2jets = r.TH2D("htvsmht_predictionTheoryUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTheoryUP_3to5  = r.TH2D("htvsmht_predictionTheoryUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTheoryUP_6to7  = r.TH2D("htvsmht_predictionTheoryUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionTheoryUP_8plus = r.TH2D("htvsmht_predictionTheoryUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionTheoryUP_2plus.Sumw2()
        htvsmht_predictionTheoryUP_3plus.Sumw2()
        htvsmht_predictionTheoryUP_2jets.Sumw2()
        htvsmht_predictionTheoryUP_3to5 .Sumw2()
        htvsmht_predictionTheoryUP_6to7 .Sumw2()
        htvsmht_predictionTheoryUP_8plus.Sumw2()

        htvsmht_predictionTheoryDN_2plus = r.TH2D("htvsmht_predictionTheoryDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTheoryDN_3plus = r.TH2D("htvsmht_predictionTheoryDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTheoryDN_2jets = r.TH2D("htvsmht_predictionTheoryDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTheoryDN_3to5  = r.TH2D("htvsmht_predictionTheoryDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTheoryDN_6to7  = r.TH2D("htvsmht_predictionTheoryDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionTheoryDN_8plus = r.TH2D("htvsmht_predictionTheoryDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionTheoryDN_2plus.Sumw2()
        htvsmht_predictionTheoryDN_3plus.Sumw2()
        htvsmht_predictionTheoryDN_2jets.Sumw2()
        htvsmht_predictionTheoryDN_3to5 .Sumw2()
        htvsmht_predictionTheoryDN_6to7 .Sumw2()
        htvsmht_predictionTheoryDN_8plus.Sumw2()

        htvsmht_predictionTotalUP_2plus = r.TH2D("htvsmht_predictionTotalUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTotalUP_3plus = r.TH2D("htvsmht_predictionTotalUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTotalUP_2jets = r.TH2D("htvsmht_predictionTotalUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTotalUP_3to5  = r.TH2D("htvsmht_predictionTotalUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTotalUP_6to7  = r.TH2D("htvsmht_predictionTotalUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionTotalUP_8plus = r.TH2D("htvsmht_predictionTotalUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionTotalUP_2plus.Sumw2()
        htvsmht_predictionTotalUP_3plus.Sumw2()
        htvsmht_predictionTotalUP_2jets.Sumw2()
        htvsmht_predictionTotalUP_3to5 .Sumw2()
        htvsmht_predictionTotalUP_6to7 .Sumw2()
        htvsmht_predictionTotalUP_8plus.Sumw2()

        htvsmht_predictionTotalDN_2plus = r.TH2D("htvsmht_predictionTotalDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTotalDN_3plus = r.TH2D("htvsmht_predictionTotalDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTotalDN_2jets = r.TH2D("htvsmht_predictionTotalDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTotalDN_3to5  = r.TH2D("htvsmht_predictionTotalDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionTotalDN_6to7  = r.TH2D("htvsmht_predictionTotalDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionTotalDN_8plus = r.TH2D("htvsmht_predictionTotalDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionTotalDN_2plus.Sumw2()
        htvsmht_predictionTotalDN_3plus.Sumw2()
        htvsmht_predictionTotalDN_2jets.Sumw2()
        htvsmht_predictionTotalDN_3to5 .Sumw2()
        htvsmht_predictionTotalDN_6to7 .Sumw2()
        htvsmht_predictionTotalDN_8plus.Sumw2()

        ####Individual effects
        ###Purity
        htvsmht_predictionPurityUP_2plus = r.TH2D("htvsmht_predictionPurityUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPurityUP_3plus = r.TH2D("htvsmht_predictionPurityUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPurityUP_2jets = r.TH2D("htvsmht_predictionPurityUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPurityUP_3to5  = r.TH2D("htvsmht_predictionPurityUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPurityUP_6to7  = r.TH2D("htvsmht_predictionPurityUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionPurityUP_8plus = r.TH2D("htvsmht_predictionPurityUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionPurityUP_2plus.Sumw2()
        htvsmht_predictionPurityUP_3plus.Sumw2()
        htvsmht_predictionPurityUP_2jets.Sumw2()
        htvsmht_predictionPurityUP_3to5 .Sumw2()
        htvsmht_predictionPurityUP_6to7 .Sumw2()
        htvsmht_predictionPurityUP_8plus.Sumw2()

        htvsmht_predictionPurityDN_2plus = r.TH2D("htvsmht_predictionPurityDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPurityDN_3plus = r.TH2D("htvsmht_predictionPurityDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPurityDN_2jets = r.TH2D("htvsmht_predictionPurityDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPurityDN_3to5  = r.TH2D("htvsmht_predictionPurityDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPurityDN_6to7  = r.TH2D("htvsmht_predictionPurityDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionPurityDN_8plus = r.TH2D("htvsmht_predictionPurityDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionPurityDN_2plus.Sumw2()
        htvsmht_predictionPurityDN_3plus.Sumw2()
        htvsmht_predictionPurityDN_2jets.Sumw2()
        htvsmht_predictionPurityDN_3to5 .Sumw2()
        htvsmht_predictionPurityDN_6to7 .Sumw2()
        htvsmht_predictionPurityDN_8plus.Sumw2()

        ###Acceptance
        htvsmht_predictionAcceptanceUP_2plus = r.TH2D("htvsmht_predictionAcceptanceUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionAcceptanceUP_3plus = r.TH2D("htvsmht_predictionAcceptanceUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionAcceptanceUP_2jets = r.TH2D("htvsmht_predictionAcceptanceUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionAcceptanceUP_3to5  = r.TH2D("htvsmht_predictionAcceptanceUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionAcceptanceUP_6to7  = r.TH2D("htvsmht_predictionAcceptanceUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionAcceptanceUP_8plus = r.TH2D("htvsmht_predictionAcceptanceUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionAcceptanceUP_2plus.Sumw2()
        htvsmht_predictionAcceptanceUP_3plus.Sumw2()
        htvsmht_predictionAcceptanceUP_2jets.Sumw2()
        htvsmht_predictionAcceptanceUP_3to5 .Sumw2()
        htvsmht_predictionAcceptanceUP_6to7 .Sumw2()
        htvsmht_predictionAcceptanceUP_8plus.Sumw2()

        htvsmht_predictionAcceptanceDN_2plus = r.TH2D("htvsmht_predictionAcceptanceDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionAcceptanceDN_3plus = r.TH2D("htvsmht_predictionAcceptanceDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionAcceptanceDN_2jets = r.TH2D("htvsmht_predictionAcceptanceDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionAcceptanceDN_3to5  = r.TH2D("htvsmht_predictionAcceptanceDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionAcceptanceDN_6to7  = r.TH2D("htvsmht_predictionAcceptanceDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionAcceptanceDN_8plus = r.TH2D("htvsmht_predictionAcceptanceDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionAcceptanceDN_2plus.Sumw2()
        htvsmht_predictionAcceptanceDN_3plus.Sumw2()
        htvsmht_predictionAcceptanceDN_2jets.Sumw2()
        htvsmht_predictionAcceptanceDN_3to5 .Sumw2()
        htvsmht_predictionAcceptanceDN_6to7 .Sumw2()
        htvsmht_predictionAcceptanceDN_8plus.Sumw2()

        ###Reco
        htvsmht_predictionRecoUP_2plus = r.TH2D("htvsmht_predictionRecoUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionRecoUP_3plus = r.TH2D("htvsmht_predictionRecoUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionRecoUP_2jets = r.TH2D("htvsmht_predictionRecoUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionRecoUP_3to5  = r.TH2D("htvsmht_predictionRecoUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionRecoUP_6to7  = r.TH2D("htvsmht_predictionRecoUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionRecoUP_8plus = r.TH2D("htvsmht_predictionRecoUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionRecoUP_2plus.Sumw2()
        htvsmht_predictionRecoUP_3plus.Sumw2()
        htvsmht_predictionRecoUP_2jets.Sumw2()
        htvsmht_predictionRecoUP_3to5 .Sumw2()
        htvsmht_predictionRecoUP_6to7 .Sumw2()
        htvsmht_predictionRecoUP_8plus.Sumw2()

        htvsmht_predictionRecoDN_2plus = r.TH2D("htvsmht_predictionRecoDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionRecoDN_3plus = r.TH2D("htvsmht_predictionRecoDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionRecoDN_2jets = r.TH2D("htvsmht_predictionRecoDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionRecoDN_3to5  = r.TH2D("htvsmht_predictionRecoDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionRecoDN_6to7  = r.TH2D("htvsmht_predictionRecoDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionRecoDN_8plus = r.TH2D("htvsmht_predictionRecoDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionRecoDN_2plus.Sumw2()
        htvsmht_predictionRecoDN_3plus.Sumw2()
        htvsmht_predictionRecoDN_2jets.Sumw2()
        htvsmht_predictionRecoDN_3to5 .Sumw2()
        htvsmht_predictionRecoDN_6to7 .Sumw2()
        htvsmht_predictionRecoDN_8plus.Sumw2()

        ###Pixel
        htvsmht_predictionPixelUP_2plus = r.TH2D("htvsmht_predictionPixelUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPixelUP_3plus = r.TH2D("htvsmht_predictionPixelUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPixelUP_2jets = r.TH2D("htvsmht_predictionPixelUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPixelUP_3to5  = r.TH2D("htvsmht_predictionPixelUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPixelUP_6to7  = r.TH2D("htvsmht_predictionPixelUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionPixelUP_8plus = r.TH2D("htvsmht_predictionPixelUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionPixelUP_2plus.Sumw2()
        htvsmht_predictionPixelUP_3plus.Sumw2()
        htvsmht_predictionPixelUP_2jets.Sumw2()
        htvsmht_predictionPixelUP_3to5 .Sumw2()
        htvsmht_predictionPixelUP_6to7 .Sumw2()
        htvsmht_predictionPixelUP_8plus.Sumw2()

        htvsmht_predictionPixelDN_2plus = r.TH2D("htvsmht_predictionPixelDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPixelDN_3plus = r.TH2D("htvsmht_predictionPixelDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPixelDN_2jets = r.TH2D("htvsmht_predictionPixelDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPixelDN_3to5  = r.TH2D("htvsmht_predictionPixelDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPixelDN_6to7  = r.TH2D("htvsmht_predictionPixelDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionPixelDN_8plus = r.TH2D("htvsmht_predictionPixelDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionPixelDN_2plus.Sumw2()
        htvsmht_predictionPixelDN_3plus.Sumw2()
        htvsmht_predictionPixelDN_2jets.Sumw2()
        htvsmht_predictionPixelDN_3to5 .Sumw2()
        htvsmht_predictionPixelDN_6to7 .Sumw2()
        htvsmht_predictionPixelDN_8plus.Sumw2()

        ###Iso
        htvsmht_predictionIsoUP_2plus = r.TH2D("htvsmht_predictionIsoUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionIsoUP_3plus = r.TH2D("htvsmht_predictionIsoUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionIsoUP_2jets = r.TH2D("htvsmht_predictionIsoUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionIsoUP_3to5  = r.TH2D("htvsmht_predictionIsoUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionIsoUP_6to7  = r.TH2D("htvsmht_predictionIsoUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionIsoUP_8plus = r.TH2D("htvsmht_predictionIsoUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionIsoUP_2plus.Sumw2()
        htvsmht_predictionIsoUP_3plus.Sumw2()
        htvsmht_predictionIsoUP_2jets.Sumw2()
        htvsmht_predictionIsoUP_3to5 .Sumw2()
        htvsmht_predictionIsoUP_6to7 .Sumw2()
        htvsmht_predictionIsoUP_8plus.Sumw2()

        htvsmht_predictionIsoDN_2plus = r.TH2D("htvsmht_predictionIsoDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionIsoDN_3plus = r.TH2D("htvsmht_predictionIsoDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionIsoDN_2jets = r.TH2D("htvsmht_predictionIsoDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionIsoDN_3to5  = r.TH2D("htvsmht_predictionIsoDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionIsoDN_6to7  = r.TH2D("htvsmht_predictionIsoDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionIsoDN_8plus = r.TH2D("htvsmht_predictionIsoDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionIsoDN_2plus.Sumw2()
        htvsmht_predictionIsoDN_3plus.Sumw2()
        htvsmht_predictionIsoDN_2jets.Sumw2()
        htvsmht_predictionIsoDN_3to5 .Sumw2()
        htvsmht_predictionIsoDN_6to7 .Sumw2()
        htvsmht_predictionIsoDN_8plus.Sumw2()

        ###DataMC
        htvsmht_predictionDataMCUP_2plus = r.TH2D("htvsmht_predictionDataMCUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionDataMCUP_3plus = r.TH2D("htvsmht_predictionDataMCUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionDataMCUP_2jets = r.TH2D("htvsmht_predictionDataMCUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionDataMCUP_3to5  = r.TH2D("htvsmht_predictionDataMCUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionDataMCUP_6to7  = r.TH2D("htvsmht_predictionDataMCUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionDataMCUP_8plus = r.TH2D("htvsmht_predictionDataMCUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionDataMCUP_2plus.Sumw2()
        htvsmht_predictionDataMCUP_3plus.Sumw2()
        htvsmht_predictionDataMCUP_2jets.Sumw2()
        htvsmht_predictionDataMCUP_3to5 .Sumw2()
        htvsmht_predictionDataMCUP_6to7 .Sumw2()
        htvsmht_predictionDataMCUP_8plus.Sumw2()

        htvsmht_predictionDataMCDN_2plus = r.TH2D("htvsmht_predictionDataMCDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionDataMCDN_3plus = r.TH2D("htvsmht_predictionDataMCDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionDataMCDN_2jets = r.TH2D("htvsmht_predictionDataMCDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionDataMCDN_3to5  = r.TH2D("htvsmht_predictionDataMCDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionDataMCDN_6to7  = r.TH2D("htvsmht_predictionDataMCDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionDataMCDN_8plus = r.TH2D("htvsmht_predictionDataMCDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionDataMCDN_2plus.Sumw2()
        htvsmht_predictionDataMCDN_3plus.Sumw2()
        htvsmht_predictionDataMCDN_2jets.Sumw2()
        htvsmht_predictionDataMCDN_3to5 .Sumw2()
        htvsmht_predictionDataMCDN_6to7 .Sumw2()
        htvsmht_predictionDataMCDN_8plus.Sumw2()

        ###ThFit
        htvsmht_predictionThFitUP_2plus = r.TH2D("htvsmht_predictionThFitUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThFitUP_3plus = r.TH2D("htvsmht_predictionThFitUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThFitUP_2jets = r.TH2D("htvsmht_predictionThFitUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThFitUP_3to5  = r.TH2D("htvsmht_predictionThFitUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThFitUP_6to7  = r.TH2D("htvsmht_predictionThFitUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionThFitUP_8plus = r.TH2D("htvsmht_predictionThFitUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionThFitUP_2plus.Sumw2()
        htvsmht_predictionThFitUP_3plus.Sumw2()
        htvsmht_predictionThFitUP_2jets.Sumw2()
        htvsmht_predictionThFitUP_3to5 .Sumw2()
        htvsmht_predictionThFitUP_6to7 .Sumw2()
        htvsmht_predictionThFitUP_8plus.Sumw2()

        htvsmht_predictionThFitDN_2plus = r.TH2D("htvsmht_predictionThFitDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThFitDN_3plus = r.TH2D("htvsmht_predictionThFitDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThFitDN_2jets = r.TH2D("htvsmht_predictionThFitDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThFitDN_3to5  = r.TH2D("htvsmht_predictionThFitDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThFitDN_6to7  = r.TH2D("htvsmht_predictionThFitDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionThFitDN_8plus = r.TH2D("htvsmht_predictionThFitDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionThFitDN_2plus.Sumw2()
        htvsmht_predictionThFitDN_3plus.Sumw2()
        htvsmht_predictionThFitDN_2jets.Sumw2()
        htvsmht_predictionThFitDN_3to5 .Sumw2()
        htvsmht_predictionThFitDN_6to7 .Sumw2()
        htvsmht_predictionThFitDN_8plus.Sumw2()

        ###Pheno
        htvsmht_predictionPhenoUP_2plus = r.TH2D("htvsmht_predictionPhenoUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPhenoUP_3plus = r.TH2D("htvsmht_predictionPhenoUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPhenoUP_2jets = r.TH2D("htvsmht_predictionPhenoUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPhenoUP_3to5  = r.TH2D("htvsmht_predictionPhenoUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPhenoUP_6to7  = r.TH2D("htvsmht_predictionPhenoUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionPhenoUP_8plus = r.TH2D("htvsmht_predictionPhenoUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionPhenoUP_2plus.Sumw2()
        htvsmht_predictionPhenoUP_3plus.Sumw2()
        htvsmht_predictionPhenoUP_2jets.Sumw2()
        htvsmht_predictionPhenoUP_3to5 .Sumw2()
        htvsmht_predictionPhenoUP_6to7 .Sumw2()
        htvsmht_predictionPhenoUP_8plus.Sumw2()

        htvsmht_predictionPhenoDN_2plus = r.TH2D("htvsmht_predictionPhenoDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPhenoDN_3plus = r.TH2D("htvsmht_predictionPhenoDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPhenoDN_2jets = r.TH2D("htvsmht_predictionPhenoDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPhenoDN_3to5  = r.TH2D("htvsmht_predictionPhenoDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionPhenoDN_6to7  = r.TH2D("htvsmht_predictionPhenoDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionPhenoDN_8plus = r.TH2D("htvsmht_predictionPhenoDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionPhenoDN_2plus.Sumw2()
        htvsmht_predictionPhenoDN_3plus.Sumw2()
        htvsmht_predictionPhenoDN_2jets.Sumw2()
        htvsmht_predictionPhenoDN_3to5 .Sumw2()
        htvsmht_predictionPhenoDN_6to7 .Sumw2()
        htvsmht_predictionPhenoDN_8plus.Sumw2()

        ###ThDouble
        htvsmht_predictionThDoubleUP_2plus = r.TH2D("htvsmht_predictionThDoubleUP_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThDoubleUP_3plus = r.TH2D("htvsmht_predictionThDoubleUP_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThDoubleUP_2jets = r.TH2D("htvsmht_predictionThDoubleUP_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThDoubleUP_3to5  = r.TH2D("htvsmht_predictionThDoubleUP_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThDoubleUP_6to7  = r.TH2D("htvsmht_predictionThDoubleUP_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionThDoubleUP_8plus = r.TH2D("htvsmht_predictionThDoubleUP_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionThDoubleUP_2plus.Sumw2()
        htvsmht_predictionThDoubleUP_3plus.Sumw2()
        htvsmht_predictionThDoubleUP_2jets.Sumw2()
        htvsmht_predictionThDoubleUP_3to5 .Sumw2()
        htvsmht_predictionThDoubleUP_6to7 .Sumw2()
        htvsmht_predictionThDoubleUP_8plus.Sumw2()

        htvsmht_predictionThDoubleDN_2plus = r.TH2D("htvsmht_predictionThDoubleDN_2jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThDoubleDN_3plus = r.TH2D("htvsmht_predictionThDoubleDN_3jet" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThDoubleDN_2jets = r.TH2D("htvsmht_predictionThDoubleDN_dijet","H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThDoubleDN_3to5  = r.TH2D("htvsmht_predictionThDoubleDN_3to5" ,"H_{T} vs. #slashH_{T}",len(lowjetHTBins)-1 ,array('d',lowjetHTBins) ,len(lowjetMHTBins)-1 ,array('d',lowjetMHTBins))
        htvsmht_predictionThDoubleDN_6to7  = r.TH2D("htvsmht_predictionThDoubleDN_6to7" ,"H_{T} vs. #slashH_{T}",len(midjetHTBins)-1 ,array('d',midjetHTBins) ,len(midjetMHTBins)-1 ,array('d',midjetMHTBins))
        htvsmht_predictionThDoubleDN_8plus = r.TH2D("htvsmht_predictionThDoubleDN_8jet" ,"H_{T} vs. #slashH_{T}",len(highjetHTBins)-1,array('d',highjetHTBins),len(highjetMHTBins)-1,array('d',highjetMHTBins))
    
        htvsmht_predictionThDoubleDN_2plus.Sumw2()
        htvsmht_predictionThDoubleDN_3plus.Sumw2()
        htvsmht_predictionThDoubleDN_2jets.Sumw2()
        htvsmht_predictionThDoubleDN_3to5 .Sumw2()
        htvsmht_predictionThDoubleDN_6to7 .Sumw2()
        htvsmht_predictionThDoubleDN_8plus.Sumw2()

    ##loop over events and perform prediction
    myChain = r.TChain("data")
    if options.sample == "zinv":
        myChain = r.TChain("zinv")
    elif options.sample == "gjets":
        myChain = r.TChain("gjets")
    elif options.sample == "mc":
        myChain = r.TChain("mc")

    myChain.Add("%s/%s_fits_%dto8_bin%d_new_%s.root"%(options.inDir,
                                                      extra,
                                                      options.fitRange,
                                                      myFitBin,
                                                      zmumuextra))

    highTrackEvents = [
        [71205682,  194314, 82],
        [19536567,  198271, 15],
        [705681614, 198271, 608],
        [176340223, 198230, 154],
        [392561262, 198969, 295],
        [64476380,  207477, 79],
        [97085033,  204599, 98],
        
        ]
        
    nentries = myChain.GetEntries()
    print "nentries %d"%(nentries)
    sys.stdout.flush()
    i = 0
    for event in myChain:
        #if not (((event.ht>500 and event.mht>200) or (event.ht>800 and event.mht>100))):

        if event.nJets>7 or event.ht>2500 or event.mht>1000:
            if options.sample == "data":
                print "ht:%2.2f, mht:%2.2f, nJets:%d, photonPt:%2.2f event:%d, run:%d, lumi:%d"%(
                    event.ht,event.mht,event.nJets,event.photonPt,
                    event.eventNum,event.runNum,event.lumiBlock)
            elif options.sample not in ["zinv"]:
                print "ht:%2.2f, mht:%2.2f, nJets:%d, photonPt:%2.2f"%(
                    event.ht,event.mht,event.nJets,event.photonPt)
            else:
                print "ht:%2.2f, mht:%2.2f, nJets:%d"%(
                    event.ht,event.mht,event.nJets)
                
        if options.sample == "data":
            if [event.eventNum,event.runNum,event.lumiBlock] in highTrackEvents:
                print "found high tracking event, skipping"
                continue
        
        if ((event.ht<500) or (event.ht<800 and event.mht<100)):
            continue
        if event.nJets<2:
            continue
        elif (event.nJets>1):
            htvsmht_raw_2plus.Fill(event.ht,event.mht,event.eventWeight)
            htvsmht_scaled_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
            if not options.sample=="zinv":
                htvsmht_prediction_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                htvsmht_predictionSystUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorUP)
                htvsmht_predictionSystDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDN)
                htvsmht_predictionTheoryUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThUP)
                htvsmht_predictionTheoryDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDN)
                htvsmht_predictionTotalUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotUP)
                htvsmht_predictionTotalDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotDN)

                htvsmht_predictionPurityUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurUP)
                htvsmht_predictionPurityDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurDN)
                htvsmht_predictionPhenoUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenUP)
                htvsmht_predictionPhenoDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenDN)
                htvsmht_predictionThFitUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitUP)
                htvsmht_predictionThFitDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitDN)
                htvsmht_predictionThDoubleUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleUP)
                htvsmht_predictionThDoubleDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleDN)
                htvsmht_predictionAcceptanceUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccUP)
                htvsmht_predictionAcceptanceDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccDN)
                htvsmht_predictionRecoUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDUP)
                htvsmht_predictionRecoDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDDN)
                htvsmht_predictionPixelUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixUP)
                htvsmht_predictionPixelDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixDN)
                htvsmht_predictionIsoUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoUP)
                htvsmht_predictionIsoDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoDN)
                htvsmht_predictionDataMCUP_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFUP)
                htvsmht_predictionDataMCDN_2plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFDN)

            mht_raw_2plus.Fill(event.mht,event.eventWeight)
            mht_scaled_2plus.Fill(event.mht,event.eventWeight*event.scaleFactor)
            ht_raw_2plus.Fill(event.ht,event.eventWeight)
            ht_scaled_2plus.Fill(event.ht,event.eventWeight*event.scaleFactor)

            njets_raw_htinc.Fill(event.nJets,event.eventWeight)
            njets_scaled_htinc.Fill(event.nJets,event.eventWeight*event.scaleFactor)
            
            if event.ht>500 and event.ht<800:
                njets_raw_ht5to8.Fill(event.nJets,event.eventWeight)
                njets_scaled_ht5to8.Fill(event.nJets,event.eventWeight*event.scaleFactor)

            elif event.ht>800 and event.ht<1000:
                njets_raw_ht8to10.Fill(event.nJets,event.eventWeight)
                njets_scaled_ht8to10.Fill(event.nJets,event.eventWeight*event.scaleFactor)

            elif event.ht>1000 and event.ht<1250:
                njets_raw_ht10to125.Fill(event.nJets,event.eventWeight)
                njets_scaled_ht10to125.Fill(event.nJets,event.eventWeight*event.scaleFactor)

            elif event.ht>1250 and event.ht<1500:
                njets_raw_ht125to15.Fill(event.nJets,event.eventWeight)
                njets_scaled_ht125to15.Fill(event.nJets,event.eventWeight*event.scaleFactor)

            elif event.ht>1500:
                njets_raw_ht15to30.Fill(event.nJets,event.eventWeight)
                njets_scaled_ht15to30.Fill(event.nJets,event.eventWeight*event.scaleFactor)
            
            if (event.nJets<3):
                htvsmht_raw_2jets.Fill(event.ht,event.mht,event.eventWeight)
                htvsmht_scaled_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                if not options.sample=="zinv":
                    htvsmht_prediction_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                    htvsmht_predictionSystUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorUP)
                    htvsmht_predictionSystDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDN)
                    htvsmht_predictionTheoryUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThUP)
                    htvsmht_predictionTheoryDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDN)
                    htvsmht_predictionTotalUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotUP)
                    htvsmht_predictionTotalDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotDN)
                    
                    htvsmht_predictionPurityUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurUP)
                    htvsmht_predictionPurityDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurDN)
                    htvsmht_predictionPhenoUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenUP)
                    htvsmht_predictionPhenoDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenDN)
                    htvsmht_predictionThFitUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitUP)
                    htvsmht_predictionThFitDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitDN)
                    htvsmht_predictionThDoubleUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleUP)
                    htvsmht_predictionThDoubleDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleDN)
                    htvsmht_predictionAcceptanceUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccUP)
                    htvsmht_predictionAcceptanceDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccDN)
                    htvsmht_predictionRecoUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDUP)
                    htvsmht_predictionRecoDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDDN)
                    htvsmht_predictionPixelUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixUP)
                    htvsmht_predictionPixelDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixDN)
                    htvsmht_predictionIsoUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoUP)
                    htvsmht_predictionIsoDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoDN)
                    htvsmht_predictionDataMCUP_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFUP)
                    htvsmht_predictionDataMCDN_2jets.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFDN)
                    
                mht_raw_2jets.Fill(event.mht,event.eventWeight)
                mht_scaled_2jets.Fill(event.mht,event.eventWeight*event.scaleFactor)
                ht_raw_2jets.Fill(event.ht,event.eventWeight)
                ht_scaled_2jets.Fill(event.ht,event.eventWeight*event.scaleFactor)
            ##
            else:
                htvsmht_raw_3plus.Fill(event.ht,event.mht,event.eventWeight)
                htvsmht_scaled_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                if not options.sample=="zinv":
                    htvsmht_prediction_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                    htvsmht_predictionSystUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorUP)
                    htvsmht_predictionSystDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDN)
                    htvsmht_predictionTheoryUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThUP)
                    htvsmht_predictionTheoryDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDN)
                    htvsmht_predictionTotalUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotUP)
                    htvsmht_predictionTotalDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotDN)

                    htvsmht_predictionPurityUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurUP)
                    htvsmht_predictionPurityDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurDN)
                    htvsmht_predictionPhenoUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenUP)
                    htvsmht_predictionPhenoDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenDN)
                    htvsmht_predictionThFitUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitUP)
                    htvsmht_predictionThFitDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitDN)
                    htvsmht_predictionThDoubleUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleUP)
                    htvsmht_predictionThDoubleDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleDN)
                    htvsmht_predictionAcceptanceUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccUP)
                    htvsmht_predictionAcceptanceDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccDN)
                    htvsmht_predictionRecoUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDUP)
                    htvsmht_predictionRecoDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDDN)
                    htvsmht_predictionPixelUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixUP)
                    htvsmht_predictionPixelDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixDN)
                    htvsmht_predictionIsoUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoUP)
                    htvsmht_predictionIsoDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoDN)
                    htvsmht_predictionDataMCUP_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFUP)
                    htvsmht_predictionDataMCDN_3plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFDN)

                mht_raw_3plus.Fill(event.mht,event.eventWeight)
                mht_scaled_3plus.Fill(event.mht,event.eventWeight*event.scaleFactor)
                ht_raw_3plus.Fill(event.ht,event.eventWeight)
                ht_scaled_3plus.Fill(event.ht,event.eventWeight*event.scaleFactor)
                if (event.nJets<6):
                    htvsmht_raw_3to5.Fill(event.ht,event.mht,event.eventWeight)
                    htvsmht_scaled_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                    if not options.sample=="zinv":
                        htvsmht_prediction_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                        htvsmht_predictionSystUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorUP)
                        htvsmht_predictionSystDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDN)
                        htvsmht_predictionTheoryUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThUP)
                        htvsmht_predictionTheoryDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDN)
                        htvsmht_predictionTotalUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotUP)
                        htvsmht_predictionTotalDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotDN)

                        htvsmht_predictionPurityUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurUP)
                        htvsmht_predictionPurityDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurDN)
                        htvsmht_predictionPhenoUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenUP)
                        htvsmht_predictionPhenoDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenDN)
                        htvsmht_predictionThFitUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitUP)
                        htvsmht_predictionThFitDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitDN)
                        htvsmht_predictionThDoubleUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleUP)
                        htvsmht_predictionThDoubleDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleDN)
                        htvsmht_predictionAcceptanceUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccUP)
                        htvsmht_predictionAcceptanceDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccDN)
                        htvsmht_predictionRecoUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDUP)
                        htvsmht_predictionRecoDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDDN)
                        htvsmht_predictionPixelUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixUP)
                        htvsmht_predictionPixelDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixDN)
                        htvsmht_predictionIsoUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoUP)
                        htvsmht_predictionIsoDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoDN)
                        htvsmht_predictionDataMCUP_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFUP)
                        htvsmht_predictionDataMCDN_3to5.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFDN)

                    mht_raw_3to5.Fill(event.mht,event.eventWeight)
                    mht_scaled_3to5.Fill(event.mht,event.eventWeight*event.scaleFactor)
                    ht_raw_3to5.Fill(event.ht,event.eventWeight)
                    ht_scaled_3to5.Fill(event.ht,event.eventWeight*event.scaleFactor)
            ##
                elif (event.nJets>5 and event.nJets<8):
                    htvsmht_raw_6to7.Fill(event.ht,event.mht,event.eventWeight)
                    htvsmht_scaled_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                    if not options.sample=="zinv":
                        htvsmht_prediction_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                        htvsmht_predictionSystUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorUP)
                        htvsmht_predictionSystDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDN)
                        htvsmht_predictionTheoryUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThUP)
                        htvsmht_predictionTheoryDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDN)
                        htvsmht_predictionTotalUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotUP)
                        htvsmht_predictionTotalDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotDN)

                        htvsmht_predictionPurityUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurUP)
                        htvsmht_predictionPurityDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurDN)
                        htvsmht_predictionPhenoUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenUP)
                        htvsmht_predictionPhenoDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenDN)
                        htvsmht_predictionThFitUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitUP)
                        htvsmht_predictionThFitDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitDN)
                        htvsmht_predictionThDoubleUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleUP)
                        htvsmht_predictionThDoubleDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleDN)
                        htvsmht_predictionAcceptanceUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccUP)
                        htvsmht_predictionAcceptanceDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccDN)
                        htvsmht_predictionRecoUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDUP)
                        htvsmht_predictionRecoDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDDN)
                        htvsmht_predictionPixelUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixUP)
                        htvsmht_predictionPixelDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixDN)
                        htvsmht_predictionIsoUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoUP)
                        htvsmht_predictionIsoDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoDN)
                        htvsmht_predictionDataMCUP_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFUP)
                        htvsmht_predictionDataMCDN_6to7.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFDN)

                    mht_raw_6to7.Fill(event.mht,event.eventWeight)
                    mht_scaled_6to7.Fill(event.mht,event.eventWeight*event.scaleFactor)
                    ht_raw_6to7.Fill(event.ht,event.eventWeight)
                    ht_scaled_6to7.Fill(event.ht,event.eventWeight*event.scaleFactor)
                else:
#                    if options.sample == "data":
#                        print "ht:%2.2f, mht:%2.2f, nJets:%d, event:%d, run:%d, lumi:%d"%(
#                            event.ht,event.mht,event.nJets,
#                            event.eventNum,event.runNum,event.lumiBlock)
#                    else:
#                        print "ht:%2.2f, mht:%2.2f, nJets:%d"%(
#                            event.ht,event.mht,event.nJets)
                        
                    #if event.nJets > 19:
                    #    continue
                    
                    htvsmht_raw_8plus.Fill(event.ht,event.mht,event.eventWeight)
                    htvsmht_scaled_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                    if not options.sample=="zinv":
                        htvsmht_prediction_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactor)
                        htvsmht_predictionSystUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorUP)
                        htvsmht_predictionSystDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDN)
                        htvsmht_predictionTheoryUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThUP)
                        htvsmht_predictionTheoryDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDN)
                        htvsmht_predictionTotalUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotUP)
                        htvsmht_predictionTotalDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorTotDN)

                        htvsmht_predictionPurityUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurUP)
                        htvsmht_predictionPurityDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPurDN)
                        htvsmht_predictionPhenoUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenUP)
                        htvsmht_predictionPhenoDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPhenDN)
                        htvsmht_predictionThFitUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitUP)
                        htvsmht_predictionThFitDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThFitDN)
                        htvsmht_predictionThDoubleUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleUP)
                        htvsmht_predictionThDoubleDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorThDoubleDN)
                        htvsmht_predictionAcceptanceUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccUP)
                        htvsmht_predictionAcceptanceDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorAccDN)
                        htvsmht_predictionRecoUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDUP)
                        htvsmht_predictionRecoDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIDDN)
                        htvsmht_predictionPixelUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixUP)
                        htvsmht_predictionPixelDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorPixDN)
                        htvsmht_predictionIsoUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoUP)
                        htvsmht_predictionIsoDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorIsoDN)
                        htvsmht_predictionDataMCUP_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFUP)
                        htvsmht_predictionDataMCDN_8plus.Fill(event.ht,event.mht,event.eventWeight*event.scaleFactorDMCSFDN)

##                        htvsmht_predictionPurityUP_2plus.Write()
##                        htvsmht_predictionPurityUP_3plus.Write()
##                        htvsmht_predictionPurityUP_2jets.Write()
##                        htvsmht_predictionPurityUP_3to5 .Write()
##                        htvsmht_predictionPurityUP_6to7 .Write()
##                        htvsmht_predictionPurityUP_8plus.Write()
##                        htvsmht_predictionPurityDN_2plus.Write()
##                        htvsmht_predictionPurityDN_3plus.Write()
##                        htvsmht_predictionPurityDN_2jets.Write()
##                        htvsmht_predictionPurityDN_3to5 .Write()
##                        htvsmht_predictionPurityDN_6to7 .Write()
##                        htvsmht_predictionPurityDN_8plus.Write()
##                        
##                        htvsmht_predictionAcceptanceUP_2plus.Write()
##                        htvsmht_predictionAcceptanceUP_3plus.Write()
##                        htvsmht_predictionAcceptanceUP_2jets.Write()
##                        htvsmht_predictionAcceptanceUP_3to5 .Write()
##                        htvsmht_predictionAcceptanceUP_6to7 .Write()
##                        htvsmht_predictionAcceptanceUP_8plus.Write()
##                        htvsmht_predictionAcceptanceDN_2plus.Write()
##                        htvsmht_predictionAcceptanceDN_3plus.Write()
##                        htvsmht_predictionAcceptanceDN_2jets.Write()
##                        htvsmht_predictionAcceptanceDN_3to5 .Write()
##                        htvsmht_predictionAcceptanceDN_6to7 .Write()
##                        htvsmht_predictionAcceptanceDN_8plus.Write()
##                        
##                        htvsmht_predictionRecoUP_2plus.Write()
##                        htvsmht_predictionRecoUP_3plus.Write()
##                        htvsmht_predictionRecoUP_2jets.Write()
##                        htvsmht_predictionRecoUP_3to5 .Write()
##                        htvsmht_predictionRecoUP_6to7 .Write()
##                        htvsmht_predictionRecoUP_8plus.Write()
##                        htvsmht_predictionRecoDN_2plus.Write()
##                        htvsmht_predictionRecoDN_3plus.Write()
##                        htvsmht_predictionRecoDN_2jets.Write()
##                        htvsmht_predictionRecoDN_3to5 .Write()
##                        htvsmht_predictionRecoDN_6to7 .Write()
##                        htvsmht_predictionRecoDN_8plus.Write()
##                        
##                        htvsmht_predictionPixelUP_2plus.Write()
##                        htvsmht_predictionPixelUP_3plus.Write()
##                        htvsmht_predictionPixelUP_2jets.Write()
##                        htvsmht_predictionPixelUP_3to5 .Write()
##                        htvsmht_predictionPixelUP_6to7 .Write()
##                        htvsmht_predictionPixelUP_8plus.Write()
##                        htvsmht_predictionPixelDN_2plus.Write()
##                        htvsmht_predictionPixelDN_3plus.Write()
##                        htvsmht_predictionPixelDN_2jets.Write()
##                        htvsmht_predictionPixelDN_3to5 .Write()
##                        htvsmht_predictionPixelDN_6to7 .Write()
##                        htvsmht_predictionPixelDN_8plus.Write()
##                        
##                        htvsmht_predictionIsoUP_2plus.Write()
##                        htvsmht_predictionIsoUP_3plus.Write()
##                        htvsmht_predictionIsoUP_2jets.Write()
##                        htvsmht_predictionIsoUP_3to5 .Write()
##                        htvsmht_predictionIsoUP_6to7 .Write()
##                        htvsmht_predictionIsoUP_8plus.Write()
##                        htvsmht_predictionIsoDN_2plus.Write()
##                        htvsmht_predictionIsoDN_3plus.Write()
##                        htvsmht_predictionIsoDN_2jets.Write()
##                        htvsmht_predictionIsoDN_3to5 .Write()
##                        htvsmht_predictionIsoDN_6to7 .Write()
##                        htvsmht_predictionIsoDN_8plus.Write()
##                        
##                        htvsmht_predictionDataMCUP_2plus.Write()
##                        htvsmht_predictionDataMCUP_3plus.Write()
##                        htvsmht_predictionDataMCUP_2jets.Write()
##                        htvsmht_predictionDataMCUP_3to5 .Write()
##                        htvsmht_predictionDataMCUP_6to7 .Write()
##                        htvsmht_predictionDataMCUP_8plus.Write()
##                        htvsmht_predictionDataMCDN_2plus.Write()
##                        htvsmht_predictionDataMCDN_3plus.Write()
##                        htvsmht_predictionDataMCDN_2jets.Write()
##                        htvsmht_predictionDataMCDN_3to5 .Write()
##                        htvsmht_predictionDataMCDN_6to7 .Write()
##                        htvsmht_predictionDataMCDN_8plus.Write()
##                        
##                        htvsmht_predictionThFitUP_2plus.Write()
##                        htvsmht_predictionThFitUP_3plus.Write()
##                        htvsmht_predictionThFitUP_2jets.Write()
##                        htvsmht_predictionThFitUP_3to5 .Write()
##                        htvsmht_predictionThFitUP_6to7 .Write()
##                        htvsmht_predictionThFitUP_8plus.Write()
##                        htvsmht_predictionThFitDN_2plus.Write()
##                        htvsmht_predictionThFitDN_3plus.Write()
##                        htvsmht_predictionThFitDN_2jets.Write()
##                        htvsmht_predictionThFitDN_3to5 .Write()
##                        htvsmht_predictionThFitDN_6to7 .Write()
##                        htvsmht_predictionThFitDN_8plus.Write()
##                        
##                        htvsmht_predictionPhenoUP_2plus.Write()
##                        htvsmht_predictionPhenoUP_3plus.Write()
##                        htvsmht_predictionPhenoUP_2jets.Write()
##                        htvsmht_predictionPhenoUP_3to5 .Write()
##                        htvsmht_predictionPhenoUP_6to7 .Write()
##                        htvsmht_predictionPhenoUP_8plus.Write()
##                        htvsmht_predictionPhenoDN_2plus.Write()
##                        htvsmht_predictionPhenoDN_3plus.Write()
##                        htvsmht_predictionPhenoDN_2jets.Write()
##                        htvsmht_predictionPhenoDN_3to5 .Write()
##                        htvsmht_predictionPhenoDN_6to7 .Write()
##                        htvsmht_predictionPhenoDN_8plus.Write()
##                        
##                        htvsmht_predictionThDoubleUP_2plus.Write()
##                        htvsmht_predictionThDoubleUP_3plus.Write()
##                        htvsmht_predictionThDoubleUP_2jets.Write()
##                        htvsmht_predictionThDoubleUP_3to5 .Write()
##                        htvsmht_predictionThDoubleUP_6to7 .Write()
##                        htvsmht_predictionThDoubleUP_8plus.Write()
##                        htvsmht_predictionThDoubleDN_2plus.Write()
##                        htvsmht_predictionThDoubleDN_3plus.Write()
##                        htvsmht_predictionThDoubleDN_2jets.Write()
##                        htvsmht_predictionThDoubleDN_3to5 .Write()
##                        htvsmht_predictionThDoubleDN_6to7 .Write()
##                        htvsmht_predictionThDoubleDN_8plus.Write()
##
                    mht_raw_8plus.Fill(event.mht,event.eventWeight)
                    mht_scaled_8plus.Fill(event.mht,event.eventWeight*event.scaleFactor)
                    ht_raw_8plus.Fill(event.ht,event.eventWeight)
                    ht_scaled_8plus.Fill(event.ht,event.eventWeight*event.scaleFactor)

    ###
    outputFile.Write()
    outputFile.Close()

    
####very end####
if __name__ == '__main__':
    main()

