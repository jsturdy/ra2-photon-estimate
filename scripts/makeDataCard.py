import sys,os
import ROOT as r
from array import array
import math
import optparse
from specialFunctions import mkdir_p

########Main
def main() :
    parser = optparse.OptionParser(description="Driver parameters for makeGenRatioPlots.py")
    parser.add_option('-g', '--genreco', action="store_true", default=False, dest="genreco")
    parser.add_option('-o', '--outDir',  type='string', action="store", default="/tmp", dest="outDir")
    parser.add_option('-i', '--inDir',   type='string', action="store", default="/tmp", dest="inDir")
    parser.add_option('-z', '--zmumuMC', action="store_true", default=False, dest="zmumuMC")
    parser.add_option('-s', '--sample',  type='string',action="store", default="data",dest="sample")
    parser.add_option('-b', '--fitBin',  type='int',   action="store", default=2,     dest="fitBin")
    parser.add_option('-r', '--fitRange',type='int',    action="store", default=2, dest="fitRange")
    options, args = parser.parse_args()

    r.gROOT.SetBatch(True)
    mkdir_p("%s"%(options.outDir))

    goodFitBins = [0,1,2,3,4,5,6]
    myFitBin = options.fitBin
    if options.fitBin not in goodFitBins:
        print "invalid option for fit bins, using default 0"
        myFitBin = 0

    histoNames = [
        #["htvsmht_scaled_2jet","$N_{Jets}\\geq 2$"],
        #["htvsmht_scaled_3jet","$N_{Jets}\\geq 3$"],
        ["dijet","$N_{Jets}==2$"],
        ["3to5", "$3\\leq N_{Jets}\\leq 5$"],
        ["6to7", "$6\\leq N_{Jets}\\leq 7$"],
        ["8jet", "$N_{Jets}\\geq 8$"],
        ]

    htBins = [
        ["$500 < H_{T} < 800$"  ,"500\\ldots   800"],
        ["$800 < H_{T} < 1000$" ,"800\\ldots  1000"],
        ["$1000 < H_{T} < 1250$","1000\\ldots 1250"],
        ["$1250 < H_{T} < 1500$","1250\\ldots 1500"],
        ["$1500 < H_{T}$"       ,"1500\\ldots     "],
        ]
    extra = "reco"
    if options.genreco:
        extra = "gen"

    zmumuextra = "zmumuGammaData"
    if options.zmumuMC:
        zmumuextra = "zmumuGammaMC"

    zinvInputFile  = r.TFile("%s/zinv_%s_predictions_%dto8_bin%d_%s_new.root"%(options.inDir,
                                                                               extra,options.fitRange,
                                                                               myFitBin,zmumuextra),"READ")
    dataInputFile  = r.TFile("%s/%s_%s_predictions_%dto8_bin%d_%s_new.root"%(options.inDir,
                                                                             options.sample,
                                                                             extra,options.fitRange,
                                                                             myFitBin,zmumuextra),"READ")
    mcInputFile  = r.TFile("%s/mc_%s_predictions_%dto8_bin%d_%s_new.root"%(options.inDir,
                                                                             extra,options.fitRange,
                                                                             myFitBin,zmumuextra),"READ")
    #gjetsInputFile = r.TFile("gjets_%s_predictions.root"%(extra),"READ")

    dc = open('%s/datacard_zinv_photons_%s_%s_%dto8_bin%d_%s_new.txt'%(options.outDir,
                                                                       options.sample,
                                                                       extra,options.fitRange,
                                                                       myFitBin,zmumuextra), 'w')
    dc.write("""# General information:
luminosity = 19371     # given in pb-1
channels = 36          # total number of channels / bins. Counting ordering, MHT, HT and nJets.
nuisances = 2          # number of nuisance/uncertainties
sample = zinvis        # name of the sample

# bin1 is for nJets [3, 5], HT [500, 800] and MHT [200, 300]; bin2 is for nJets [3, 5], HT [500, 800] and MHT [300, 450] ...
channel = bin1; bin2; bin3; bin4; bin5; bin6; bin7; bin8; bin9; bin10; \
bin11; bin12; bin13; bin14; bin15; bin16; bin17; bin18; bin19; bin20; \
bin21; bin22; bin23; bin24; bin25; bin26; bin27; bin28; bin29; bin30; \
bin31; bin32; bin33; bin34; bin35; bin36;

# Predicted events
zinvis_events = """)

