import os
import numpy as np
import subprocess


def executePBRT(configFilename, pathToExecute='/Users/sebastianhoch/Documents/pbrt/pbrt-v4/build/Debug/pbrt', useGPU=False):
   parameters = ''
   if useGPU:
       parameters += ' -gpu'
   output = subprocess.getoutput(pathToExecute+' '+configFilename + parameters)
   return output

def writeLensFilePos(lens, lensFilename='test.dat'):
    f = open(lensFilename, 'w')
    f.write('#')
    f.writelines(lens.description)
    f.write('\n#\tradius\taxpos\tN\taperture\n')
    for i, (rad, axpos, index, semiaperture) in enumerate(zip(lens.radius, lens.pos, lens.index, lens.sa)):
        if i == lens.apertureIndex:
            index = 0
        #print(i, rad, axpos, index, semiaperture)
        f.write(str(rad)+'\t'+str(axpos)+'\t'+str(index)+'\t'+str(semiaperture*2)+'\n')
    f.close()

def writeLensFile(lens, lensFilename='test.dat'):
    f = open(lensFilename, 'w')
    f.write('#')
    f.writelines(lens.description)
    f.write('\n#\tradius\tthickness\tN\taperture\n')
    nelem = len(lens.thickness)
    for i, (rad, thick, index, semiaperture) in enumerate(zip(lens.radius, lens.thickness, lens.index, lens.sa)):
        if i == lens.apertureIndex:
            if rad == 0:
                f.write(str(0)+'\t'+str(thick)+'\t'+str(0)+'\t'+str(semiaperture*2)+'\n')
                continue
            else:
                index = 0

        if i == len(lens.thickness) - 1:
            thick = 0
        print(i, rad, thick, index, semiaperture)
        f.write(str(rad)+'\t'+str(thick)+'\t'+str(index)+'\t'+str(semiaperture*2)+'\n')
    f.close()


def writePBRTConfig(lens, filename="test.pbrt", outputFilename="test.exr", lensFilename="test.dat"):
    buffer = [f'LookAt\t0\t0\t0\n',     # eye
              f'\t0\t1\t0\n',         # look at point
              f'\t0\t0\t1\n',           # up vector
              f'\n',
              f'Camera\t"realistic"\n',
              f'\t"string lensfile"\t"{lensFilename}"\n',
              f'\t"float aperturediameter"\t[{lens.apertureDiameter}]\n',
              f'\t"float focusdistance"\t[{(lambda: 1e9 if lens.objectDistance == np.inf else lens.objectDistance)()}]\n',
              f'\n',
              f'Film\t"gbuffer"\n',
              f'\t"string\tfilename"\t"{outputFilename}"\n',
              f'\t"integer xresolution"\t[512]\n',
              f'\t"integer yresolution"\t[512]\n',
              f'\t"float diagonal"\t[{lens.diagonal}]\n',
              f'\t"bool savefp16"\ttrue\n',
              f'\n',
              f'Sampler\t"halton"\n',
              f'\t"integer pixelsamples"\t[16]\n',
              f'\n',
              f'\n',
              f'WorldBegin\n',
              f'\n',
              f'LightSource\t"infinite"\n',
              f'\t"rgb\tL"\t[.4\t.45\t.5]\n',
              f'\n',
              f'\n',
              f'\tAttributeBegin\n',
              f'\n',
              f'\tTexture\t"checks"\t"spectrum"\t"checkerboard"\n',
              f'\t\t"float uscale"\t[10]\n',
              f'\t\t"float vscale"\t[10]\n',
              f'\t\t"rgb tex1"\t[0.1\t0.1\t0.1]\n',
              f'\t\t"rgb tex2"\t[0.9\t0.9\t0.9]\n',
              f'\tMaterial\t"diffuse"\t"texture\treflectance"\t"checks"\n',
              f'\tTranslate\t0\t{(lambda: 1e9 if lens.objectDistance == np.inf else lens.objectDistance)()}\t0\n',
              f'\tRotate\t30\t0\t1\t0\n',
              f'\tShape\t"bilinearmesh"\n',
              f'\t\t"point3\tP"\t[\t-1\t0\t-1\t\t1\t0\t-1\t\t-1\t0\t1\t\t1\t0\t1]\n',
              f'\t\t"point2\tuv"\t[\t0\t0\t\t0\t1\t\t1\t0\t\t1\t1]\n',
              f'\n',
              f'\tAttributeEnd\n',
              f'\n',
              ]
    f = open(filename, 'w')
    f.writelines(buffer)
    f.close()

    return buffer

if __name__ == "__main__":
    import template_lens
    lens = template_lens.Lens()
    lens.objectDistance = 100

    writeLensFile(lens)
    writePBRTConfig(lens)
    print(executePBRT('test.pbrt'))
