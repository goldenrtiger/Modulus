import csv
import matplotlib.pyplot as plt
import numpy as np

class Text:
    @staticmethod
    def ReadSamples( path ):
        samples = []
        with open( path, newline='' ) as file:
            reader = csv.reader( file)
            for row in reader:
                if row: samples.append( row )

        return samples

    @staticmethod
    def WriteTxt( name, contents ):
        with open( name, 'w' ) as file:
            return file.write( contents )

    @staticmethod
    def WriteCSV( ):
        pass

    @staticmethod
    def ListToString( l ):
        return " ".join( str(x) for x in l )

    @staticmethod
    def List2DToString( l2D ):
        string = ""

        for l in l2D:
            string += Text.ListToString( l )
            string += "\n"

        return string

class Field:
    hRow = 0
    bRow = 1
    LRow = 2
    hCol = 1
    bCol = 1
    LCol = 1

    sDRow = 6
    sDCol = 1
    sLRow = 6
    sLCol = 2

class FlexuralCalc:
    def __init__( self, path ):
        self.samples = Text.ReadSamples( path )
        self.stress = []
        self.strain = []
        self.strStressStrain = ''
        self.Extract( )

    def Extract( self ):
        self.h = float( self.samples[ Field.hRow ][ Field.hCol ] )
        self.b = float( self.samples[ Field.bRow ][ Field.bCol ] )
        self.L = float( self.samples[ Field.LRow ][ Field.LCol ] )

        self.d = []
        self.load = [] # kgf
        sDRow = Field.sDRow
        sLRow = Field.sLRow

        self.strStressStrain += "h: " + str( self.h ) + ", b: " + str( self.b ) + ", L: " + str( self.L ) + "\n "

        for i in range( len(self.samples[ sDRow: ] ) ):
            self.d.append( float( self.samples[ sDRow ][ Field.sDCol ] ) )
            self.load.append( float( self.samples[ sLRow ][ Field.sLCol ] ) )
            sDRow += 1
            sLRow += 1

    def CalcTrueCurve( self, strain, stress ):
        """
            Mechanical Properties of Materials: https://mechanicalc.com/reference/mechanical-properties-of-materials#:~:text=Ramberg%2DOsgood%20equation.-,True%20Stress%20and%20Strain,actual%20area%20of%20the%20specimen
        """
        pass

    def Apply( self ):
        '''
            Formula: 
                stress: (3*Load * 9.80665*L)/(2*b*POWER(h,2))
                strain: 6*d*h/(POWER(L,2))
        '''
        for i in range( len( self.d ) ):
            d, load = self.d[i], self.load[i]
            stress = ( 3 * load * 9.8065 * self.L ) / ( 2 * self.b * self.h * self.h )
            strain = ( 6 * d * self.h ) / ( self.L * self.L )
            self.stress.append( stress ) 
            self.strain.append( strain )
            self.strStressStrain += ( str(stress) + " " + str(strain) + " \n ")

        end_strain = 0.008
        start_strain = 0.002
        end, _ = FindNearest( self.strain, end_strain )
        start, _ = FindNearest( self.strain, start_strain )
        
        # start = 10
        # end = 45
        m = ( self.stress[end] - self.stress[start] ) / ( self.strain[end] - self.strain[start] )

        return [m, self.h, self.b]

def FindNearest( array, value ):
    array = np.asarray( array )
    idx = ( np.abs( array - value ) ).argmin()

    return idx, array[ idx ]


def Plot( stress, strain ):
    num = len( stress )
    rows, cols = 3, 5
    fig, axes = plt.subplots( 3, 5 )
    legend = []

    for r in range( rows ):
        for c in range( cols ):
            num = r * cols + c

            line1 = axes[r][c].plot( strain[num * 3], stress[num * 3] )
            line2 = axes[r][c].plot( strain[num * 3 + 1], stress[num * 3 + 1] )
            line3 = axes[r][c].plot( strain[num * 3 + 2], stress[num * 3 + 2] )

            axes[r][c].legend(('1', '2', '3'), loc='upper right')
            axes[r][c].set_ylabel( "Stress( MPa )" )
            axes[r][c].set_xlabel( str(num + 1) + " Strain" )



    # axes.set_ylabel( "Stress( MPa )" )
    # axes.set_xlabel( "Strain" )

    # for i in range( num ):
    #     axes.plot( strain[i], stress[i] )
    #     legend.append( str(i + 1) )

    # plt.legend( (legend), loc='upper right')

    plt.show( )
    

