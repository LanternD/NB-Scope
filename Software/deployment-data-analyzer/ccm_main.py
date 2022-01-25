from CellCoverageMeasurementProcessor import CellCoverageMeasurementProcessor
from Utils import *
import time


whoami = 'dy'  # 'ls', 'xh'

def ccm_main():
    print(INFO, 'Cell Coverage Map Plot')
    ccmp = CellCoverageMeasurementProcessor(whoami)
    ccmp.pipeline()


if __name__ == '__main__':
    start_time = time.time()

    ccm_main()

    print('Total execution time: {0:.4f} s'.format(time.time()-start_time))
