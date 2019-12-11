# generates images for various combinations of attributes for Retina
# https://docs.opencv.org/3.0.0/dc/d54/classcv_1_1bioinspired_1_1Retina.html
import os
from cv2 import imread, imwrite, bioinspired, bioinspired_Retina
import defusedxml.ElementTree as ET
import itertools
import re # regular expressions

FindPatternForCapitals = re.compile(r'[A-Z].')

def abbrevOf(term) :
    lenOfTerm = len(term)
    abbrev = term[0:2]
    while True:
        capitals = FindPatternForCapitals.findall(term[2:])
        for capitalStr in capitals:
            abbrev += capitalStr
        return abbrev

def retinaGenerateVariants( originalPictureName, testname, VariantsList, countOfRetries ):

    plainVariantList = []
    abbreviations = {}
    for k in VariantsList.keys(): 
        arrOrValue = VariantsList.get(k) # list or value
        tVj = []
        if isinstance(arrOrValue, list):
            for v in arrOrValue:
                tVj.append((k,v))
        else:
            tVj.append((k,arrOrValue))
        
        plainVariantList.append(tVj)
        
        abbreviations.update( { k: abbrevOf(k) } )

    combinationList = list(itertools.product(*plainVariantList))

    inputImage = imread( originalPictureName )

    retina = bioinspired.Retina_create((inputImage.shape[1], inputImage.shape[0]))

    xmlPropFil = "retinaProps.xml"
    xmlPropUpdFil = "retinaPropsUpd.xml"

    retina.write( xmlPropFil )

    xmlTree = ET.parse(xmlPropFil)
    
    xmlPravoSection = xmlTree.getroot().find('OPLandIPLparvo')

    for propVariant in combinationList:
        pictureOutputName = testname
        for modifier in propVariant:
            forModificationKey = modifier[0]
            forModificationValStr = str(modifier[1])

            pictureOutputName += '_' + abbreviations.get( forModificationKey ) + forModificationValStr
            xmlElement = xmlPravoSection.find(forModificationKey)
            xmlElement.text = forModificationValStr #modification in XML

        xmlTree.write(xmlPropUpdFil,
                xml_declaration=True,encoding='utf-8',
                method="xml")

        retina.setup(xmlPropUpdFil) # load 
        bioinspired_Retina.clearBuffers( retina )
        # seems to be default:
        bioinspired_Retina.setColorSaturation( retina, saturateColors=False, colorSaturationValue=0.0) 

        inputImageUse = inputImage.copy()
        for i in range( countOfRetries ):
            retina.run(inputImageUse)
            retinaOut_parvo = retina.getParvo()

        outfil = pictureOutputName + ".jpg"
        nix = imwrite( outfil , retinaOut_parvo)

os.chdir("H:/Users/gle/Pictures/Romans_40er/prog/Retina/")
'''
retinaGenerateVariants("origin.JPG", "horCellGain",
     [0.05, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8],
     3 )

retinaGenerateVariants(   "origin.JPG", "tQ",
        {   'horizontalCellsGain' : [ 0.3 ],
            'photoreceptorsLocalAdaptationSensitivity' : [0.5, 0.9, 0.99] ,
            'ganglionCellsSensitivity' : [0.5, 0.9, 0.99] },
        7 )

retinaGenerateVariants(   "origin.JPG", "tQ",
        {   'normaliseOutput' : [ 1, 0 ],
            'horizontalCellsGain' : [ 0.001, 0.5, 0.99 ],
            'photoreceptorsLocalAdaptationSensitivity' : [0.5, 0.9, 0.99] ,
            'ganglionCellsSensitivity' : 0.5 },
        7 )        
'''
retinaGenerateVariants(   "origin.JPG", "tQ",
        {   'horizontalCellsGain' :  0.99,
            'photoreceptorsLocalAdaptationSensitivity' : [0.0, 0.5, 0.99] ,
            'ganglionCellsSensitivity' : [ 0.3, 0.7 ] },
        7 )        
# the best result: hoCeGa 0.99 _ phLoAdSe 0.5 _ gaCeSe 0.3
