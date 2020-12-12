import csv
import matplotlib.pyplot as plt

class Text:
    @staticmethod
    def ReadSamples( path ):
        samples = []
        with open( path, newline='' ) as file:
            reader = csv.reader( file)
            for row in reader:
                if row: samples.append( row )

        return samples

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
        self.Extract( )
        self.stress = []
        self.strain = []

    def Extract( self ):
        self.h = float( self.samples[ Field.hRow ][ Field.hCol ] )
        self.b = float( self.samples[ Field.bRow ][ Field.bCol ] )
        self.L = float( self.samples[ Field.LRow ][ Field.LCol ] )

        self.d = []
        self.load = [] # kgf
        sDRow = Field.sDRow
        sLRow = Field.sLRow

        for i in range( len(self.samples[ sDRow: ] ) ):
            self.d.append( float( self.samples[ sDRow ][ Field.sDCol ] ) )
            self.load.append( float( self.samples[ sLRow ][ Field.sLCol ] ) )
            sDRow += 1
            sLRow += 1

    def Apply( self ):
        '''
            Formula: 
                stress: (3*Load * 9.80665*L)/(2*b*POWER(h,2))
                strain: 6*d*h/(POWER(L,2))
        '''
        for i in range( len( self.d ) ):
            d, load = self.d[i], self.load[i]
            self.stress.append( ( 3 * load * 9.8065 * self.L ) / ( 2 * self.b * self.h * self.h ) ) 
            self.strain.append( ( 6 * d * self.h ) / ( self.L * self.L ) )

        start = 5
        end = 45
        m = ( self.stress[end] - self.stress[start] ) / ( self.strain[end] - self.strain[start] )

        return [m, self.h, self.b]

def Plot( stress, strain ):
    num = len( stress )
    fig, axes = plt.subplots( )
    legend = []

    axes.set_ylabel( "Stress( MPa )" )
    axes.set_xlabel( "Strain" )

    for i in range( num ):
        axes.plot( strain[i], stress[i] )
        legend.append( str(i + 1) )

    plt.legend( (legend), loc='upper right')

    plt.show( )
    

dir = ".\\20.12.09\\"
dir2 = "Specimen_RawData_1.csv"
path = [ dir + "1Layer_1.is_flex_RawData\\" + dir2, dir + "1Layer_2.is_flex_RawData\\" + dir2, dir + "1Layer_3.is_flex_RawData\\" + dir2
        , dir + "1Layer_4.is_flex_RawData\\" + dir2, dir + "1Layer_5.is_flex_RawData\\" + dir2, dir + "1Layer_6.is_flex_RawData\\" + dir2
        , dir + "1Layer_7.is_flex_RawData\\" + dir2, dir + "1Layer_8.is_flex_RawData\\" + dir2, dir + "1Layer_9.is_flex_RawData\\" + dir2
        , dir + "1Layer_10.is_flex_RawData\\" + dir2, dir + "1Layer_11.is_flex_RawData\\" + dir2, dir + "1Layer_12.is_flex_RawData\\" + dir2
        , dir + "1Layer_13.is_flex_RawData\\" + dir2, dir + "1Layer_14.is_flex_RawData\\" + dir2, dir + "1Layer_15.is_flex_RawData\\" + dir2]

Flexural = []
stress = []
strain = []
for p in path:
    c = FlexuralCalc( p )
    Flexural.append( c.Apply() )

    stress.append( c.stress )
    strain.append( c.strain )

print( Flexural )
Plot( stress, strain )    



        