###    
##dupe??##    datapred  = open('%s/%s_%s_prediction_ra2_tables_%dto8_bin%d_%s_new.tex'%(options.outDir,
##dupe??##                                                                              options.sample,
##dupe??##                                                                              extra,options.fitRange,
##dupe??##                                                                              myFitBin,zmumuextra), 'w')
    datapred  = open('%s/%s_%s_prediction_ra2_tables_%dto8_bin%d_%s_new.tex'%(options.outDir,
                                                                              options.sample,
                                                                              extra,options.fitRange,
                                                                              myFitBin,zmumuextra), 'w')
    zinvest   = open('%s/zinv_estimate_ra2_tables_%dto8_new.tex'%(options.outDir,options.fitRange), 'w')
    totalpred = open('%s/%s_%s_total_estimate_ra2_tables_%dto8_bin%s_%s_new.tex'%(options.outDir,
                                                                            options.sample,
                                                                            extra,options.fitRange,
                                                                            myFitBin,zmumuextra), 'w')
    totalperpred = open('%s/%s_%s_total_estimate_per_ra2_tables_%dto8_bin%s_%s_new.tex'%(options.outDir,
                                                                                         options.sample,
                                                                                         extra,options.fitRange,
                                                                                         myFitBin,zmumuextra), 'w')
    totaldatamcpred = open('%s/%s_%s_total_datamc_estimate_ra2_tables_%dto8_bin%s_%s_new.tex'%(options.outDir,
                                                                                               options.sample,
                                                                                               extra,options.fitRange,
                                                                                               myFitBin,zmumuextra), 'w')
    totaldatamcperpred = open('%s/%s_%s_total_datamc_estimate_per_ra2_tables_%dto8_bin%s_%s_new.tex'%(options.outDir,
                                                                                                      options.sample,
                                                                                                      extra,options.fitRange,
                                                                                                      myFitBin,zmumuextra), 'w')
    totalunc = open('%s/%s_%s_total_uncertainties_ra2_tables_%dto8_bin%s_%s_new.tex'%(options.outDir,
                                                                            options.sample,
                                                                            extra,options.fitRange,
                                                                            myFitBin,zmumuextra), 'w')
    totalperunc = open('%s/%s_%s_total_peruncertainties_ra2_tables_%dto8_bin%s_%s_new.tex'%(options.outDir,
                                                                                            options.sample,
                                                                                            extra,options.fitRange,
                                                                                            myFitBin,zmumuextra), 'w')
    datapred.write("\\documentclass{article}\n")
    datapred.write("\\usepackage[english]{babel}\n")
    datapred.write("\\usepackage{mathtools}\n")
    datapred.write("\\usepackage{pdflscape}\n")
    datapred.write("\\usepackage{multirow}\n")
    datapred.write("\\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}\n")
    datapred.write("\\usepackage{xspace}\n")
    datapred.write("\\usepackage{marvosym}\n")
    datapred.write("\\usepackage{ifsym}\n")
    datapred.write("\\usepackage{savesym}\n")
    datapred.write("\\savesymbol{T}\n")
    datapred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/ptdr-definitions.sty}\n")
    datapred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pennames-pazo.sty}\n")
    datapred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/sparticles.sty}\n")
    datapred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pdefs}\n")
    datapred.write("\\restoresymbol{pdefs}{T}\n")
    #datapred.write("\\newcommand{\\INVZJET}{\\ensuremath{\\PZ\\to\\Pgn\\Pagn+\\mathrm{jet}}\\xspace}\n")
    #datapred.write("\\newcommand{\\INVZJETS}{\\ensuremath{\\INVZJET\\mathrm{s}}\\xspace}\n")
    datapred.write("\\begin{document}\n")
    datapred.write("\\begin{landscape}\n")

    zinvest.write("\\documentclass{article}\n")
    zinvest.write("\\usepackage[english]{babel}\n")
    zinvest.write("\\usepackage{mathtools}\n")
    zinvest.write("\\usepackage{pdflscape}\n")
    zinvest.write("\\usepackage{multirow}\n")
    zinvest.write("\\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}\n")
    zinvest.write("\\usepackage{xspace}\n")
    zinvest.write("\\usepackage{marvosym}\n")
    zinvest.write("\\usepackage{ifsym}\n")
    zinvest.write("\\usepackage{savesym}\n")
    zinvest.write("\\savesymbol{T}\n")
    zinvest.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/ptdr-definitions.sty}\n")
    zinvest.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pennames-pazo.sty}\n")
    zinvest.write("\\input{/home/Frod014/research/thesis-sturdy/styles/sparticles.sty}\n")
    zinvest.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pdefs}\n")
    zinvest.write("\\restoresymbol{pdefs}{T}\n")
    #zinvest.write("\\newcommand{\\INVZJET}{\\ensuremath{\\PZ\\to\\Pgn\\Pagn+\\mathrm{jet}}\\xspace}\n")
    #zinvest.write("\\newcommand{\\INVZJETS}{\\ensuremath{\\INVZJET\\mathrm{s}}\\xspace}\n")
    zinvest.write("\\begin{document}\n")
    zinvest.write("\\begin{landscape}\n")
    zinvest.write("  \\begin{table}[h]\n")
    zinvest.write("    \\centering\n")
    zinvest.write("    \\begin{tabular}{|l|l|l|l|l|l|}\n")
    zinvest.write("      \\hline\n")
    zinvest.write("      & $100<\\slash{H_{T}}<200$ & $200<\\slash{H_{T}}<300$ & $300<\\slash{H_{T}}<450$ & $450<\\slash{H_{T}}<600$ & $600<\\slash{H_{T}}$   \\\\\n")

    totalpred.write("\\documentclass{article}\n")
    totalpred.write("\\usepackage[english]{babel}\n")
    totalpred.write("\\usepackage{mathtools}\n")
    totalpred.write("\\usepackage{pdflscape}\n")
    totalpred.write("\\usepackage{multirow}\n")
    totalpred.write("\\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}\n")
    totalpred.write("\\usepackage{xspace}\n")
    totalpred.write("\\usepackage{marvosym}\n")
    totalpred.write("\\usepackage{ifsym}\n")
    totalpred.write("\\usepackage{savesym}\n")
    totalpred.write("\\savesymbol{T}\n")
    totalpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/ptdr-definitions.sty}\n")
    totalpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pennames-pazo.sty}\n")
    totalpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/sparticles.sty}\n")
    totalpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pdefs}\n")
    totalpred.write("\\restoresymbol{pdefs}{T}\n")
    #totalpred.write("\\newcommand{\\INVZJET}{\\ensuremath{\\PZ\\to\\Pgn\\Pagn+\\mathrm{jet}}\\xspace}\n")
    #totalpred.write("\\newcommand{\\INVZJETS}{\\ensuremath{\\INVZJET\\mathrm{s}}\\xspace}\n")
    totalpred.write("\\begin{document}\n")

    totalpred.write("""\\newsavebox{\zinvScaledTableBox}
\\begin{table}[htbp]
  \\fontsize{10 pt}{1.2 em}
  \\selectfont
  \\begin{centering}
    \\hspace*{-4ex}
    \\begin{lrbox}{\\zinvScaledTableBox}
      \\begin{tabular}{|ll||rllll|rl|}
        \\hline\n""")

    totalperpred.write("\\documentclass{article}\n")
    totalperpred.write("\\usepackage[english]{babel}\n")
    totalperpred.write("\\usepackage{mathtools}\n")
    totalperpred.write("\\usepackage{pdflscape}\n")
    totalperpred.write("\\usepackage{multirow}\n")
    totalperpred.write("\\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}\n")
    totalperpred.write("\\usepackage{xspace}\n")
    totalperpred.write("\\usepackage{marvosym}\n")
    totalperpred.write("\\usepackage{ifsym}\n")
    totalperpred.write("\\usepackage{savesym}\n")
    totalperpred.write("\\savesymbol{T}\n")
    totalperpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/ptdr-definitions.sty}\n")
    totalperpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pennames-pazo.sty}\n")
    totalperpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/sparticles.sty}\n")
    totalperpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pdefs}\n")
    totalperpred.write("\\restoresymbol{pdefs}{T}\n")
    #totalperpred.write("\\newcommand{\\INVZJET}{\\ensuremath{\\PZ\\to\\Pgn\\Pagn+\\mathrm{jet}}\\xspace}\n")
    #totalperpred.write("\\newcommand{\\INVZJETS}{\\ensuremath{\\INVZJET\\mathrm{s}}\\xspace}\n")
    totalperpred.write("\\begin{document}\n")

    totalperpred.write("""\\newsavebox{\zinvScaledTableBox}
\\begin{table}[htbp]
  \\fontsize{10 pt}{1.2 em}
  \\selectfont
  \\begin{centering}
    \\hspace*{-4ex}
    \\begin{lrbox}{\\zinvScaledTableBox}
      \\begin{tabular}{|ll||rllll|rl|}
      \\hline\n""")

    totaldatamcpred.write("\\documentclass{article}\n")
    totaldatamcpred.write("\\usepackage[english]{babel}\n")
    totaldatamcpred.write("\\usepackage{mathtools}\n")
    totaldatamcpred.write("\\usepackage{pdflscape}\n")
    totaldatamcpred.write("\\usepackage{multirow}\n")
    totaldatamcpred.write("\\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}\n")
    totaldatamcpred.write("\\usepackage{xspace}\n")
    totaldatamcpred.write("\\usepackage{marvosym}\n")
    totaldatamcpred.write("\\usepackage{ifsym}\n")
    totaldatamcpred.write("\\usepackage{savesym}\n")
    totaldatamcpred.write("\\savesymbol{T}\n")
    totaldatamcpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/ptdr-definitions.sty}\n")
    totaldatamcpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pennames-pazo.sty}\n")
    totaldatamcpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/sparticles.sty}\n")
    totaldatamcpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pdefs}\n")
    totaldatamcpred.write("\\restoresymbol{pdefs}{T}\n")
    #totaldatamcpred.write("\\newcommand{\\INVZJET}{\\ensuremath{\\PZ\\to\\Pgn\\Pagn+\\mathrm{jet}}\\xspace}\n")
    #totaldatamcpred.write("\\newcommand{\\INVZJETS}{\\ensuremath{\\INVZJET\\mathrm{s}}\\xspace}\n")
    totaldatamcpred.write("\\begin{document}\n")

    totaldatamcpred.write("""\\newsavebox{\zinvScaledTableBox}
\\begin{landscape}
  \\begin{table}[htbp]
    \\fontsize{10 pt}{1.2 em}
    \\selectfont
    \\begin{centering}
      \\hspace*{-4ex}
      \\begin{lrbox}{\\zinvScaledTableBox}
        \\begin{tabular}{|ll||rllll|rllll|rl|}
          \\hline\n""")

    totaldatamcperpred.write("\\documentclass{article}\n")
    totaldatamcperpred.write("\\usepackage[english]{babel}\n")
    totaldatamcperpred.write("\\usepackage{mathtools}\n")
    totaldatamcperpred.write("\\usepackage{pdflscape}\n")
    totaldatamcperpred.write("\\usepackage{multirow}\n")
    totaldatamcperpred.write("\\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}\n")
    totaldatamcperpred.write("\\usepackage{xspace}\n")
    totaldatamcperpred.write("\\usepackage{marvosym}\n")
    totaldatamcperpred.write("\\usepackage{ifsym}\n")
    totaldatamcperpred.write("\\usepackage{savesym}\n")
    totaldatamcperpred.write("\\savesymbol{T}\n")
    totaldatamcperpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/ptdr-definitions.sty}\n")
    totaldatamcperpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pennames-pazo.sty}\n")
    totaldatamcperpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/sparticles.sty}\n")
    totaldatamcperpred.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pdefs}\n")
    totaldatamcperpred.write("\\restoresymbol{pdefs}{T}\n")
    #totaldatamcperpred.write("\\newcommand{\\INVZJET}{\\ensuremath{\\PZ\\to\\Pgn\\Pagn+\\mathrm{jet}}\\xspace}\n")
    #totaldatamcperpred.write("\\newcommand{\\INVZJETS}{\\ensuremath{\\INVZJET\\mathrm{s}}\\xspace}\n")
    totaldatamcperpred.write("\\begin{document}\n")

    totaldatamcperpred.write("""\\newsavebox{\zinvScaledTableBox}
\\begin{landscape}
  \\begin{table}[htbp]
    \\fontsize{10 pt}{1.2 em}
    \\selectfont
    \\begin{centering}
      \\hspace*{-4ex}
      \\begin{lrbox}{\\zinvScaledTableBox}
        \\begin{tabular}{|ll||rllll|rllll|rl|}
          \\hline\n""")

    totalunc.write("\\documentclass{article}\n")
    totalunc.write("\\usepackage[english]{babel}\n")
    totalunc.write("\\usepackage{mathtools}\n")
    totalunc.write("\\usepackage{pdflscape}\n")
    totalunc.write("\\usepackage{multirow}\n")
    totalunc.write("\\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}\n")
    totalunc.write("\\usepackage{xspace}\n")
    totalunc.write("\\usepackage{marvosym}\n")
    totalunc.write("\\usepackage{ifsym}\n")
    totalunc.write("\\usepackage{savesym}\n")
    totalunc.write("\\savesymbol{T}\n")
    totalunc.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/ptdr-definitions.sty}\n")
    totalunc.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pennames-pazo.sty}\n")
    totalunc.write("\\input{/home/Frod014/research/thesis-sturdy/styles/sparticles.sty}\n")
    totalunc.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pdefs}\n")
    totalunc.write("\\restoresymbol{pdefs}{T}\n")
    #totalunc.write("\\newcommand{\\INVZJET}{\\ensuremath{\\PZ\\to\\Pgn\\Pagn+\\mathrm{jet}}\\xspace}\n")
    #totalunc.write("\\newcommand{\\INVZJETS}{\\ensuremath{\\INVZJET\\mathrm{s}}\\xspace}\n")
    totalunc.write("\\begin{document}\n")

    totalunc.write("""\\newsavebox{\zinvScaledTableBox}
\\begin{landscape}
  \\begin{table}[htbp]
    \\fontsize{10 pt}{1.2 em}
    \\selectfont
    \\begin{centering}
      \\hspace*{-4ex}
      \\begin{lrbox}{\\zinvScaledTableBox}
        \\begin{tabular}{|ll||r|llllllllll|}
          \\hline\n"""
                   )

    totalperunc.write("\\documentclass{article}\n")
    totalperunc.write("\\usepackage[english]{babel}\n")
    totalperunc.write("\\usepackage{mathtools}\n")
    totalperunc.write("\\usepackage{pdflscape}\n")
    totalperunc.write("\\usepackage{multirow}\n")
    totalperunc.write("\\usepackage[left=1cm,right=1cm,top=1cm,bottom=1cm]{geometry}\n")
    totalperunc.write("\\usepackage{xspace}\n")
    totalperunc.write("\\usepackage{marvosym}\n")
    totalperunc.write("\\usepackage{ifsym}\n")
    totalperunc.write("\\usepackage{savesym}\n")
    totalperunc.write("\\savesymbol{T}\n")
    totalperunc.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/ptdr-definitions.sty}\n")
    totalperunc.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pennames-pazo.sty}\n")
    totalperunc.write("\\input{/home/Frod014/research/thesis-sturdy/styles/sparticles.sty}\n")
    totalperunc.write("\\input{/home/Frod014/research/thesis-sturdy/styles/cmsStyles/pdefs}\n")
    totalperunc.write("\\restoresymbol{pdefs}{T}\n")
    #totalperunc.write("\\newcommand{\\INVZJET}{\\ensuremath{\\PZ\\to\\Pgn\\Pagn+\\mathrm{jet}}\\xspace}\n")
    #totalperunc.write("\\newcommand{\\INVZJETS}{\\ensuremath{\\INVZJET\\mathrm{s}}\\xspace}\n")
    totalperunc.write("\\begin{document}\n")

    totalperunc.write("""\\newsavebox{\zinvScaledTableBox}
\\begin{landscape}
  \\begin{table}[htbp]
    \\fontsize{10 pt}{1.2 em}
    \\selectfont
    \\begin{centering}
      \\hspace*{-4ex}
      \\begin{lrbox}{\\zinvScaledTableBox}
        \\begin{tabular}{|ll||r|llllllllll|}
          \\hline\n""")
