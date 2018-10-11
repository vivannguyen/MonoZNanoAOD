import sys, os
import argparse

crab_template = """
import sys
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName     = '{JOBNAME}'
config.General.workArea        = '/afs/cern.ch/user/y/yhaddad/work/MonoZ/crab/'
config.General.transferOutputs = True
config.General.transferLogs    = True
config.JobType.pluginName      = 'Analysis'
config.JobType.psetName        = 'PSet.py'
config.JobType.scriptExe       = 'crab_script.sh'

config.JobType.scriptArgs = [
    'isMC={ISMC}',
    'era=2017',
    'doSyst=0',
    'dataRun=X'
]

config.JobType.inputFiles = [
    '../keep_and_drop.txt',
    '../postproc.py',
    '../haddnano.py'
]

config.JobType.sendPythonFolder	       = True
config.Data.inputDataset               = '{DATASET}'
config.Data.inputDBS                   = 'global'
config.Data.splitting                  = 'FileBased'
config.Data.unitsPerJob                = 1
config.Data.outLFNDirBase              = '/store/user/yhaddad/MonoZAnalysis'
config.Data.publication                = False
config.Data.outputDatasetTag           = '{OUTPUTTAG}'
config.Data.allowNonValidInputDataset  = True
config.JobType.allowUndistributedCMSSW = True
config.Site.storageSite                = 'T2_CH_CERN'

sites=['T2_CH_CERN']
"""


parser = argparse.ArgumentParser()
parser.add_argument("-i"   , "--inputs", type=str, default="data.txt", help="")
parser.add_argument("-isMC", "--isMC"  , type=int, default=1         , help="")

options = parser.parse_args()
proc_args = [ "'isMC=%i'" % options.isMC, "'era=2017'", "'doSyst=0'", "'dataRun=X'"]

print(" configuration :", options.inputs )
with open(options.inputs, 'r') as stream:
    for sample in stream.read().split('\n'):
        if '#' in sample: continue
	if len(sample.split('/')) <= 1: continue
	
	tag = sample.split("/")[1]
	if not options.isMC:
		tag = sample.split("/")[1] + "_" + sample.split("/")[2]
	crab_config = crab_template.replace("{JOBNAME}", "1110_data_" + tag)
        crab_config = crab_config.replace("{DATASET}", sample)
        crab_config = crab_config.replace("{ISMC}", str(options.isMC) )
        crab_config = crab_config.replace("{OUTPUTTAG}", "MonoZ2017_1110_data")
        crab_file = "job_submit_%s.py" % tag
        os.system("rm -f " +  crab_file)
	with open(crab_file, 'a') as the_file:
    		the_file.write(crab_config)

        cmd = "crab submit " + crab_file
        print cmd
        os.system(cmd)