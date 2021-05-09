from multiprocessing import Pool
from functools import partial
import sys, getopt
  
#################################################################################

# Appends the current matrix to output file
def writeMatrix(outfile, matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            outfile.write(matrix[i][j])
        outfile.write("\n")
    
# Compute the matrix. Accepts n as a parameter which represents which
# thread is calling this function; used to determine which part of the
# matrix will be computed.
def computeMatrix(n, matr, rPP, pCount): #(current proc number, matrix,
                                         # rows per proc, proc count)
    cellRow = []                                
    cellGrid = []
    start = n * rPP
    stop = start + rPP
    numRows = len(matr)
    numCols = len(matr[0])
    
    # if last thread, task it with any leftover rows
    if n == pCount-1:
        while stop != numRows:                   
            stop += 1

    # compute matrix
    for i in range(start, stop):                
        for j in range(numCols):  #iterate through each cell            
            
            # find number of live neighbors
            num = 0
            for cn in range(-1,2):
                for rn in range(-1,2):  
                    if not (rn==0 and cn==0): #exclude the cell that is input (i,j)
                        #check neighboring cell (i+rn,j+cn)
                        if matr[(i+rn)%numRows][(j+cn)%numCols] == 'O':
                            num += 1
                            
            cell = '.' # let cell be dead by default                
            # if cell in current gen is alive and has 2, 3, or 4 live
            # neighbors, make it alive for next gen                
            if matr[i][j] == 'O':
                if num==2 or num==3 or num==4:
                    cell = 'O'
                    
            # if cell in current gen is dead and has an even number
            # of live neighbors > 0, make it alive next gen
            else:
                if num>0 and num%2==0: 
                    cell = 'O'
            
            
            cellRow.append(cell)
        cellGrid.append(cellRow)
        cellRow = []        
    return [n,cellGrid]

#END OF COMPUTE MATRIX#
#################################################################################

def main(argv):

    procCount = 1
    # Command line arguments:
    try:
        opts, args = getopt.getopt(argv,"i:o:t:")
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> -t <threads>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            infilename = arg
        elif opt == '-o':
            outfilename = arg
        elif opt == '-t':
            procCount = int(arg)


    
    infile = open(infilename, 'r')
    
    # Make a pool of processes
    procPool = Pool(procCount)
    
    # Matrix init:
    matrix = []
    i = 0
    for line in infile:
        rowArray = line.strip()
        rowSize = len(rowArray)
        if rowSize > 0:
            if i>0 and cols != rowSize:
                print("Error: unequal row size")
                sys.exit(1)
            cols = rowSize
            for j in range(rowSize):
                cell = rowArray[j]
                if not (rowArray[j] == '.' or rowArray[j] == 'O'):
                    print("Error: invalid symbol in file")
                    sys.exit(1)
                       
            matrix.append(rowArray)
            i += 1
            
    rowsPerProc = i//procCount
    #infile.close()
    
    print("Project :: R11525907")
    
    finalized = []
    # Execute the steps
    for step in range(1,101):
        # pass in the arguments that won't change
        constArgs = partial(computeMatrix,matr=matrix,rPP=rowsPerProc,pCount=procCount)
        # map the pool to compute different segments
        # cellMatrices will contain a list of lists [n, [[row1],[row2],...]],...
        cellMatrices = procPool.map(constArgs, range(procCount))
        # sort by n
        cellMatrices.sort()

        # put it all in order into one matrix
        for n in range(len(cellMatrices)):
            for i in range(len(cellMatrices[n][1])):
                finalized.append(cellMatrices[n][1][i])
                #print(cellMatrices[n][1][i])
            
        # finalize matrix
        matrix = finalized       
        finalized = []

    outfile = open(outfilename, 'w')
    writeMatrix(outfile, matrix)
    #outfile.close()


if __name__ == '__main__':
    main(sys.argv[1:])