# dir = ".\\20.12.16\\"
# dir2 = "Specimen_RawData_1.csv"
# path = [ dir + "1Layer_1.is_flex_RawData\\" + dir2, dir + "1Layer_2.is_flex_RawData\\" + dir2, dir + "1Layer_3.is_flex_RawData\\" + dir2
#         , dir + "1Layer_4.is_flex_RawData\\" + dir2, dir + "1Layer_5.is_flex_RawData\\" + dir2, dir + "1Layer_6.is_flex_RawData\\" + dir2
#         , dir + "1Layer_7.is_flex_RawData\\" + dir2, dir + "1Layer_8.is_flex_RawData\\" + dir2, dir + "1Layer_9.is_flex_RawData\\" + dir2
#         , dir + "1Layer_10.is_flex_RawData\\" + dir2, dir + "1Layer_11.is_flex_RawData\\" + dir2
#         , dir + "1Layer_13.is_flex_RawData\\" + dir2, dir + "1Layer_14.is_flex_RawData\\" + dir2, dir + "1Layer_15.is_flex_RawData\\" + dir2]

dir = ".\\20.12.18\\"
dir2 = "Specimen_RawData_1.csv"
path = [ dir + "1_1.is_flex_RawData\\" + dir2, dir + "1_2.is_flex_RawData\\" + dir2, dir + "1_3.is_flex_RawData\\" + dir2
        ,dir + "2_1.is_flex_RawData\\" + dir2, dir + "2_2.is_flex_RawData\\" + dir2, dir + "2_3.is_flex_RawData\\" + dir2 
        ,dir + "3_1.is_flex_RawData\\" + dir2, dir + "3_2.is_flex_RawData\\" + dir2, dir + "3_3.is_flex_RawData\\" + dir2 
        ,dir + "4_1.is_flex_RawData\\" + dir2, dir + "4_2.is_flex_RawData\\" + dir2, dir + "4_3.is_flex_RawData\\" + dir2 
        ,dir + "5_1.is_flex_RawData\\" + dir2, dir + "5_2.is_flex_RawData\\" + dir2, dir + "5_3.is_flex_RawData\\" + dir2 
        ,dir + "6_1.is_flex_RawData\\" + dir2, dir + "6_2.is_flex_RawData\\" + dir2, dir + "6_3.is_flex_RawData\\" + dir2 
        ,dir + "7_1.is_flex_RawData\\" + dir2, dir + "7_2.is_flex_RawData\\" + dir2, dir + "7_3.is_flex_RawData\\" + dir2 
        ,dir + "8_1.is_flex_RawData\\" + dir2, dir + "8_2.is_flex_RawData\\" + dir2, dir + "8_3.is_flex_RawData\\" + dir2 
        ,dir + "9_1.is_flex_RawData\\" + dir2, dir + "9_2.is_flex_RawData\\" + dir2, dir + "9_3.is_flex_RawData\\" + dir2 
        ,dir + "10_1.is_flex_RawData\\" + dir2, dir + "10_2.is_flex_RawData\\" + dir2, dir + "10_3.is_flex_RawData\\" + dir2 
        ,dir + "11_1.is_flex_RawData\\" + dir2, dir + "11_2.is_flex_RawData\\" + dir2, dir + "11_3.is_flex_RawData\\" + dir2 
        ,dir + "12_1.is_flex_RawData\\" + dir2, dir + "12_2.is_flex_RawData\\" + dir2, dir + "12_3.is_flex_RawData\\" + dir2 
        ,dir + "13_1.is_flex_RawData\\" + dir2, dir + "13_2.is_flex_RawData\\" + dir2, dir + "13_3.is_flex_RawData\\" + dir2 
        ,dir + "14_1.is_flex_RawData\\" + dir2, dir + "14_2.is_flex_RawData\\" + dir2, dir + "14_3.is_flex_RawData\\" + dir2 
        ,dir + "15_1.is_flex_RawData\\" + dir2, dir + "15_2.is_flex_RawData\\" + dir2, dir + "15_3.is_flex_RawData\\" + dir2 
    ]

Flexural = []
stress = []
strain = []

for p in path:
    c = FlexuralCalc( p )
    Flexural.append( c.Apply() )

    #-- check
    if c.stress[0] > 0.:
        print ("strain: " + c.strain[0] + p )

    stress.append( c.stress )
    strain.append( c.strain )

    # name = p.split( "\\" )[-2]
    # Text.WriteTxt( ".\\files\\" + name, c.strStressStrain )

print( Flexural )
Plot( stress, strain )    

# -- Average


        
