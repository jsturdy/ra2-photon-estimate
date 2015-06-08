######change 15.03.2013 to 27.11.2013
export BASE_OUT_DIR=/media/btrfs/research/BackgroundStudies/ZInvisible/Photons/03.12.2013
echo $BASE_OUT_DIR/LO/corrected
mkdir -p $BASE_OUT_DIR/scripts
cp -rfp runFitting.sh makeDataCard.py makeFitFunctions_corrected.py histoInformation.py makeDoubleRatios.py makeDoubleRatios_v3.py makeDoubleRatios_v4.py makeDoubleRatios_v5.py makePredictionPlots.py $BASE_OUT_DIR/scripts
#export BASE_HOME_DIR=/media/btrfs/research/BackgroundStudies/ZInvisible/Photons/28.01.2013/
#cd $BASE_OUT_DIR

##
### running the LO setup and scripts
python makeDoubleRatios.py    -i $BASE_OUT_DIR -o $BASE_OUT_DIR/LO >&$BASE_OUT_DIR/making.doubles.lo
python makeDoubleRatios_v3.py -i $BASE_OUT_DIR -o $BASE_OUT_DIR/LO >&$BASE_OUT_DIR/making.doubles.lo.v3
python makeDoubleRatios_v4.py -i $BASE_OUT_DIR -o $BASE_OUT_DIR/LO >&$BASE_OUT_DIR/making.doubles.lo.v4
python makeDoubleRatios_v5.py -i $BASE_OUT_DIR -o $BASE_OUT_DIR/LO >&$BASE_OUT_DIR/making.doubles.lo.v5

### running the NNLO setup and scripts
python makeDoubleRatios.py    -i $BASE_OUT_DIR -n -o $BASE_OUT_DIR/NNLO >&$BASE_OUT_DIR/making.doubles.nnlo
python makeDoubleRatios_v3.py -i $BASE_OUT_DIR -n -o $BASE_OUT_DIR/NNLO >&$BASE_OUT_DIR/making.doubles.nnlo.v3
python makeDoubleRatios_v4.py -i $BASE_OUT_DIR -n -o $BASE_OUT_DIR/NNLO >&$BASE_OUT_DIR/making.doubles.nnlo.v4
python makeDoubleRatios_v5.py -i $BASE_OUT_DIR -n -o $BASE_OUT_DIR/NNLO >&$BASE_OUT_DIR/making.doubles.nnlo.v5

##LO fitting jobs
mkdir -p $BASE_OUT_DIR/LO/original
python makeFitFunctions.py -i $BASE_OUT_DIR/LO -o $BASE_OUT_DIR/LO/original -g -r 2 -f 0 >&$BASE_OUT_DIR/LO/original/gen.fits.bins0.range2.REMFSO.new.out&
python makeFitFunctions.py -i $BASE_OUT_DIR/LO -o $BASE_OUT_DIR/LO/original -g -r 2 -z -f 0 >&$BASE_OUT_DIR/LO/original/gen.fits.bins0.range2.zmumuMC.REMFSO.new.out&

mkdir -p $BASE_OUT_DIR/LO/corrected
python makeFitFunctions_corrected.py -i $BASE_OUT_DIR/LO -o $BASE_OUT_DIR/LO/corrected -g -r 2 -f 0 >&$BASE_OUT_DIR/LO/corrected/gen.fits.bins0.range2.REMFSO.new.out&
python makeFitFunctions_corrected.py -i $BASE_OUT_DIR/LO -o $BASE_OUT_DIR/LO/corrected -g -r 2 -z -f 0 >&$BASE_OUT_DIR/LO/corrected/gen.fits.bins0.range2.zmumuMC.REMFSO.new.out&


##NNLO fitting jobs
mkdir -p $BASE_OUT_DIR/NNLO/original
python makeFitFunctions.py -i $BASE_OUT_DIR/NNLO -o $BASE_OUT_DIR/NNLO/original -g -r 2 -f 0 >&$BASE_OUT_DIR/NNLO/original/gen.fits.bins0.range2.REMFSO.new.out&
python makeFitFunctions.py -i $BASE_OUT_DIR/NNLO -o $BASE_OUT_DIR/NNLO/original -g -r 2 -z -f 0 >&$BASE_OUT_DIR/NNLO/original/gen.fits.bins0.range2.zmumuMC.REMFSO.new.out&

mkdir -p $BASE_OUT_DIR/NNLO/corrected
python makeFitFunctions_corrected.py -i $BASE_OUT_DIR/NNLO -o $BASE_OUT_DIR/NNLO/corrected -g -r 2 -f 0 >&$BASE_OUT_DIR/NNLO/corrected/gen.fits.bins0.range2.REMFSO.new.out&
python makeFitFunctions_corrected.py -i $BASE_OUT_DIR/NNLO -o $BASE_OUT_DIR/NNLO/corrected -g -r 2 -z -f 0 >&$BASE_OUT_DIR/NNLO/corrected/gen.fits.bins0.range2.zmumuMC.REMFSO.new.out&