##
    binnings = {}
    binnings[0] = [6,6,6,5,4]
    binnings[1] = [6,6,6,5,4]
    binnings[2] = [5,5,5,5,4]
    binnings[3] = [3,3,3,3,3]

    mhtBins = {}
    mhtBins[0] = [["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots 600","600\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots 600","600\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots 600","600\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots     "]]
    mhtBins[1] = [["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots 600","600\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots 600","600\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots 600","600\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots     "]]
    mhtBins[2] = [["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots 450","450\\ldots     "],
                  ["100\\ldots 200","200\\ldots 300","300\\ldots     "]]
    mhtBins[3] = [["100\\ldots 200","200\\ldots     "],
                  ["100\\ldots 200","200\\ldots     "],
                  ["100\\ldots 200","200\\ldots     "],
                  ["100\\ldots 200","200\\ldots     "],
                  ["100\\ldots 200","200\\ldots     "]]

    predVals     = []
    predStatErrs = []
    predValsSystUP   = []
    predValsSystDN   = []
    predValsTheoryUP = []
    predValsTheoryDN = []
    predValsTotalUP  = []
    predValsTotalDN  = []

    for h,hist in enumerate(histoNames):
        print hist
        dataHist  = dataInputFile.Get("htvsmht_%s_%s"%("scaled",hist[0]))
        zinvHist  = zinvInputFile.Get("htvsmht_%s_%s"%("scaled",hist[0]))
        mcHist    = mcInputFile.Get("htvsmht_%s_%s"%("scaled",hist[0]))
        ##gjetsHist = gjetsInputFile.Get("htvsmht_%s_%s"%("scaled",hist[0]))
        dataHistAcceptanceUP   = dataInputFile.Get("htvsmht_%s_%s"%("predictionAcceptanceUP",hist[0]))
        dataHistAcceptanceDN   = dataInputFile.Get("htvsmht_%s_%s"%("predictionAcceptanceDN",hist[0]))
        dataHistRecoUP    = dataInputFile.Get("htvsmht_%s_%s"%("predictionRecoUP",hist[0]))
        dataHistRecoDN    = dataInputFile.Get("htvsmht_%s_%s"%("predictionRecoDN",hist[0]))
        dataHistPixelUP   = dataInputFile.Get("htvsmht_%s_%s"%("predictionPixelUP",hist[0]))
        dataHistPixelDN   = dataInputFile.Get("htvsmht_%s_%s"%("predictionPixelDN",hist[0]))
        dataHistIsoUP     = dataInputFile.Get("htvsmht_%s_%s"%("predictionIsoUP",hist[0]))
        dataHistIsoDN     = dataInputFile.Get("htvsmht_%s_%s"%("predictionIsoDN",hist[0]))
        dataHistDataMCUP  = dataInputFile.Get("htvsmht_%s_%s"%("predictionDataMCUP",hist[0]))
        dataHistDataMCDN  = dataInputFile.Get("htvsmht_%s_%s"%("predictionDataMCDN",hist[0]))

        dataHistSystUP   = dataInputFile.Get("htvsmht_%s_%s"%("predictionSystUP",hist[0]))
        dataHistSystDN   = dataInputFile.Get("htvsmht_%s_%s"%("predictionSystDN",hist[0]))
        dataHistTheoryUP = dataInputFile.Get("htvsmht_%s_%s"%("predictionTheoryUP",hist[0]))
        dataHistTheoryDN = dataInputFile.Get("htvsmht_%s_%s"%("predictionTheoryDN",hist[0]))
        dataHistTotalUP  = dataInputFile.Get("htvsmht_%s_%s"%("predictionTotalUP",hist[0]))
        dataHistTotalDN  = dataInputFile.Get("htvsmht_%s_%s"%("predictionTotalDN",hist[0]))

        dataHistPurUP      = dataInputFile.Get("htvsmht_%s_%s"%("predictionPurityUP",hist[0]))
        dataHistPurDN      = dataInputFile.Get("htvsmht_%s_%s"%("predictionPurityDN",hist[0]))
        dataHistPhenoUP    = dataInputFile.Get("htvsmht_%s_%s"%("predictionPhenoUP",hist[0]))
        dataHistPhenoDN    = dataInputFile.Get("htvsmht_%s_%s"%("predictionPhenoDN",hist[0]))
        dataHistThFitUP    = dataInputFile.Get("htvsmht_%s_%s"%("predictionThFitUP",hist[0]))
        dataHistThFitDN    = dataInputFile.Get("htvsmht_%s_%s"%("predictionThFitDN",hist[0]))
        dataHistThDoubleUP = dataInputFile.Get("htvsmht_%s_%s"%("predictionThDoubleUP",hist[0]))
        dataHistThDoubleDN = dataInputFile.Get("htvsmht_%s_%s"%("predictionThDoubleDN",hist[0]))

        mcHistAcceptanceUP   = mcInputFile.Get("htvsmht_%s_%s"%("predictionAcceptanceUP",hist[0]))
        mcHistAcceptanceDN   = mcInputFile.Get("htvsmht_%s_%s"%("predictionAcceptanceDN",hist[0]))
        mcHistRecoUP    = mcInputFile.Get("htvsmht_%s_%s"%("predictionRecoUP",hist[0]))
        mcHistRecoDN    = mcInputFile.Get("htvsmht_%s_%s"%("predictionRecoDN",hist[0]))
        mcHistPixelUP   = mcInputFile.Get("htvsmht_%s_%s"%("predictionPixelUP",hist[0]))
        mcHistPixelDN   = mcInputFile.Get("htvsmht_%s_%s"%("predictionPixelDN",hist[0]))
        mcHistIsoUP     = mcInputFile.Get("htvsmht_%s_%s"%("predictionIsoUP",hist[0]))
        mcHistIsoDN     = mcInputFile.Get("htvsmht_%s_%s"%("predictionIsoDN",hist[0]))
        mcHistDataMCUP  = mcInputFile.Get("htvsmht_%s_%s"%("predictionDataMCUP",hist[0]))
        mcHistDataMCDN  = mcInputFile.Get("htvsmht_%s_%s"%("predictionDataMCDN",hist[0]))

        mcHistSystUP   = mcInputFile.Get("htvsmht_%s_%s"%("predictionSystUP",hist[0]))
        mcHistSystDN   = mcInputFile.Get("htvsmht_%s_%s"%("predictionSystDN",hist[0]))
        mcHistTheoryUP = mcInputFile.Get("htvsmht_%s_%s"%("predictionTheoryUP",hist[0]))
        mcHistTheoryDN = mcInputFile.Get("htvsmht_%s_%s"%("predictionTheoryDN",hist[0]))
        mcHistTotalUP  = mcInputFile.Get("htvsmht_%s_%s"%("predictionTotalUP",hist[0]))
        mcHistTotalDN  = mcInputFile.Get("htvsmht_%s_%s"%("predictionTotalDN",hist[0]))

        mcHistPurUP      = mcInputFile.Get("htvsmht_%s_%s"%("predictionPurityUP",hist[0]))
        mcHistPurDN      = mcInputFile.Get("htvsmht_%s_%s"%("predictionPurityDN",hist[0]))
        mcHistPhenoUP    = mcInputFile.Get("htvsmht_%s_%s"%("predictionPhenoUP",hist[0]))
        mcHistPhenoDN    = mcInputFile.Get("htvsmht_%s_%s"%("predictionPhenoDN",hist[0]))
        mcHistThFitUP    = mcInputFile.Get("htvsmht_%s_%s"%("predictionThFitUP",hist[0]))
        mcHistThFitDN    = mcInputFile.Get("htvsmht_%s_%s"%("predictionThFitDN",hist[0]))
        mcHistThDoubleUP = mcInputFile.Get("htvsmht_%s_%s"%("predictionThDoubleUP",hist[0]))
        mcHistThDoubleDN = mcInputFile.Get("htvsmht_%s_%s"%("predictionThDoubleDN",hist[0]))

        datapred.write("  \\begin{table}[h]\n")
        datapred.write("    \\footnotesize\n")
        datapred.write("    \\centering\n")
        datapred.write("    \\begin{tabular}{|l|l|l|l|l|l|}\n")
        datapred.write("      \\hline\n")
        datapred.write("      %s & $100<\\slash{H_{T}}<200$ & $200<\\slash{H_{T}}<300$ & $300<\\slash{H_{T}}<450$ & $450<\\slash{H_{T}}<600$ & $600<\\slash{H_{T}}$   \\\\\n"%(hist[1]))
        datapred.write("      \\hline\n")

        zinvest.write("      \\hline\n")
        zinvest.write("      \\multicolumn{6}{|l|}{%s}  \\\\\n"%(hist[1]))
        zinvest.write("      \\hline\n")

        if hist[0]=="dijet":
            totalpred.write("        %%%%no-dijets%%%%\\multicolumn{2}{|c||}{%s}& Data-driven \
& \\multicolumn{4}{c|}{uncertainty} & Z$\\rightarrow\\nu\\nu+$jets (NNLO) & uncertainty\\\\\n"%(hist[1]))
            totalpred.write("        %%%%no-dijets%%%%\\HT [GeV] & \\MHT [GeV]                \
& prediction  & stat.   & syst. & pheno. & tot. & MC expectation     & stat.\\\\\n")
            totalpred.write("        %%%%no-dijets%%%%\\hline\n")
            
            totalperpred.write("      %%%%no-dijets%%%%\\multicolumn{2}{|c||}{%s}& Data-driven \
& \\multicolumn{4}{c|}{uncertainty} & Z$\\rightarrow\\nu\\nu+$jets (NNLO) & uncertainty\\\\\n"%(hist[1]))
            totalperpred.write("      %%%%no-dijets%%%%\\HT [GeV] & \\MHT [GeV]                \
& prediction  & stat.   & syst. & pheno. & tot. & MC expectation     & stat.\\\\\n")
            totalperpred.write("      %%%%no-dijets%%%%\\hline\n")
            
            totaldatamcpred.write("          %%%%no-dijets%%%%\\multicolumn{2}{|c||}{%s}& Data-driven \
& \\multicolumn{4}{c|}{uncertainty} & Data-driven & \\multicolumn{4}{c|}{uncertainty} \
& Z$\\rightarrow\\nu\\nu+$jets (NNLO) & uncertainty\\\\\n"%(hist[1]))
            totaldatamcpred.write("          %%%%no-dijets%%%%\\HT [GeV] & \\MHT [GeV]  & prediction on MC  \
& stat.   & syst. & pheno. & tot. & prediction on data  & stat.   & syst. & pheno. & tot. \
& MC expectation     & stat.\\\\\n")
            totaldatamcpred.write("          %%%%no-dijets%%%%\\hline\n")
            
            totaldatamcperpred.write("          %%%%no-dijets%%%%\\multicolumn{2}{|c||}{%s}& Data-driven \
& \\multicolumn{4}{c|}{uncertainty [\\%%]} & Data-driven & \\multicolumn{4}{c|}{uncertainty [\\%%]} \
& Z$\\rightarrow\\nu\\nu+$jets (NNLO) & uncertainty [\\%%]\\\\\n"%(hist[1]))
            totaldatamcperpred.write("          %%%%no-dijets%%%%\\HT [GeV] & \\MHT [GeV]  & prediction on MC  \
& stat.   & syst. & pheno. & tot. & prediction on data  & stat.   & syst. & pheno. & tot. \
& MC expectation     & stat.\\\\\n")
            totaldatamcperpred.write("          %%%%no-dijets%%%%\\hline\n")
            
        ###\\begin{tabular}{|ll||r|l|lllll|l|lll|}
            totalunc.write("          %%%%no-dijets%%%%\\multicolumn{2}{|c||}{%s}& Data-driven \
& \\multicolumn{10}{c|}{uncertainties} \\\\\n"%(hist[1]))
            totalunc.write("          %%%%no-dijets%%%%\\HT [GeV] & \\MHT [GeV]  & prediction  \
& stat.   & acc. & reco & pixel veto & isolation & data/mc SF & purity & ratio \
& pheno. fit & pheno. double \\\\\n")
            totalunc.write("          %%%%no-dijets%%%%\\hline\n")
            
            totalperunc.write("          %%%%no-dijets%%%%\\multicolumn{2}{|c||}{%s}& Data-driven \
& \\multicolumn{10}{c|}{percent uncertainties} \\\\\n"%(hist[1]))
            totalperunc.write("          %%%%no-dijets%%%%\\HT [GeV] & \\MHT [GeV]  & prediction  \
& stat.   & acc. & reco & pixel veto & isolation & data/mc SF & purity & ratio \
& pheno. fit & pheno. double \\\\\n")
            totalperunc.write("          %%%%no-dijets%%%%\\hline\n")
        else:
            totalpred.write("        \\multicolumn{2}{|c||}{%s}& Data-driven & \\multicolumn{4}{c|}{uncertainty} \
& Z$\\rightarrow\\nu\\nu+$jets (NNLO) & uncertainty\\\\\n"%(hist[1]))
            totalpred.write("        \\HT [GeV] & \\MHT [GeV]                      & prediction  & stat.   \
& syst. & pheno. & tot. & MC expectation     & stat.\\\\\n")
            totalpred.write("        \\hline\n")
            
            totalperpred.write("      \\multicolumn{2}{|c||}{%s}& Data-driven & \\multicolumn{4}{c|}{uncertainty} \
& Z$\\rightarrow\\nu\\nu+$jets (NNLO) & uncertainty\\\\\n"%(hist[1]))
            totalperpred.write("      \\HT [GeV] & \\MHT [GeV]                      & prediction  & stat.   \
& syst. & pheno. & tot. & MC expectation     & stat.\\\\\n")
            totalperpred.write("      \\hline\n")
            
            totaldatamcpred.write("          \\multicolumn{2}{|c||}{%s}& Data-driven & \\multicolumn{4}{c|}{uncertainty} \
& Data-driven & \\multicolumn{4}{c|}{uncertainty} & Z$\\rightarrow\\nu\\nu+$jets (NNLO) & uncertainty\\\\\n"%(hist[1]))
            totaldatamcpred.write("          \\HT [GeV] & \\MHT [GeV]  & prediction on MC  & stat.   & syst. & pheno. & tot. \
& prediction on data  & stat.   & syst. & pheno. & tot. & MC expectation     & stat.\\\\\n")
            totaldatamcpred.write("          \\hline\n")
            
            totaldatamcperpred.write("          \\multicolumn{2}{|c||}{%s}& Data-driven & \\multicolumn{4}{c|}{uncertainty [\\%%]} \
& Data-driven & \\multicolumn{4}{c|}{uncertainty [\\%%]} & Z$\\rightarrow\\nu\\nu+$jets (NNLO) & uncertainty [\\%%]\\\\\n"%(hist[1]))
            totaldatamcperpred.write("          \\HT [GeV] & \\MHT [GeV]  & prediction on MC  & stat.   & syst. & pheno. & tot. \
& prediction on data  & stat.   & syst. & pheno. & tot. & MC expectation     & stat.\\\\\n")
            totaldatamcperpred.write("          \\hline\n")
            
        ###\\begin{tabular}{|ll||r|l|lllll|l|lll|}
            totalunc.write("          \\multicolumn{2}{|c||}{%s}& Data-driven & \\multicolumn{10}{c|}{uncertainties} \\\\\n"%(hist[1]))
            totalunc.write("          \\HT [GeV] & \\MHT [GeV]  & prediction  & stat.   & acc. & reco & pixel veto \
& isolation & data/mc SF & purity & ratio & pheno. fit & pheno. double \\\\\n")
            totalunc.write("          \\hline\n")
            
            totalperunc.write("          \\multicolumn{2}{|c||}{%s}& Data-driven & \\multicolumn{10}{c|}{percent uncertainties} \\\\\n"%(hist[1]))
            totalperunc.write("          \\HT [GeV] & \\MHT [GeV]  & prediction  & stat.   & acc. & reco & pixel veto \
& isolation & data/mc SF & purity & ratio & pheno. fit & pheno. double \\\\\n")
            totalperunc.write("          \\hline\n")


        for xbin in range(dataHist.GetNbinsX()):
            myxbin = xbin+1
            if myxbin < 2:
                continue

            datapred.write("      %s "%(htBins[xbin-1][0]))
            zinvest.write("      %s "%(htBins[xbin-1][0]))
                
            for ybin in range(dataHist.GetNbinsY()):
                myybin = ybin+1
                if myybin<2 or myxbin < 2:
                    continue
                if myxbin<3 and myybin<3:
                    #f.write("& \\multicolumn{2}{c|}{-} ")
                    datapred.write("& - ")
                    zinvest.write("& - ")
                    continue
                if myybin > binnings[h][xbin-1]:
                    continue

                xbinlow = myxbin
                xbinhigh = myxbin
                
                ybinlow = myybin
                ybinhigh = myybin
                
                if myxbin == dataHist.GetNbinsX():
                    xbinhigh = -1
                if myybin == binnings[h][xbin-1]:
                    ybinhigh = -1
                    
                ##print("%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                if hist[0]=="dijet":
                    if myybin == 2:
                        totalpred.write("        %%%%no-dijets%%%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totalperpred.write("      %%%%no-dijets%%%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totaldatamcpred.write("          %%%%no-dijets%%%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totaldatamcperpred.write("          %%%%no-dijets%%%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totalunc.write("          %%%%no-dijets%%%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totalperunc.write("          %%%%no-dijets%%%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    else:
                        totalpred.write("        %%%%no-dijets%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totalperpred.write("      %%%%no-dijets%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totaldatamcpred.write("          %%%%no-dijets%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totaldatamcperpred.write("          %%%%no-dijets%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totalunc.write("          %%%%no-dijets%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                        totalperunc.write("          %%%%no-dijets%%%%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                elif myybin == 2:
                    totalpred.write("        %%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totalperpred.write("      %%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totaldatamcpred.write("          %%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totaldatamcperpred.write("          %%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totalunc.write("          %%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totalperunc.write("          %%%s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                else:
                    totalpred.write("        %s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totalperpred.write("      %s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totaldatamcpred.write("          %s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totaldatamcperpred.write("          %s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totalunc.write("          %s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                    totalperunc.write("          %s & %s"%(htBins[xbin-1][1],mhtBins[h][xbin-1][ybin-1]))
                binStatError = r.Double(0)
                #print dataHist.GetXaxis().GetBinLowEdge(xbinlow),dataHist.GetXaxis().GetBinLowEdge(xbinhigh+1),dataHist.GetYaxis().GetBinLowEdge(ybinlow),dataHist.GetYaxis().GetBinLowEdge(ybinhigh+1)
                binPrediction = dataHist.IntegralAndError(xbinlow,xbinhigh,ybinlow,ybinhigh,binStatError,"")

                binPredSystUP   = dataHistSystUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredSystDN   = dataHistSystDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredTheoryUP = dataHistTheoryUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredTheoryDN = dataHistTheoryDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredTotalUP  = dataHistTotalUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredTotalDN  = dataHistTotalDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)


                binAccSystUP    = dataHistAcceptanceUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binAccSystDN    = dataHistAcceptanceDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binRecoSystUP   = dataHistRecoUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binRecoSystDN   = dataHistRecoDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPixelSystUP  = dataHistPixelUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPixelSystDN  = dataHistPixelDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binIsoSystUP    = dataHistIsoUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binIsoSystDN    = dataHistIsoDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binDataMCSystUP = dataHistDataMCUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binDataMCSystDN = dataHistDataMCDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)

                binPurSystUP   = dataHistPurUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPurSystDN   = dataHistPurDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)

                binPredPhenoUP     = dataHistPhenoUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredPhenoDN     = dataHistPhenoDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredTheoryFitUP = dataHistThFitUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredTheoryFitDN = dataHistThFitDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredThDoubleUP  = dataHistThDoubleUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                binPredThDoubleDN  = dataHistThDoubleDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)

                mcBinStatError = r.Double(0)
                mcBinPrediction = mcHist.IntegralAndError(xbinlow,xbinhigh,ybinlow,ybinhigh,mcBinStatError,"")

                mcBinPredSystUP   = mcHistSystUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredSystDN   = mcHistSystDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredTheoryUP = mcHistTheoryUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredTheoryDN = mcHistTheoryDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredTotalUP  = mcHistTotalUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredTotalDN  = mcHistTotalDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)


                mcBinAccSystUP    = mcHistAcceptanceUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinAccSystDN    = mcHistAcceptanceDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinRecoSystUP   = mcHistRecoUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinRecoSystDN   = mcHistRecoDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPixelSystUP  = mcHistPixelUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPixelSystDN  = mcHistPixelDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinIsoSystUP    = mcHistIsoUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinIsoSystDN    = mcHistIsoDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinDataMCSystUP = mcHistDataMCUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinDataMCSystDN = mcHistDataMCDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)

                mcBinPurSystUP   = mcHistPurUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPurSystDN   = mcHistPurDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)

                mcBinPredPhenoUP     = mcHistPhenoUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredPhenoDN     = mcHistPhenoDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredTheoryFitUP = mcHistThFitUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredTheoryFitDN = mcHistThFitDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredThDoubleUP  = mcHistThDoubleUP.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)
                mcBinPredThDoubleDN  = mcHistThDoubleDN.Integral(xbinlow,xbinhigh,ybinlow,ybinhigh)

                zinvStatError = r.Double(0)
                zinvPrediction = zinvHist.IntegralAndError(xbinlow,xbinhigh,ybinlow,ybinhigh,zinvStatError,"")

                predErrsSystUP   = binPredSystUP  -binPrediction
                predErrsSystDN   = binPrediction  -binPredSystDN
                predErrsTheoryUP = binPredTheoryUP-binPrediction
                predErrsTheoryDN = binPrediction  -binPredTheoryDN
                predErrsTotalUP  = binPredTotalUP -binPrediction
                predErrsTotalDN  = binPrediction  -binPredTotalDN

                acceptanceErrsSystUP = binAccSystUP   -binPrediction
                acceptanceErrsSystDN = binPrediction  -binAccSystDN
                recoIDErrsSystUP     = binRecoSystUP  -binPrediction
                recoIDErrsSystDN     = binPrediction  -binRecoSystDN
                pixelVetoErrsSystUP  = binPixelSystUP -binPrediction
                pixelVetoErrsSystDN  = binPrediction  -binPixelSystDN
                isolationErrsSystUP  = binIsoSystUP   -binPrediction
                isolationErrsSystDN  = binPrediction  -binIsoSystDN
                datamcErrsSystUP     = binDataMCSystUP-binPrediction
                datamcErrsSystDN     = binPrediction  -binDataMCSystDN

                purityErrsSystUP     = binPurSystUP -binPrediction
                purityErrsSystDN     = binPrediction-binPurSystDN

                predErrsPhenoUP     = binPredPhenoUP    -binPrediction
                predErrsPhenoDN     = binPrediction     -binPredPhenoDN
                predErrsTheoryFitUP = binPredTheoryFitUP-binPrediction
                predErrsTheoryFitDN = binPrediction     -binPredTheoryFitDN
                predErrsThDoubleUP  = binPredThDoubleUP -binPrediction
                predErrsThDoubleDN  = binPrediction     -binPredThDoubleDN

                #####Prediction performed using the MC
                predMCErrsSystUP   = mcBinPredSystUP  -mcBinPrediction
                predMCErrsSystDN   = mcBinPrediction  -mcBinPredSystDN
                predMCErrsTheoryUP = mcBinPredTheoryUP-mcBinPrediction
                predMCErrsTheoryDN = mcBinPrediction  -mcBinPredTheoryDN
                predMCErrsTotalUP  = mcBinPredTotalUP -mcBinPrediction
                predMCErrsTotalDN  = mcBinPrediction  -mcBinPredTotalDN

                acceptanceMCErrsSystUP = mcBinAccSystUP   -mcBinPrediction
                acceptanceMCErrsSystDN = mcBinPrediction  -mcBinAccSystDN
                recoIDMCErrsSystUP     = mcBinRecoSystUP  -mcBinPrediction
                recoIDMCErrsSystDN     = mcBinPrediction  -mcBinRecoSystDN
                pixelVetoMCErrsSystUP  = mcBinPixelSystUP -mcBinPrediction
                pixelVetoMCErrsSystDN  = mcBinPrediction  -mcBinPixelSystDN
                isolationMCErrsSystUP  = mcBinIsoSystUP   -mcBinPrediction
                isolationMCErrsSystDN  = mcBinPrediction  -mcBinIsoSystDN
                datamcMCErrsSystUP     = mcBinDataMCSystUP-mcBinPrediction
                datamcMCErrsSystDN     = mcBinPrediction  -mcBinDataMCSystDN

                purityMCErrsSystUP     = mcBinPurSystUP -mcBinPrediction
                purityMCErrsSystDN     = mcBinPrediction-mcBinPurSystDN

                predMCErrsPhenoUP     = mcBinPredPhenoUP    -mcBinPrediction
                predMCErrsPhenoDN     = mcBinPrediction     -mcBinPredPhenoDN
                predMCErrsTheoryFitUP = mcBinPredTheoryFitUP-mcBinPrediction
                predMCErrsTheoryFitDN = mcBinPrediction     -mcBinPredTheoryFitDN
                predMCErrsThDoubleUP  = mcBinPredThDoubleUP -mcBinPrediction
                predMCErrsThDoubleDN  = mcBinPrediction     -mcBinPredThDoubleDN

                nonZeroBinPrediction = binPrediction
                if not (binPrediction > 0):
                    print "found zero bin prediction, setting up alternate method"
                    sys.stdout.flush()
                    nonZeroBinPrediction = 10000000000000000000
                    ### set up the uncertainties to be taken from the GJets for stat, syst., pheno., and tot.
                    ###dataMCSigTree = r.TChain("gjets")
                    ###dataMCSigTree.Add("new/gen_fits_2to8_bin0_new_zmumuGammaData.root")
                    mcMCSigTree   = r.TChain("gjets")
                    #mcMCSigTree.Add("%s/../gen_fits_2to8_bin0_new_zmumuGammaMC.root"%(options.inDir))
                    mcMCSigTree.Add("%s/gen_fits_2to8_bin0_new_zmumuGammaMC.root"%(options.inDir))
                    
                    myRatioHisto = r.TH1D("ratioHisto","ratioHisto",5000,-20,20)

                    htLow   = dataHist.GetXaxis().GetBinLowEdge(xbinlow)
                    htHigh  = dataHist.GetXaxis().GetBinLowEdge(xbinhigh+1)
                    mhtLow  = dataHist.GetYaxis().GetBinLowEdge(ybinlow)
                    mhtHigh = dataHist.GetYaxis().GetBinLowEdge(ybinhigh+1)
                    if htHigh<0:
                        htHigh = 8000
                    if mhtHigh<0:
                        mhtHigh = 5000

                    mcMCSigTree.Draw(
                        "scaleFactor>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatio = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorThUP>>ratioHisto" ,"eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioMCUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorTotUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioMCTotUP = myRatioHisto.GetMean()

                    ## value of 1.841 comes from Garwood interval around a Poisson
                    # observation of 0
                    ## Garwood intervals on Poisson observation of 0 [asymmetric], [symmetric]
                    ##68%    [0,1.1394], [0,1.8326]
                    ##68.27% [0,1.1479], [0,1.8411]
                    ##90%    [0,2.3026], [0,2.9957]
                    ##95%    [0,2.9957], [0,3.6889]
                    ##99%    [0,4.6052], [0,5.2983]
                    ##prob = 0.6827
                    ##bound = 1.0-prob
                    ##halfbound = bound/2.0
                    ##symmetric interval: -math.log(halfbound)
                    ##asymmetric interval:-math.log(bound)
                    binStatError     = 1.841*phenoRatio
                    predErrsSystUP   = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioUP)
                    predErrsTheoryUP = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioMCUP)
                    predErrsTotalUP  = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioMCTotUP)

                    mcMCSigTree.Draw(
                        "scaleFactorAccUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioAccUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorIDUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioRecoIDUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorPixUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioPixelUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorIsoUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioIsoUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorDMCSFUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioDataMCUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorPurUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioPurityUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorPhenUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioPhenoUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorThFitUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioThFitUP = myRatioHisto.GetMean()
                    mcMCSigTree.Draw(
                        "scaleFactorThDoubleUP>>ratioHisto","eventWeight*(nJets>7&&ht>%d&&ht<%d&&mht>%d&&mht<%d)"%(
                            htLow,htHigh,mhtLow,mhtHigh),
                        "texte")
                    phenoRatioThDoubleUP = myRatioHisto.GetMean()
                    acceptanceErrsSystUP = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioAccUP)
                    recoIDErrsSystUP     = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioRecoIDUP)
                    pixelVetoErrsSystUP  = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioPixelUP)
                    isolationErrsSystUP  = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioIsoUP)
                    datamcErrsSystUP     = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioDataMCUP)
                    purityErrsSystUP     = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioPurityUP)
                    predErrsPhenoUP      = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioPhenoUP)
                    predErrsTheoryFitUP  = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioThFitUP)
                    predErrsThDoubleUP   = unFoldErrors(1.841*phenoRatio,1.841*phenoRatioThDoubleUP)
                    print "found empty prediction bin %d < ht < %d, %d < mht < %d"%(
                        htLow,htHigh,mhtLow,mhtHigh)
                    print phenoRatioThDoubleUP,acceptanceErrsSystUP,recoIDErrsSystUP,pixelVetoErrsSystUP,isolationErrsSystUP,datamcErrsSystUP,purityErrsSystUP,predErrsPhenoUP,predErrsTheoryFitUP,predErrsThDoubleUP
                    sys.stdout.flush()
                    ##end treatment of empty prediction

                nonZeroBinZInvPrediction = zinvPrediction
                if not (zinvPrediction > 0):
                    nonZeroBinZInvPrediction = 10000000000000000000

                nonZeroMCBinPrediction = mcBinPrediction
                if not (mcBinPrediction > 0):
                    nonZeroMCBinPrediction = 10000000000000000000

                if myybin == binnings[h][xbin-1]:
                    datapred.write(""" &\\multicolumn{%d}{l|}{%2.2f$\\pm$%2.2f (stat.) $\\substack{\\left(^{+%2.2f}_{-%2.2f} \\mathrm{syst.}\\right) \\\\ \
\\left(\\pm%2.2f \\mathrm{theo.}\\right) \\\\ \\left(^{+%2.2f}_{-%2.2f} \\mathrm{tot.}\\right)}$} \\\\\n"""%(6+1-myybin,binPrediction,
                                                                                                             binStatError,predErrsSystUP,
                                                                                                             predErrsSystDN,predErrsTheoryUP,
                                                                                                             predErrsTotalUP,predErrsTotalDN))
                    datapred.write("      \\hline\n")
                    zinvest.write(" &\\multicolumn{%d}{l|}{%2.2f$\\pm$%2.2f} \\\\\n"%(6+1-myybin, zinvPrediction,zinvStatError))

                    totalpred.write("  & %2.2f& $\\pm$ %2.2f & $^{+%2.2f}_{-%2.2f}$ & $\\pm %2.2f$ & $^{+%2.2f}_{-%2.2f}$ & %2.2f& $\\pm$ %2.2f \\\\\n"%(binPrediction,binStatError,
                                                                                                                                                         predErrsSystUP,predErrsSystDN,
                                                                                                                                                         predErrsTheoryUP,
                                                                                                                                                         #math.sqrt((binStatError*binStatError)+(predErrsTotalUP*predErrsTotalUP)),
                                                                                                                                                         #math.sqrt((binStatError*binStatError)+(predErrsTotalDN*predErrsTotalDN)),
                                                                                                                                                         predErrsTotalUP,predErrsTotalDN,
                                                                                                                                                         zinvPrediction,zinvStatError))

                    totalperpred.write("""  & %2.2f& $\\pm$ %2.2f\\%% & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ & $\\pm %2.2f\\%%$ & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ \
& %2.2f& $\\pm$ %2.2f\\%% \\\\\n"""%(binPrediction,binStatError/nonZeroBinPrediction*100,
                                     predErrsSystUP/nonZeroBinPrediction*100,predErrsSystDN/nonZeroBinPrediction*100,
                                     predErrsTheoryUP/nonZeroBinPrediction*100,
                                     #math.sqrt((binStatError*binStatError)+(predErrsTotalUP*predErrsTotalUP))/nonZeroBinPrediction*100,
                                     #math.sqrt((binStatError*binStatError)+(predErrsTotalDN*predErrsTotalDN))/nonZeroBinPrediction*100,
                                     predErrsTotalUP/nonZeroBinPrediction*100,predErrsTotalDN/nonZeroBinPrediction*100,
                                     zinvPrediction,zinvStatError/nonZeroBinZInvPrediction*100))
                    
                    totaldatamcpred.write("""& %2.2f& $\\pm$ %2.2f & $^{+%2.2f}_{-%2.2f}$ & $\\pm %2.2f$ & $^{+%2.2f}_{-%2.2f}$ \
& %2.2f& $\\pm$ %2.2f & $^{+%2.2f}_{-%2.2f}$ & $\\pm %2.2f$ & $^{+%2.2f}_{-%2.2f}$ \
& %2.2f& $\\pm$ %2.2f \\\\\n"""%(mcBinPrediction,mcBinStatError,
                                 predMCErrsSystUP,predMCErrsSystDN,
                                 predMCErrsTheoryUP,
                                 #math.sqrt((mcBinStatError*mcBinStatError)+(predMCErrsTotalUP*predMCErrsTotalUP)),
                                 #math.sqrt((mcBinStatError*mcBinStatError)+(predMCErrsTotalDN*predMCErrsTotalDN)),
                                 predMCErrsTotalUP,predMCErrsTotalDN,
                                 binPrediction,binStatError,
                                 predErrsSystUP,predErrsSystDN,
                                 predErrsTheoryUP,
                                 #math.sqrt((binStatError*binStatError)+(predErrsTotalUP*predErrsTotalUP)),
                                 #math.sqrt((binStatError*binStatError)+(predErrsTotalDN*predErrsTotalDN)),
                                 predErrsTotalUP,predErrsTotalDN,
                                 zinvPrediction,zinvStatError)
                                          )

                    totaldatamcperpred.write("""& %2.2f& $\\pm$ %2.2f\\%% & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ & $\\pm %2.2f\\%%$ & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ \
& %2.2f& $\\pm$ %2.2f\\%% & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ & $\\pm %2.2f\\%%$ & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ \
& %2.2f& $\\pm$ %2.2f\\%% \\\\\n"""%(mcBinPrediction,mcBinStatError/nonZeroMCBinPrediction*100,
                                     predMCErrsSystUP/nonZeroMCBinPrediction*100,predMCErrsSystDN/nonZeroMCBinPrediction*100,
                                     predMCErrsTheoryUP/nonZeroMCBinPrediction*100,
                                     #math.sqrt((mcBinStatError*mcBinStatError)+(predMCErrsTotalUP*predMCErrsTotalUP))/nonZeroMCBinPrediction*100,
                                     #math.sqrt((mcBinStatError*mcBinStatError)+(predMCErrsTotalDN*predMCErrsTotalDN))/nonZeroMCBinPrediction*100,
                                     predMCErrsTotalUP/nonZeroMCBinPrediction*100,predMCErrsTotalDN/nonZeroMCBinPrediction*100,
                                     binPrediction,binStatError/nonZeroBinPrediction*100,
                                     predErrsSystUP/nonZeroBinPrediction*100,predErrsSystDN/nonZeroBinPrediction*100,
                                     predErrsTheoryUP/nonZeroBinPrediction*100,
                                     #math.sqrt((binStatError*binStatError)+(predErrsTotalUP*predErrsTotalUP))/nonZeroBinPrediction*100,
                                     #math.sqrt((binStatError*binStatError)+(predErrsTotalDN*predErrsTotalDN))/nonZeroBinPrediction*100,
                                     predErrsTotalUP/nonZeroBinPrediction*100,predErrsTotalDN/nonZeroBinPrediction*100,
                                     zinvPrediction,zinvStatError/nonZeroBinZInvPrediction*100)
                                             )
                    
                    
                    totalunc.write("""  & %2.2f& $\\pm$ %2.2f & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ \
& $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ \\\\\n"""%(binPrediction,binStatError,
                                                                                                                              acceptanceErrsSystUP,acceptanceErrsSystDN,
                                                                                                                              recoIDErrsSystUP,recoIDErrsSystDN,
                                                                                                                              pixelVetoErrsSystUP,pixelVetoErrsSystDN,
                                                                                                                              isolationErrsSystUP,isolationErrsSystDN,
                                                                                                                              datamcErrsSystUP,datamcErrsSystDN,
                                                                                                                              
                                                                                                                              purityErrsSystUP,purityErrsSystDN,
                                                                                                                              
                                                                                                                              predErrsPhenoUP,predErrsPhenoDN,
                                                                                                                              predErrsTheoryFitUP,predErrsTheoryFitDN,
                                                                                                                              predErrsThDoubleUP,predErrsThDoubleDN
                                                                                                                              ))

                    totalperunc.write("""  & %2.2f & $\\pm$ %2.2f \\%% & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ \
& $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ \
& $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ \\\\\n"""%(binPrediction,binStatError/nonZeroBinPrediction*100,
                                                                                                              acceptanceErrsSystUP/nonZeroBinPrediction*100,acceptanceErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              recoIDErrsSystUP/nonZeroBinPrediction*100,recoIDErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              pixelVetoErrsSystUP/nonZeroBinPrediction*100,pixelVetoErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              isolationErrsSystUP/nonZeroBinPrediction*100,isolationErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              datamcErrsSystUP/nonZeroBinPrediction*100,datamcErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              
                                                                                                              purityErrsSystUP/nonZeroBinPrediction*100,purityErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              
                                                                                                              predErrsPhenoUP/nonZeroBinPrediction*100,predErrsPhenoDN/nonZeroBinPrediction*100,
                                                                                                              predErrsTheoryFitUP/nonZeroBinPrediction*100,predErrsTheoryFitDN/nonZeroBinPrediction*100,
                                                                                                              predErrsThDoubleUP/nonZeroBinPrediction*100,predErrsThDoubleDN/nonZeroBinPrediction*100
                                                                                                              ))

                    if hist[0]=="dijet":
                        totalpred.write("        %%%%no-dijets%%%%\\hline\n")
                        totalperpred.write("      %%%%no-dijets%%%%\\hline\n")
                        totaldatamcpred.write("          %%%%no-dijets%%%%\\hline\n")
                        totaldatamcperpred.write("          %%%%no-dijets%%%%\\hline\n")
                        totalunc.write("          %%%%no-dijets%%%%\\hline\n")
                        totalperunc.write("          %%%%no-dijets%%%%\\hline\n")
                    else:
                        totalpred.write("        \\hline\n")
                        totalperpred.write("      \\hline\n")
                        totaldatamcpred.write("          \\hline\n")
                        totaldatamcperpred.write("          \\hline\n")
                        totalunc.write("          \\hline\n")
                        totalperunc.write("          \\hline\n")

                    #f.write("&%2.2f$\\pm$ %2.2f &\\multicolumn{%d}{l|}{%2.2f$\\pm$ %2.2f} \\\\\n"%(binPrediction,binStatError,2*6+1-2*myybin,zinvPrediction,zinvStatError))
                else:
                    datapred.write("""&  %2.2f$\\pm$ %2.2f (stat.) $\\substack{\\left(^{+%2.2f}_{-%2.2f} \\mathrm{syst.}\\right) \\\\ \\left(\\pm%2.2f \\mathrm{theo.}\\right) \\\\ \
\\left(^{+%2.2f}_{-%2.2f} \\mathrm{tot.}\\right)}$ \n"""%(binPrediction,binStatError,predErrsSystUP,predErrsSystDN,predErrsTheoryUP,predErrsTotalUP,predErrsTotalDN))
                    zinvest.write("&  %2.2f$\\pm$ %2.2f "%(zinvPrediction,zinvStatError))
                    totalpred.write("""  & %2.2f& $\\pm$ %2.2f & $^{+%2.2f}_{-%2.2f}$ & $\\pm %2.2f$ & $^{+%2.2f}_{-%2.2f}$ \
& %2.2f& $\\pm$ %2.2f \\\\\n"""%(binPrediction,binStatError,
                                 predErrsSystUP,predErrsSystDN,
                                 predErrsTheoryUP,
                                 predErrsTotalUP,predErrsTotalDN,
                                 zinvPrediction,zinvStatError))
                    
                    totalperpred.write("""  & %2.2f& $\\pm$ %2.2f\\%% & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ & $\\pm %2.2f\\%%$ & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ \
& %2.2f& $\\pm$ %2.2f\\%% \\\\\n"""%(binPrediction,binStatError/nonZeroBinPrediction*100,
                                     predErrsSystUP/nonZeroBinPrediction*100,predErrsSystDN/nonZeroBinPrediction*100,
                                     predErrsTheoryUP/nonZeroBinPrediction*100,
                                     predErrsTotalUP/nonZeroBinPrediction*100,predErrsTotalDN/nonZeroBinPrediction*100,
                                     zinvPrediction,zinvStatError/nonZeroBinZInvPrediction*100))
                    
                    totaldatamcpred.write("""& %2.2f& $\\pm$ %2.2f & $^{+%2.2f}_{-%2.2f}$ & $\\pm %2.2f$ & $^{+%2.2f}_{-%2.2f}$ \
& %2.2f& $\\pm$ %2.2f & $^{+%2.2f}_{-%2.2f}$ & $\\pm %2.2f$ & $^{+%2.2f}_{-%2.2f}$ \
& %2.2f& $\\pm$ %2.2f \\\\\n"""%(mcBinPrediction,mcBinStatError,
                                 predMCErrsSystUP,predMCErrsSystDN,
                                 predMCErrsTheoryUP,
                                 predMCErrsTotalUP,predMCErrsTotalDN,
                                 binPrediction,binStatError,
                                 predErrsSystUP,predErrsSystDN,
                                 predErrsTheoryUP,
                                 predErrsTotalUP,predErrsTotalDN,
                                 zinvPrediction,zinvStatError)
                                          )

                    totaldatamcperpred.write("""& %2.2f& $\\pm$ %2.2f\\%% & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ & $\\pm %2.2f\\%%$ & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ \
& %2.2f& $\\pm$ %2.2f\\%% & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ & $\\pm %2.2f\\%%$ & $^{+%2.2f\\%%}_{-%2.2f\\%%}$ \
& %2.2f& $\\pm$ %2.2f\\%% \\\\\n"""%(mcBinPrediction,mcBinStatError/nonZeroMCBinPrediction*100,
                                     predMCErrsSystUP/nonZeroMCBinPrediction*100,predMCErrsSystDN/nonZeroMCBinPrediction*100,
                                     predMCErrsTheoryUP/nonZeroMCBinPrediction*100,
                                     predMCErrsTotalUP/nonZeroMCBinPrediction*100,predMCErrsTotalDN/nonZeroMCBinPrediction*100,
                                     binPrediction,binStatError/nonZeroBinPrediction*100,
                                     predErrsSystUP/nonZeroBinPrediction*100,predErrsSystDN/nonZeroBinPrediction*100,
                                     predErrsTheoryUP/nonZeroBinPrediction*100,
                                     predErrsTotalUP/nonZeroBinPrediction*100,predErrsTotalDN/nonZeroBinPrediction*100,
                                     zinvPrediction,zinvStatError/nonZeroBinZInvPrediction*100)
                                             )
                    
                    
                    totalunc.write("""  & %2.2f& $\\pm$ %2.2f & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ \
& $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ & $^{+%2.2f}_{-%2.2f}$ \\\\\n"""%(binPrediction,binStatError,
                                                                                                                              acceptanceErrsSystUP,acceptanceErrsSystDN,
                                                                                                                              recoIDErrsSystUP,recoIDErrsSystDN,
                                                                                                                              pixelVetoErrsSystUP,pixelVetoErrsSystDN,
                                                                                                                              isolationErrsSystUP,isolationErrsSystDN,
                                                                                                                              datamcErrsSystUP,datamcErrsSystDN,
                                                                                                                              
                                                                                                                              purityErrsSystUP,purityErrsSystDN,
                                                                                                                              
                                                                                                                              predErrsPhenoUP,predErrsPhenoDN,
                                                                                                                              predErrsTheoryFitUP,predErrsTheoryFitDN,
                                                                                                                              predErrsThDoubleUP,predErrsThDoubleDN
                                                                                                                              ))

                    totalperunc.write("""  & %2.2f & $\\pm$ %2.2f \\%% & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ \
& $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ \
& $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ & $^{+%2.2f \\%%}_{-%2.2f \\%%}$ \\\\\n"""%(binPrediction,binStatError/nonZeroBinPrediction*100,
                                                                                                              acceptanceErrsSystUP/nonZeroBinPrediction*100,acceptanceErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              recoIDErrsSystUP/nonZeroBinPrediction*100,recoIDErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              pixelVetoErrsSystUP/nonZeroBinPrediction*100,pixelVetoErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              isolationErrsSystUP/nonZeroBinPrediction*100,isolationErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              datamcErrsSystUP/nonZeroBinPrediction*100,datamcErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              
                                                                                                              purityErrsSystUP/nonZeroBinPrediction*100,purityErrsSystDN/nonZeroBinPrediction*100,
                                                                                                              
                                                                                                              predErrsPhenoUP/nonZeroBinPrediction*100,predErrsPhenoDN/nonZeroBinPrediction*100,
                                                                                                              predErrsTheoryFitUP/nonZeroBinPrediction*100,predErrsTheoryFitDN/nonZeroBinPrediction*100,
                                                                                                              predErrsThDoubleUP/nonZeroBinPrediction*100,predErrsThDoubleDN/nonZeroBinPrediction*100
                                                                                                              ))
                    #f.write("&  %2.2f$\\pm$ %2.2f & %2.2f$\\pm$ %2.2f"%(binPrediction,binStatError,zinvPrediction,zinvStatError))
                if not hist[0]=="dijet":
                    if myybin > 2:
                        #print "dataHist.IntegralAndError(%d,%d,%d,%d,binStatError,\"\") = %2.2f+/-%2.2f"%(xbinlow,xbinhigh,ybinlow,ybinhigh,binPrediction,binStatError)
                        predVals.append(binPrediction)
                        predValsSystUP.append(predErrsSystUP)
                        predValsSystDN.append(predErrsSystDN)
                        predValsTheoryUP.append(predErrsTheoryUP)
                        predValsTheoryDN.append(predErrsTheoryDN)
                        predValsTotalUP.append(predErrsTotalUP)
                        predValsTotalDN.append(predErrsTotalDN)
                        ##predValsSystUP.append(binPredSystUP-binPrediction)
                        ##predValsSystDN.append(binPrediction-binPredSystDN)
                        ##predValsTheoryUP.append(binPredTheoryUP-binPrediction)
                        ##predValsTheoryDN.append(binPrediction-binPredTheoryDN)
                        ##predValsTotalUP.append(binPredTotalUP-binPrediction)
                        ##predValsTotalDN.append(binPrediction-binPredTotalDN)
                        predStatErrs.append(binStatError)
                        dc.write("    %2.2f"%(binPrediction))
                        
        datapred.write("      \\hline\n")
        datapred.write("    \\end{tabular}\n")
        datapred.write("    \\caption{Z$\\rightarrow\\nu\\nu+$jets predictions from %s for %s\n"%(options.sample,hist[1]))
        datapred.write("      \\label{tab:%s_zinv_%s_%s_prediction}}\n"%(options.sample,extra,hist[0]))
        datapred.write("  \\end{table}\n\n\n")

        totalpred.write("        \\hline\n")
        totalperpred.write("      \\hline\n")
        totaldatamcpred.write("          \\hline\n")
        totaldatamcperpred.write("          \\hline\n")
        totalunc.write("          \\hline\n")
        totalperunc.write("          \\hline\n")

            
    datapred.write("\\end{landscape}\n")
    datapred.write("\\end{document}\n")
    datapred.close()

    zinvest.write("      \\hline\n")
    zinvest.write("    \\end{tabular}\n")
    zinvest.write("    \\caption{Z$\\rightarrow\\nu\\nu+$jets MC expectation\n")
    zinvest.write("      \\label{tab:zinv_expectation}}\n")
    zinvest.write("  \\end{table}\n")
    zinvest.write("\\end{landscape}\n")
    zinvest.write("\\end{document}\n")
    zinvest.close()

    totalpred.write("""        \\end{tabular}
      \\end{lrbox}
      \\scalebox{0.80}{\\usebox{\\zinvScaledTableBox}}
      \\caption{Z$\\rightarrow\\nu\\nu+$jets predictions from $\\gamma+$jets data
        \\label{tab:%s_zinv_%s_prediction}}
    \\par\\end{centering}
  \\end{table}
\\end{document}\n"""%(options.sample,extra))
    totalpred.close()

    totalperpred.write("""        \\end{tabular}
      \\end{lrbox}
      \\scalebox{0.80}{\\usebox{\\zinvScaledTableBox}}
      \\caption{Z$\\rightarrow\\nu\\nu+$jets predictions from $\\gamma+$jets data
        \\label{tab:%s_zinv_%s_prediction_percent_uncertainties}}
    \\par\\end{centering}
  \\end{table}
\\end{document}\n"""%(options.sample,extra))
    totalperpred.close()

    totaldatamcpred.write("""        \\end{tabular}
      \\end{lrbox}
      \\scalebox{0.80}{\\usebox{\\zinvScaledTableBox}}
      \\caption{Z$\\rightarrow\\nu\\nu+$jets predictions from $\\gamma+$jets data
        \\label{tab:%s_zinv_%s_prediction}}
    \\par\\end{centering}
  \\end{table}
\\end{landscape}
\\end{document}\n"""%(options.sample,extra))
    totaldatamcpred.close()

    totaldatamcperpred.write("""        \\end{tabular}
      \\end{lrbox}
      \\scalebox{0.80}{\\usebox{\\zinvScaledTableBox}}
      \\caption{Z$\\rightarrow\\nu\\nu+$jets predictions from $\\gamma+$jets data
        \\label{tab:%s_zinv_%s_prediction_percent_uncertainties}}
    \\par\\end{centering}
  \\end{table}
\\end{landscape}
\\end{document}\n"""%(options.sample,extra))
    totaldatamcperpred.close()

    totalunc.write("""        \\end{tabular}
      \\end{lrbox}
      \\scalebox{0.80}{\\usebox{\\zinvScaledTableBox}}
      \\caption{Z$\\rightarrow\\nu\\nu+$jets uncertainties from $\\gamma+$jets data
        \\label{tab:%s_zinv_%s_uncertainties}}
    \\par\\end{centering}
  \\end{table}
\\end{landscape}
\\end{document}\n"""%(options.sample,extra))
    totalunc.close()

    totalperunc.write("""        \\end{tabular}
      \\end{lrbox}
      \\scalebox{0.80}{\\usebox{\\zinvScaledTableBox}}
      \\caption{Z$\\rightarrow\\nu\\nu+$jets percent uncertainties from $\\gamma+$jets data
        \\label{tab:%s_zinv_%s_percent_uncertainties}}
    \\par\\end{centering}
  \\end{table}
\\end{landscape}
\\end{document}\n"""%(options.sample,extra))
    totalunc.close()

    dc.write("""\n
# Uncertainties --> at least stat. and syst.
nuisance = stat.; theory; syst.; total
zinvis_uncertaintyDistribution_1 = lnN
zinvis_uncertaintyDistribution_2 = lnN
#zinvis_uncertaintyDistribution_3 = lnN
#zinvis_uncertaintyDistribution_4 = lnN\n""")

    print len(predStatErrs)
    dc.write("zinvis_uncertainty_1 =")
    for err in predStatErrs:
        dc.write("    %2.2f"%(err))
    dc.write("\nzinvis_uncertaintyUP_2 =")
    for err in predValsTotalUP:
        dc.write("    %2.2f"%(err))
    dc.write("\nzinvis_uncertaintyDN_2 =")
    for err in predValsTotalDN:
        dc.write("    %2.2f"%(err))
    dc.write("\n#zinvis_uncertaintyUP_3 =")
    for err in predValsSystUP:
        dc.write("    %2.2f"%(err))
    dc.write("\n#zinvis_uncertaintyDN_3 =")
    for err in predValsSystDN:
        dc.write("    %2.2f"%(err))
    dc.write("\n#zinvis_uncertainty_4 =")
    for err in predValsTheoryUP:
        dc.write("    %2.2f"%(err))
    #dc.write("\nzinvis_uncertaintyDN_4 =")
    #for err in predValsTotalDN:
    #    dc.write("    %2.2f"%(err))

    ##for h,hist in enumerate(histoNames):
    ##    print hist
    ##    dataHist  = dataInputFile.Get(hist[0])
    ##    ##zinvHist  = zinvInputFile.Get(hist[0])
    ##    ##gjetsHist = gjetsInputFile.Get(hist[0])
    ##    for xbin in range(dataHist.GetNbinsX()):
    ##        myxbin = xbin+1
    ##        for ybin in range(dataHist.GetNbinsY()):
    ##            myybin = ybin+1
    ##            if myybin<2 or myxbin < 2:
    ##                continue
    ##            if myxbin<3 and myybin<3:
    ##                continue
    ##            if myybin > binnings[h][xbin-1]:
    ##                continue
    ##            
    ##            xbinlow = myxbin
    ##            xbinhigh = myxbin
    ##            
    ##            ybinlow = myybin
    ##            ybinhigh = myybin
    ##            
    ##            if myxbin == dataHist.GetNbinsX():
    ##                xbinhigh = -1
    ##            if myybin == binnings[h][xbin-1]:
    ##                ybinhigh = -1
    ##            #if myybin == dataHist.GetNbinsY():
    ##            #    ybinhigh = -1
    ##
    ##            binStatError = r.Double(0)
    ##            binPrediction = dataHist.IntegralAndError(xbinlow,xbinhigh,ybinlow,ybinhigh,binStatError,"")
    ##            if not hist[0]=="htvsmht_scaled_dijet":
    ##                if myybin > 2:
    ##                    print "dataHist.IntegralAndError(%d,%d,%d,%d,binStatError,\"\") = %2.2f+/-%2.2f"%(xbinlow,xbinhigh,ybinlow,ybinhigh,binPrediction,binStatError)
    ##                    dc.write("    %2.2f"%(binStatError))

    dc.write("\n")
    dc.close()

def unFoldErrors(statErr, totErr):
    ##total error = sqrt(stat2+syst2)
    ## tot2 = stat2 + syst2
    ## syst2 = tot2 - stat2
    ## syst = sqrt(tot2 - stat2)
    
    return math.sqrt((totErr*totErr) - (statErr*statErr))


####very end####
if __name__ == '__main__':
    main()