##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 -z >& /dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 -s gjets -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 -s mc -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 -s zinv -z >&/dev/null&
##
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 -s gjets -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 -s mc -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 -s zinv -z >&/dev/null&
##
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 -s gjets >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 -s mc >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 -s zinv >&/dev/null&
##
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 -s gjets >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 -s mc >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 -s zinv >&/dev/null&
##
######NNLO jobs
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 -s gjets -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 -s mc -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 -s zinv -z >&/dev/null&
##
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 -s gjets -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 -s mc -z >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 -s zinv -z >&/dev/null&
##
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 -s gjets >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 -s mc >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 -s zinv >&/dev/null&
##
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 -s gjets >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 -s mc >&/dev/null&
##python makePredictionPlots.py -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 -s zinv >&/dev/null&

##last step##### make predictions on the LO ratios
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2 -z          >&$BASE_OUT_DIR/LO/original/gen.data.bins0.range2.zmumumc.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -s gjets -g -r 2 -z -b 0 >&$BASE_OUT_DIR/LO/original/gen.gjets.bins0.range2.zmumumc.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -s mc -g -r 2 -z -b 0    >&$BASE_OUT_DIR/LO/original/gen.mc.bins0.range2.zmumumc.new.out
##last step##
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -b 0 -g -r 2          >&$BASE_OUT_DIR/LO/original/gen.data.bins0.range2.zmumudata.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -s gjets -g -r 2 -b 0 >&$BASE_OUT_DIR/LO/original/gen.gjets.bins0.range2.zmumudata.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/original -o $BASE_OUT_DIR/LO/original -s mc -g -r 2 -b 0    >&$BASE_OUT_DIR/LO/original/gen.mc.bins0.range2.zmumudata.new.out
##last step##
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2 -z          >&$BASE_OUT_DIR/LO/corrected/gen.data.bins0.range2.zmumumc.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -s gjets -g -r 2 -z -b 0 >&$BASE_OUT_DIR/LO/corrected/gen.gjets.bins0.range2.zmumumc.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -s mc -g -r 2 -z -b 0    >&$BASE_OUT_DIR/LO/corrected/gen.mc.bins0.range2.zmumumc.new.out
##last step##
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -b 0 -g -r 2          >&$BASE_OUT_DIR/LO/corrected/gen.data.bins0.range2.zmumudata.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -s gjets -g -r 2 -b 0 >&$BASE_OUT_DIR/LO/corrected/gen.gjets.bins0.range2.zmumudata.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/LO/corrected -o $BASE_OUT_DIR/LO/corrected -s mc -g -r 2 -b 0    >&$BASE_OUT_DIR/LO/corrected/gen.mc.bins0.range2.zmumudata.new.out
##last step##
##last step##### make predictions on the NNLO ratios
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2 -z          >&$BASE_OUT_DIR/NNLO/original/gen.data.bins0.range2.zmumumc.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -s gjets -g -r 2 -z -b 0 >&$BASE_OUT_DIR/NNLO/original/gen.gjets.bins0.range2.zmumumc.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -s mc -g -r 2 -z -b 0    >&$BASE_OUT_DIR/NNLO/original/gen.mc.bins0.range2.zmumumc.new.out
##last step##
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -b 0 -g -r 2          >&$BASE_OUT_DIR/NNLO/original/gen.data.bins0.range2.zmumudata.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -s gjets -g -r 2 -b 0 >&$BASE_OUT_DIR/NNLO/original/gen.gjets.bins0.range2.zmumudata.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/original -o $BASE_OUT_DIR/NNLO/original -s mc -g -r 2 -b 0    >&$BASE_OUT_DIR/NNLO/original/gen.mc.bins0.range2.zmumudata.new.out
##last step##
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2 -z          >&$BASE_OUT_DIR/NNLO/corrected/gen.data.bins0.range2.zmumumc.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -s gjets -g -r 2 -z -b 0 >&$BASE_OUT_DIR/NNLO/corrected/gen.gjets.bins0.range2.zmumumc.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -s mc -g -r 2 -z -b 0    >&$BASE_OUT_DIR/NNLO/corrected/gen.mc.bins0.range2.zmumumc.new.out
##last step##
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -b 0 -g -r 2          >&$BASE_OUT_DIR/NNLO/corrected/gen.data.bins0.range2.zmumudata.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -s gjets -g -r 2 -b 0 >&$BASE_OUT_DIR/NNLO/corrected/gen.gjets.bins0.range2.zmumudata.new.out
##last step##python makeDataCard.py  -i $BASE_OUT_DIR/NNLO/corrected -o $BASE_OUT_DIR/NNLO/corrected -s mc -g -r 2 -b 0    >&$BASE_OUT_DIR/NNLO/corrected/gen.mc.bins0.range2.zmumudata.new.out

